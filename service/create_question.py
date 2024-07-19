from openai import OpenAI
from service.call_env import env_data
import re


class create_question() : 
    def build_regex(result):
        question_pattern = r'\[NEW_QUESTION\]\s*(.*?)\s*\[NEW_ANSWER\]'
        answer_pattern = r'\[NEW_ANSWER\]\s*(.*?)\s*\[NEW_CHOICE\]'
        choice_pattern = r'\[NEW_CHOICE\]\s*(.*)'

        question = re.search(question_pattern, result, re.DOTALL).group(1).strip()
        answer = re.search(answer_pattern, result, re.DOTALL).group(1).strip()
        choice = re.search(choice_pattern, result, re.DOTALL).group(1).strip()

        return {
            'question' : question,
            'answer' : answer,
            'choice' : choice
        }
    
    def run(question, choice, raw_answer):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """
    Anda adalah sebuah sistem pembuat soal, pilihan jawaban, dan penjelasan jawaban dengan tingkat kesulitan yang lebih tinggi dibandingkan soal yang diberikan saat ini. Bahasa yang digunakan antara bahasa indonesia atau bahasa inggris menyesuaikan input yang diberikan
    URUTAN INPUT : [QUESTION], [CHOICE], [RAW_ANSWER]
    URUTAN OUTPUT : [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE]

    Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
    Soal-soal yang anda buat adalah soal BARU, anda tidak bisa merefer ke soal sebelumnya. Anda perlu menjelaskan kembali apa yang diperlukan
    Apabila soal tersebut bertipe sebuah soal yang mengandung teks bahasa indonesia ataupun teks bahasa inggris, anda perlu membuat teks baru sehingga soal yang dibuat tidak merefer ke teks sebelumnya
    Apabila soal dan jawaban menggunakan bahasa inggris, anda wajib tetap menggunakan bahasa inggris untuk membuat soal dan jawaban baru. tujuan anda bukan untuk mengartikan atau mengubah soal dan jawabannya ke bahasa indonesia
    Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
    Pilihan jawaban dengan label [CHOICE] yang berisikan lima pilihan jawaban (A,B,C,D,E)
    Penjelasan jawaban dengan label [RAW_ANSWER]
    Anda ditugaskan untuk membuat soal baru tersebut dengan memahami ketiga aspek yang telah diberikan : [QUESTION], [CHOICE], dan [RAW_ANSWER] untuk menghasilkan soal baru yang serupa, tetapi dengan tingkat kesulitan yang lebih tinggi [NEW_QUESTION], pilihan jawaban baru berdasarkan soal baru [NEW_CHOICE], dan pembahasan jawabannya [NEW_ANSWER]

    Langkah pembuatan :
    Hal yang pertama dibuat adalah pertanyaan yang akan dijadikan sebagai [NEW_QUESTION]
    Anda akan mendeteksi terlebih dahulu bahasa apa yang digunakan pada [NEW_QUESTION], yaitu bahasa indonesia atau bahasa inggris
    Apabila pada soal mengandung sebuah bacaan teks bahasa indonesia atau teks bahasa inggris, yaitu sebuah teks bacaan yang memuat minimal terdiri dari 2 paragraf atau minimal 200 kata, anda perlu membuat ulang sebuah teks dengan minimal 3 paragraf atau minimal 300 kata (MINIMUM 3 PARAGRAPH OR 250 TEXT) pada [NEW_QUESTION] yang masih relevan pada topik bacaan di [QUESTION] . Dilarang untuk memberikan bacaan yang panjang teksnya terdiri dari 1 paragraf saja atau dibawah 200 kata pada [NEW_QUESTION] untuk kasus ini 
    Apabila [QUESTION] dan [CHOICE] menggunakan bahasa inggris, anda tetap harus menggunakan bahasa inggris untuk membuat [NEW_QUESTION] dan [NEW_CHOICE]. Tugas anda bukan menerjemahkannya ke bahasa indonesia, tetapi membuat soal dengan topik yang sama beserta jawabannya. Dengan demikian [NEW_QUSTION] dan [NEW_CHOICE] DILARANG menggunakan bahasa indonesia
    Setelah itu dibuatlah pembahasan yang terperinci dari [NEW_QUESTION] untuk membuat [NEW_ANSWER]
    Jawaban pada [NEW_ANSWER] berdasarkan [NEW_QUESTION], bukan menggunakan hal yang sama pada [RAW_ANSWER]
    Untuk soal matematika, [NEW_ANSWER] diharapkan juga menampilkan langkah-langkah sampai jawaban akhir
    Pada tahap ini anda telah mendapatkan [NEW_QUESTION] dan [NEW_ANSWER]

    Setelah didapatkan jawaban yang ada pada [NEW_ANSWER], anda akan melanjutkan membuat [NEW_CHOICE]
    Cara pembuatan [NEW_CHOICE] adalah dengan membuat format sebagai berikut: 
    A. Jawaban 1
    B. Jawaban 2
    C. Jawaban 3
    D. Jawaban 4
    E. Jawaban 5
    Pastikan bahwa jawaban yang ada pada [NEW_ANSWER] terdapat pada salah satu pilihan yang ada di [NEW_QUESTION]

    Pada tahap ini anda telah mendapatkan [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE]

    Setelah itu anda akan melakukan update pada jawaban yang terkandung di [NEW_ANSWER] dengan langkah-langkah seperti di bawah ini (pilihan jawaban di [NEW_CHOICE] tidak boleh berbeda dengan yang ada di [NEW_ANSWER]):
    Pada [NEW_ANSWER] anda akan membaginya menjadi 3 topik, yaitu : pemahaman soal, pembahasan pilihan jawaban, dan kesimpulan
    Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [NEW_QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut
    Pembahasan pilihan jawaban adalah paragraf yang menjelaskan masing-masing jawaban (A,B,C,D,E) yang diberikan dengan bantuan analisis yang telah anda lakukan dalam memahami soal sehingga anda menemukan satu jawaban yang paling sesuai dan pemabahasan setiap jawaban-jawaban yang ada
    Kesimpulan adalah paragraf yang menjelaskan jawaban akhir yang dipilih dengan memilih salah satu dari choice yang disediakan pada [NEW_CHOICE]

    NOTE:
    Apabila soal bertipe matematika atau perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjabarkan secara detail langkah-langkah untuk mengerjakan soal yang tetera bersamaan dengan hasil perhitungannya pada [NEW_QUESTION], tidak perlu menjelaskan satu-satu jawaban yang ada pada [NEW_CHOICE]
    Apabila soal berbahasa inggris, wajib menggunakan bahasa inggris untuk membuat [NEW_QUESTION] dan [NEW_CHOICE], tetapi untuk penjelasan yang ada pada [NEW_ANSWER] wajib menggunakan bahasa indonesia. Namun, untuk urutan keluaran tetap wajib seperti urutan ini : [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE]
    Sebelum output dikeluarkan, mohon pastikan kembali urutan output adalah [NEW_QUESTION] dilanjutkan dengan [NEW_ANSWER] dan ditutup dengan [NEW_CHOICE]
    """
        bc_question = """
        Tika, Pita, Ana, Ira, dan Retha pergi bersama ke toko buah. Empat orang diantara mereka membeli jeruk. Pita dan Ira tidak membeli apel seperti lainnya. pita hanya membeli anggur. Tika dan Retha juga tidak membeli anggur seperti yang lainnya. siapakah yang membeli jenis buah yang sama persis?
        """
        bc_choice = """
        A. Tika dan Ira
        B. Ana dan Ira
        C. Tika dan Ana
        D. Tika dan Pita
        E. Tika dan Retha
        """

        bc_answer = """
        Tika, Pita, Ana, Ira, Retha
        4 orang membeli jeruk
        Pita dan Ira tidak membeli apel
        Pita hanya membeli anggur.
        Tika dan Retha tidak membeli anggur Kesimpulan
        Pita membeli anggur Tika membeli Jeruk, Apel Ana membeli Jeruk, Apel, anggur Ira membeli Jeruk, Anggur Retha membeli Jeruk, Apel
        """

        bc_regenerate = """
        [NEW_QUESTION]
        Dalam sebuah acara arisan, Lima teman yaitu Budi, Doni, Eka, Fina, dan Gita membeli beberapa jenis buah untuk dihidangkan. Tiga dari mereka memilih untuk membeli pisang. Budi dan Eka tidak membeli semangka berbeda dengan yang lain. Doni hanya membeli melon. Gita dan Fina juga tidak membeli melon seperti yang lainnya. Siapakah yang membeli jenis buah yang sama persis?

        [NEW_ANSWER]
        Pemahaman soal: 
        Untuk menyelesaikan soal ini, perhatikan distribusi buah yang mungkin dibeli oleh setiap orang berdasarkan informasi yang diberikan:
        - Tiga orang membeli pisang.
        - Budi dan Eka tidak membeli semangka.
        - Doni hanya membeli melon.
        - Gita dan Fina tidak membeli melon.

        Pembahasan pilihan jawaban: 
        A. Budi dan Doni - Tidak cocok karena Doni hanya membeli melon, sementara Budi tidak membeli melon dan semangka.
        B. Eka dan Doni - Tidak cocok, alasan sama dengan A.
        C. Budi dan Eka - Kombinasi buah yang dibeli bisa sama, tetapi tidak ada informasi pasti tentang buah lain yang dibeli selain pisang.
        D. Fina dan Gita - Cocok karena kedua membeli pisang dan semangka, dan tidak membeli melon.
        E. Gita dan Doni - Tidak cocok karena Doni hanya membeli melon sementara Gita tidak membeli melon.

        Kesimpulan: 
        Berdasarkan analisis dan informasi yang diberikan, Fina dan Gita adalah dua orang yang membeli jenis buah yang sama persis.

        [NEW_CHOICE]
        A. Budi dan Doni
        B. Eka dan Doni
        C. Budi dan Eka
        D. Fina dan Gita
        E. Gita dan Doni"""

        complation = client.chat.completions.create(
        model = 'gpt-4-turbo',
        messages = [
            {
                "role": "system", "content": task
            },
            {
                                "role": "user", "content": "[QUESTION]: " + bc_question
                            },
                            {
                                "role": "user", "content": "[CHOICE]: " + bc_choice
                            },
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + bc_answer 
                            },
                            {
                                "role": "assistant", "content": "[OUTPUT]: " + bc_regenerate
                            },
                            {
                "role": "system", "content": task
            },
            {
                                "role": "user", "content": "[QUESTION]: " + question
                            },
                            {
                                "role": "user", "content": "[CHOICE]: " + choice
                            },
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + raw_answer 
                            }
            
            ]
        )

        result = complation.choices[0].message.content

        return create_question.build_regex(result)
