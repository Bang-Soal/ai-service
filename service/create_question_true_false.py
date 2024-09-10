from openai import OpenAI
from service.call_env import env_data
import re


class create_question_true_false() : 
    def build_regex(result):
        question_pattern = r"\[NEW_QUESTION\]:\s*(.*?)\n\[NEW_ANSWER\]"
        answer_pattern = r"\[NEW_ANSWER\]:\s*(.*?)\n\[NEW_CHOICE\]"
        choice_pattern = r"\[NEW_CHOICE\]:\s*(.*?)$"

        question_match = re.search(question_pattern, result, re.DOTALL)
        question = question_match.group(1).strip() if question_match else None

        answer_match = re.search(answer_pattern, result, re.DOTALL)
        answer = answer_match.group(1).strip() if answer_match else None

        choice_match = re.search(choice_pattern, result, re.DOTALL)
        choice_block = choice_match.group(1).strip() if choice_match else None

        choice = []
        choice_lines = choice_block.split("\n")
        for line in choice_lines:
            if line:
                parts = line.split(" - ")
                statement = parts[0].strip()
                is_true = parts[1].strip() == "TRUE"
                choice.append({
                    "statement": statement,
                    "is_true": is_true,
                })
        
        return {
            'question' : question,
            'choice' : choice,
            'answer' : answer
            }

        
    
    def run(question, total_question):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """
Anda adalah sebuah sistem pembuat soal berjenis TRUE-FALSE dari sebuah argumen yang diberikan dan penjelasan jawaban dengan tingkat kesulitan yang lebih tinggi dibandingkan soal yang diberikan saat ini. Bahasa yang digunakan antara bahasa indonesia atau bahasa inggris menyesuaikan input yang diberikan. Penjelasan wajib menggunakan bahasa indonesia karena target penggunanya adalah siswa yang berasal dari indonesia
URUTAN INPUT : [QUESTION], [TOTAL_QUESTION]
URUTAN OUTPUT : [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE]

Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
Soal-soal yang anda buat adalah soal BARU, anda tidak bisa merefer ke soal sebelumnya. Anda perlu menjelaskan kembali apa yang diperlukan
Apabila soal tersebut bertipe sebuah soal yang mengandung teks bahasa indonesia ataupun teks bahasa inggris, anda perlu membuat teks baru sehingga soal yang dibuat tidak merefer ke teks sebelumnya
Apabila soal dan jawaban menggunakan bahasa inggris, anda wajib tetap menggunakan bahasa inggris untuk membuat soal dan jawaban baru. tujuan anda bukan untuk mengartikan atau mengubah soal dan jawabannya ke bahasa indonesia
Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
Anda akan diberikan sebuah total argumentasi TRUE-FALSE yang perlu dibuat [TOTAL_QUESTION]
Anda ditugaskan untuk membuat soal baru tersebut dengan memahami kedua aspek yang telah diberikan : [QUESTION] dan [TOTAL_QUESTION] untuk menghasilkan soal baru yang serupa, tetapi dengan tingkat kesulitan yang lebih tinggi [NEW_QUESTION], pilihan argumen TRUE-FALSE berdasarkan soal baru [NEW_CHOICE], dan pembahasan jawabannya [NEW_ANSWER]
Format dari [NEW_CHOICE] adalah "[No urutan].Argumen - TRUE/FALSE"

Langkah pembuatan :
Hal yang pertama dibuat adalah pertanyaan yang akan dijadikan sebagai [NEW_QUESTION]
Anda akan mendeteksi terlebih dahulu bahasa apa yang digunakan pada [NEW_QUESTION], yaitu bahasa indonesia atau bahasa inggris
Apabila pada soal mengandung sebuah bacaan teks bahasa indonesia atau teks bahasa inggris, yaitu sebuah teks bacaan yang memuat minimal terdiri dari 2 paragraf atau minimal 200 kata, anda perlu membuat ulang sebuah teks dengan minimal 3 paragraf atau minimal 300 kata (MINIMUM 3 PARAGRAPH OR 250 TEXT) pada [NEW_QUESTION] yang masih relevan pada topik bacaan di [QUESTION] . Dilarang untuk memberikan bacaan yang panjang teksnya terdiri dari 1 paragraf saja atau dibawah 200 kata pada [NEW_QUESTION] untuk kasus ini 
Apabila [QUESTION] menggunakan bahasa inggris, anda tetap harus menggunakan bahasa inggris untuk membuat [NEW_QUESTION] dan [NEW_CHOICE]. Tugas anda bukan menerjemahkannya ke bahasa indonesia, tetapi membuat soal dengan topik yang sama beserta jawabannya. Dengan demikian [NEW_QUSTION] dan [NEW_CHOICE] DILARANG menggunakan bahasa indonesia
Setelah itu dibuatlah argumen-argumen TRUE/FALSE pada [NEW_CHOICE] berdasarkan jumlah argumen yang diminta [TOTAL_QUESTION]
Setelah itu dibuatlah pembahasan yang terperinci dari [NEW_QUESTION] berdasarkan [TOTAL_QUESTION] untuk membuat [NEW_ANSWER]
Untuk soal matematika, [NEW_ANSWER] diharapkan juga menampilkan langkah-langkah sampai jawaban akhir
[NEW_ANSWER] menjelaskan secara rinci mengenai argumen-argumen yang ada pada [NEW_CHOICE] mengapa argumen tersebut dapat bernilai TRUE atau FALSE
Format dari [NEW_ANSWER] untuk setiap argumen-argumen yang ada pada [NEW_CHOICE] adalah 
Argumen - TRUE/FALSE
Explanation : [penjelasan argumen] 

contoh : 
Rising ocean temperatures will reduce the frequency of hurricanes and typhoons. - FALSE
Explanation: Naiknya suhu laut sebenarnya meningkatkan kekerapan dan intensitas badai seperti angin topan dan hurricane karena menyediakan lebih banyak energi dan uap air.

NOTE:
Apabila soal bertipe matematika atau perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjabarkan secara detail langkah-langkah untuk mengerjakan soal yang tetera bersamaan dengan hasil perhitungannya pada [NEW_QUESTION], tidak perlu menjelaskan satu-satu jawaban yang ada pada [NEW_CHOICE]
Apabila soal berbahasa indonesia, wajib menggunakan bahasa indonesia untuk membuat [NEW_QUESTION] dan [NEW_CHOICE], tetapi untuk penjelasan yang ada pada [NEW_ANSWER] wajib menggunakan bahasa indonesia. Namun, untuk urutan keluaran tetap wajib seperti urutan ini : [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE]
Apabila soal berbahasa inggris, wajib menggunakan bahasa inggris untuk membuat [NEW_QUESTION] dan [NEW_CHOICE], tetapi untuk penjelasan yang ada pada [NEW_ANSWER] wajib menggunakan bahasa indonesia. Namun, untuk urutan keluaran tetap wajib seperti urutan ini : [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE]
Sebelum output dikeluarkan, mohon pastikan kembali urutan output adalah [NEW_QUESTION] dilanjutkan dengan [NEW_ANSWER] dan ditutup dengan [NEW_CHOICE]

Contoh Output : 
[NEW_QUESTION]: 
Penggunaan plastik dalam kehidupan sehari-hari memiliki dampak pada kesehatan dan lingkungan. Produk plastik seperti kantong plastik yang sering digunakan dalam berbelanja memiliki sifat yang tahan lama dan tidak mudah terurai. Plastik dapat bertahan di lingkungan selama hingga 500 tahun. Dengan penggunaan yang masif dan berkelanjutan, plastik telah menyumbangkan jumlah sampah yang besar, yang memiliki dampak langsung pada ekosistem dan kesehatan manusia.  

Kantong plastik dianggap sebagai salah satu penyumbang utama polusi karena sifatnya yang tahan lama dan produksinya yang murah. Dampak lingkungan dari kantong plastik muncul ketika mereka tidak dibuang dengan benar, mengakibatkan polusi visual di perkotaan dan bahkan mempengaruhi kehidupan hewan yang salah memakan plastik sebagai makanan. Selain itu, kantong plastik juga dapat merilis zat berbahaya seperti Bisphenol A (BPA) saat terurai, yang memiliki konsekuensi serius terhadap kesehatan, merusak hormon dan meningkatkan risiko penyakit seperti gangguan hormonal, kanker, dan efek reproduktif.

Berbagai upaya telah dilakukan untuk mengurangi penggunaan kantong plastik, termasuk pengenaan tarif, pelarangan penggunaan, dan mempromosikan tas belanja yang dapat digunakan kembali. Meskipun demikian, tantangan tetap ada karena keefektifan kebijakan-kebijakan ini masih terbatas dan penggunaan kantong plastik masih tinggi di berbagai bagian dunia.

[NEW_ANSWER]:
1. Kantong plastik dapat bertahan hingga 500 tahun di lingkungan - TRUE
Explanation: Kantong plastik terbuat dari polimer yang sangat tahan lama dan tidak mudah terurai secara biologis, sehingga memungkinkan mereka bertahan di lingkungan hingga berabad-abad.

2. Penggunaan kembali kantong plastik tidak mempengaruhi kesehatan manusia - FALSE
Explanation: Penggunaan kembali kantong plastik, terutama yang sudah tua dan mulai terurai, dapat melepaskan zat kimia seperti Bisphenol A (BPA), yang diketahui memberikan efek negatif pada kesehatan, termasuk pengaruh pada hormon dan potensi gangguan kesehatan serius lainnya.

3. Kebijakan larangan penggunaan kantong plastik telah efektif mengurangi polusi plastik di seluruh dunia - FALSE
Explanation: Meskipun telah ada upaya dan kebijakan larangan penggunaan kantong plastik di beberapa negara, penggunaannya masih tinggi di beberapa bagian dunia dan efektivitas kebijakan ini dalam mengurangi polusi secara global masih terbatas.

[NEW_CHOICE]:
1. Kantong plastik dapat bertahan hingga 500 tahun di lingkungan - TRUE
2. Penggunaan kembali kantong plastik tidak mempengaruhi kesehatan manusia - FALSE
3. Kebijakan larangan penggunaan kantong plastik telah efektif mengurangi polusi plastik di seluruh dunia - FALSE
"""

        complation = client.chat.completions.create(
        model = 'gpt-4-turbo',
        messages = [
            {
                "role": "system", "content": task
            },
            {
                                "role": "user", "content": "[QUESTION]: " + question
                            },
                            {
                                "role": "user", "content": "[TOTAL_QUESTION]: " + total_question
                            },

        ]
        )
        result = complation.choices[0].message.content

        return create_question_true_false.build_regex(result)
