from openai import OpenAI
from service.call_env import env_data
import re


class create_answer_tf() : 
    def run(question, choice, description):
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
Format dari [NEW_CHOICE] adalah "[Urutan Abjad]. Argumen - TRUE/FALSE"

Langkah pembuatan :
Hal yang pertama dibuat adalah pertanyaan yang akan dijadikan sebagai [NEW_QUESTION]
Anda akan mendeteksi terlebih dahulu bahasa apa yang digunakan pada [NEW_QUESTION], yaitu bahasa indonesia atau bahasa inggris
Apabila pada soal mengandung sebuah bacaan teks bahasa indonesia atau teks bahasa inggris, yaitu sebuah teks bacaan yang memuat minimal terdiri dari 2 paragraf atau minimal 200 kata, anda perlu membuat ulang sebuah teks dengan minimal 3 paragraf atau minimal 300 kata (MINIMUM 3 PARAGRAPH OR 250 TEXT) pada [NEW_QUESTION] yang masih relevan pada topik bacaan di [QUESTION] . Dilarang untuk memberikan bacaan yang panjang teksnya terdiri dari 1 paragraf saja atau dibawah 200 kata pada [NEW_QUESTION] untuk kasus ini 
Apabila [QUESTION] menggunakan bahasa inggris, anda tetap harus menggunakan bahasa inggris untuk membuat [NEW_QUESTION] 
Setelah membuat paragara [NEW_QUESTION], paragraf [NEW_QUESTION] wajib ditambah dengan kalimat ini "Pernyataan-pernyataan di bawah ini yang tepat adalah ..."
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
"""

        complation = client.chat.completions.create(
            model = 'gpt-4o',
             messages = [
        {
            "role": "system", "content": task
        },
        {
                            "role": "user", "content": "[QUESTION]: " + question
                        },{
                            "role": "user", "content": "[CHOICE]: " + choice
                        },
                        {
                            "role": "user", "content": "[DESCRIPTION]: " + description
                        }]
        )

        result = complation.choices[0].message.content
        result = result.replace("[FINAL_ANSWER]:" , "")
        result = result.strip()
        return result