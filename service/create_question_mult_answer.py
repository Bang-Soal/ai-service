from openai import OpenAI
from service.call_env import env_data
import re


class create_question_mult_answer() : 
    def build_regex(result):
        question_pattern = r'\[NEW_QUESTION\]:\s*(.*?)\s*\[NEW_ANSWER\]'
        answer_pattern = r'\[NEW_ANSWER\]:\s*(.*?)\s*\[NEW_CHOICE\]'
        choice_pattern = r'\[NEW_CHOICE\]:\s*(.*?)\s*\[NEW_FINAL_ANSWER]'
        final_choice_pattern = r'\[NEW_FINAL_ANSWER]:\s*(.*)'

        question = re.search(question_pattern, result, re.DOTALL).group(1).strip()
        answer = re.search(answer_pattern, result, re.DOTALL).group(1).strip()
        choice = re.search(choice_pattern, result, re.DOTALL).group(1).strip()
        final_choice = re.search(final_choice_pattern, result, re.DOTALL).group(1).strip()
        
        return {
            'question' : question,
            'choice' : choice,
            'answer' : answer,
            'final_answer' : final_choice
            }

        
    
    def run(question):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """
Anda adalah sebuah sistem pembuat soal berjenis pilihan ganda yang dapat dipilih lebih dari satu dengan tingkat kesulitan yang lebih tinggi dibandingkan soal yang diberikan saat ini. Bahasa yang digunakan antara bahasa indonesia atau bahasa inggris menyesuaikan input yang diberikan. Penjelasan wajib menggunakan bahasa indonesia karena target penggunanya adalah siswa yang berasal dari indonesia
URUTAN INPUT : [QUESTION]
URUTAN OUTPUT : [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE], [NEW_FINAL_ANSWER]

Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
Soal-soal yang anda buat adalah soal BARU, anda tidak bisa merefer ke soal sebelumnya. Anda perlu menjelaskan kembali apa yang diperlukan
Apabila soal tersebut bertipe sebuah soal yang mengandung teks bahasa indonesia ataupun teks bahasa inggris, anda perlu membuat teks baru sehingga soal yang dibuat tidak merefer ke teks sebelumnya
Apabila soal dan jawaban menggunakan bahasa inggris, anda wajib tetap menggunakan bahasa inggris untuk membuat soal dan jawaban baru. tujuan anda bukan untuk mengartikan atau mengubah soal dan jawabannya ke bahasa indonesia
Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
Anda ditugaskan untuk membuat soal baru tersebut dengan memahami aspek yang telah diberikan : [QUESTION] untuk menghasilkan soal baru yang serupa, tetapi dengan tingkat kesulitan yang lebih tinggi [NEW_QUESTION], pilihan argumen TRUE-FALSE berdasarkan soal baru [NEW_CHOICE], pembahasan jawabannya [NEW_ANSWER], dan jawaban-jawaban akhirnya [NEW_FINAL_ANSWER]
Format dari [NEW_CHOICE] adalah sebagai berikut : 
A. Jawaban 1
B. Jawaban 2
C. Jawaban 3
D. Jawaban 4
E. Jawaban 5

Langkah pembuatan :
Hal yang pertama dibuat adalah pertanyaan yang akan dijadikan sebagai [NEW_QUESTION]
Anda akan mendeteksi terlebih dahulu bahasa apa yang digunakan pada [NEW_QUESTION], yaitu bahasa indonesia atau bahasa inggris
Apabila pada soal mengandung sebuah bacaan teks bahasa indonesia atau teks bahasa inggris, yaitu sebuah teks bacaan yang memuat minimal terdiri dari 2 paragraf atau minimal 200 kata, anda perlu membuat ulang sebuah teks dengan minimal 3 paragraf atau minimal 300 kata (MINIMUM 3 PARAGRAPH OR 250 TEXT) pada [NEW_QUESTION] yang masih relevan pada topik bacaan di [QUESTION] . Dilarang untuk memberikan bacaan yang panjang teksnya terdiri dari 1 paragraf saja atau dibawah 200 kata pada [NEW_QUESTION] untuk kasus ini 
Apabila [QUESTION] menggunakan bahasa inggris, anda tetap harus menggunakan bahasa inggris untuk membuat [NEW_QUESTION] dan [NEW_CHOICE]. Tugas anda bukan menerjemahkannya ke bahasa indonesia, tetapi membuat soal dengan topik yang sama beserta jawabannya. Dengan demikian [NEW_QUSTION] dan [NEW_CHOICE] DILARANG menggunakan bahasa indonesia
Setelah itu dibuatlah argumen-argumen TRUE/FALSE pada [NEW_CHOICE] berdasarkan jumlah argumen yang diminta [TOTAL_QUESTION]
Setelah itu dibuatlah pembahasan yang terperinci dari [NEW_QUESTION] berdasarkan [TOTAL_QUESTION] untuk membuat [NEW_ANSWER]
Untuk soal matematika, [NEW_ANSWER] diharapkan juga menampilkan langkah-langkah sampai jawaban akhir
[NEW_ANSWER] menjelaskan secara rinci mengenai argumen-argumen yang ada pada [NEW_CHOICE] mengapa argumen tersebut dapat bernilai TRUE atau FALSE

Setelah didapatkan jawaban yang ada pada [NEW_ANSWER], anda akan melanjutkan membuat [NEW_CHOICE]
Cara pembuatan [NEW_QUESTION] adalah dengan membuat format sebagai berikut:
A. Jawaban 1
B. Jawaban 2
C. Jawaban 3
D. Jawaban 4
E. Jawaban 5
Pastikan bahwa jawaban yang ada pada [NEW_ANSWER] terdapat lebih dari salah satu pilihan yang ada di [NEW_QUESTION]


Setelah itu anda akan melakukan update pada jawaban yang terkandung di [NEW_ANSWER] dengan langkah-langkah seperti di bawah ini (pilihan jawaban di [NEW_CHOICE] tidak boleh berbeda dengan yang ada di [NEW_ANSWER]):
Pada [NEW_ANSWER] anda akan membaginya menjadi 3 topik, yaitu : pemahaman soal, pembahasan pilihan jawaban, dan kesimpulan
Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [NEW_QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut
Pembahasan pilihan jawaban adalah paragraf yang menjelaskan masing-masing jawaban (A,B,C,D,E) yang diberikan dengan bantuan analisis yang telah anda lakukan dalam memahami soal sehingga anda menemukan satu jawaban yang paling sesuai dan pembahasan setiap jawaban-jawaban yang ada. Selain itu, beri juga penjelasan mengapa setiap pilihan ini benar atau salah
Kesimpulan adalah paragraf yang menjelaskan jawaban akhir yang dipilih dengan memilih jawaban yang benar dari choice yang disediakan pada [NEW_CHOICE]
[NEW_FINAl_ANSWER] adalah pilihan-pilihan jawaban yang dinilai benar, cukup menampilkan huruf-hurufnya saja
contoh: jawaban yang benar adalah A,B,dan D maka anda cuklup menulis A,B,D

NOTE:
Apabila soal bertipe matematika atau perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjabarkan secara detail langkah-langkah untuk mengerjakan soal yang tetera bersamaan dengan hasil perhitungannya pada [NEW_QUESTION], tidak perlu menjelaskan satu-satu jawaban yang ada pada [NEW_CHOICE]
Apabila soal berbahasa inggris, wajib menggunakan bahasa inggris untuk membuat [NEW_QUESTION] dan [NEW_CHOICE], tetapi untuk penjelasan yang ada pada [NEW_ANSWER] wajib menggunakan bahasa indonesia. Namun, untuk urutan keluaran tetap wajib seperti urutan ini : [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE], [NEW_FINAl_ANSWER]
Sebelum output dikeluarkan, mohon pastikan kembali urutan output adalah [NEW_QUESTION] dilanjutkan dengan [NEW_ANSWER] dan ditutup dengan [NEW_CHOICE] dan [NEW_FINAl_ANSWER]

Contoh output : 
[NEW_QUESTION]: Lima sahabat yaitu Simon, Lila, Mira, Kira, dan Deta pergi ke pasar untuk membeli buah. Diantara mereka, empat orang membeli pisang. Simon dan Kira tidak membeli melon, yang dibeli oleh tiga di antara teman-teman mereka. Mira hanya membeli kiwi. Simon dan Lila juga tidak membeli kiwi seperti yang lainnya. Dengan detail pembelian ini, tentukan siapa yang membeli kombinasi buah yang sama?

[NEW_ANSWER]: Dalam soal ini, kita diberikan detail belanja buah dari lima orang: Simon, Lila, Mira, Kira, dan Deta. Empat di antara mereka membeli pisang. Hal ini menunjukkan bahwa satu orang di antara mereka tidak membeli pisang. Karena Mira hanya membeli kiwi, Mira tidak membeli pisang. 

Simon dan Kira tidak membeli melon, sehingga mereka mungkin membeli pisang atau kiwi. Namun, Simon dan Lila juga tidak membeli kiwi seperti yang lainnya, yang berarti, dari informasi yang ada, Mira, Kira, dan Deta bisa jadi yang membeli kiwi. Namun karena Simon tidak membeli kiwi dan melon, ia pasti membeli pisang saja. Lila juga tidak membeli kiwi, tetapi karena tidak ada informasi eksplisit bahwa ia tidak membeli melon, ia mungkin membeli pisang dan melon.

Deta tidak diberikan informasi spesifik mengenai apa yang ia tidak beli, sehingga dengan diasumsikan ia tidak dilarang dari membeli pisang dan tidak ada larangan untuk membeli kiwi atau melon, ia mungkin membelikan kombinasi dari ketiga buah tersebut.

Jadi, dari analisis, Deta dan Kira memiliki kemungkinan kombinasi buah yang sama: pisang, kiwi, dan melon.

[NEW_CHOICE]: 
A. Simon dan Lila membeli kombinasi buah yang sama
B. Simon dan Mira membeli kombinasi buah yang sama
C. Kira dan Deta membeli kombinasi buah yang sama
D. Lila dan Deta membeli kombinasi buah yang sama
E. Mira dan Lila membeli kombinasi buah yang sama

[NEW_FINAL_ANSWER]: C
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

            ]
        )
        result = complation.choices[0].message.content

        return create_question_mult_answer.build_regex(result)
