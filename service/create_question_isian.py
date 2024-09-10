from openai import OpenAI
from service.call_env import env_data
import re


class create_question_isian() : 
    def build_regex(result):
        pattern = r"\[NEW_QUESTION\]:\s*(.*?)\s*\[NEW_ANSWER\]:\s*(.*?)\s*\[NEW_FINAL_ANSWER\]:\s*(.*?)\s*$"
        match = re.search(pattern, result, re.DOTALL)
        if match:
            new_question = match.group(1).strip()
            new_answer = match.group(2).strip()
            new_final_answer = match.group(3).strip()

            return {
            'question' : new_question,
            'explanation' : new_answer,
            'answer' : new_final_answer
            }
        else:
            return {
                'message' : "response error"
            }

        
    
    def run(question, explanation, answer):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """
Anda adalah sebuah sistem pembuat soal bertipe isian yang ditandai dengan [FILL] untuk bagian blank (bagian yang perlu diisi oleh user) dan penjelasan jawaban dengan tingkat kesulitan yang lebih tinggi dibandingkan soal yang diberikan saat ini. Bahasa yang digunakan antara bahasa indonesia atau bahasa inggris menyesuaikan input yang diberikan
URUTAN INPUT : [QUESTION], [ANSWER], [FINAL_ANSWER]
URUTAN OUTPUT : [NEW_QUESTION], [NEW_ANSWER], [NEW_FINAL_ANSWER]

Soal-soal ini adalah soal matematika
Soal-soal yang anda buat adalah soal BARU, anda tidak bisa merefer ke soal sebelumnya. Anda perlu menjelaskan kembali apa yang diperlukan
Soal bertipe isian adalah jenis soal di mana peserta diminta untuk mengisi bagian kosong dengan jawaban yang tepat. Bagian kosong ini biasanya ditandai dengan sebuah tempat kosong, sering dilambangkan dengan garis atau tanda seperti [FILL]. Tidak seperti soal pilihan ganda, soal isian menuntut peserta untuk memberikan jawaban secara mandiri, tanpa opsi jawaban yang disediakan.
Dengan demikian, anda perlu melakukan parafrase pada soal agar tidak membuat soal yang bersifat pertanyaan (umumnya menggunakan "?") 
Soal yang anda buat hanya perlu memiliki satu jawaban final, bukan soal yang bisa diisi dengan lebih dari 1 jawaban (memiliki banyak kemungkinan)
Apabila soal dan jawaban menggunakan bahasa inggris, anda wajib tetap menggunakan bahasa inggris untuk membuat soal dan jawaban baru. tujuan anda bukan untuk mengartikan atau mengubah soal dan jawabannya ke bahasa indonesia
Anda akan diberikan sebuah pertanyaan dengan label [QUESTION] tanpa ada bagian blank [FILL] dan jawaban dari question tersebut [ANSWER]
Anda ditugaskan untuk membuat soal baru tersebut dengan memahami ketiga aspek yang telah diberikan : [QUESTION] untuk menghasilkan soal baru yang serupa, [ANSWER] penjelasan jawaban dari [QUESTION], dan [FINAL_ANSWER] jawaban dari [QUESTION]. Hasilnya adalah soal  tetapi dengan tingkat kesulitan yang lebih tinggi [NEW_QUESTION] dan anda perlu membuat [FILL] sebagai penanda blank yang ada di [NEW_QUESTION] (hal ini didasari karena anda membuat sebuah soal bertipe isian), pembahasan jawabannya [NEW_ANSWER], dan jawaban akhir [NEW_FINAL_ANSWER]

Langkah pembuatan :
Hal yang pertama dibuat adalah pertanyaan yang akan dijadikan sebagai [NEW_QUESTION] dan anda perlu membuat [FILL] sebagai penanda bagian blank yang ada di [NEW_QUESTION]
Anda akan mendeteksi terlebih dahulu bahasa apa yang digunakan pada [NEW_QUESTION], yaitu bahasa indonesia atau bahasa inggris
Apabila [QUESTION] menggunakan bahasa inggris, anda tetap harus menggunakan bahasa inggris untuk membuat [NEW_QUESTION]. Tugas anda bukan menerjemahkannya ke bahasa indonesia, tetapi membuat soal dengan topik yang sama beserta jawabannya. Dengan demikian [NEW_QUSTION] DILARANG menggunakan bahasa indonesia
Setelah itu dibuatlah pembahasan yang terperinci dari [NEW_QUESTION] untuk membuat [NEW_ANSWER]
Untuk soal matematika, [NEW_ANSWER] diharapkan juga menampilkan langkah-langkah sampai jawaban akhir
Pada tahap ini anda telah mendapatkan [NEW_QUESTION] dan [NEW_ANSWER]
Setelah didapatkan jawaban yang ada pada [NEW_ANSWER], anda akan membuat jawaban final [NEW_FINAL_ANSWER]
[NEW_FINAL_ANSWER] hanya sebuah angka saja, tidak perlu diikuti dengan penjelasannya saja. Apabila merupakan angka desimal, cukup keluarkan 2 angka di belakang koma
Pada [NEW_ANSWER] anda akan membaginya menjadi 3 topik, yaitu : pemahaman soal dan kesimpulan
Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [NEW_QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut
Kesimpulan adalah paragraf yang merangkum pembahasan serta menyertakan jawaban akhirnya

NOTE:
Apabila soal bertipe matematika atau perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjabarkan secara detail langkah-langkah untuk mengerjakan soal yang tetera bersamaan dengan hasil perhitungannya pada [NEW_QUESTION]
Sebelum output dikeluarkan, mohon pastikan kembali urutan output adalah [NEW_QUESTION] dilanjutkan dengan [NEW_ANSWER] dan ditutup dengan [NEW_FINAL_ANSWER]
"""
        bc_question = """
Panitia jalan sehat akan membuat kupon bernomor yang terdiri atas 4 angka yang disusun oleh angkaangka \( 0,1,3,5 \) dan 7 . Jika angka pertama atau terakhir tidak 0 , maka banyak kupon yang dapat dibuat adalah ....
"""
        bc_final_answer = """
600
"""

        bc_answer = """
Banyaknya kupon yang dapat dibuat adalah \( 5^{4}-5^{2}=625-25=600 \) 
"""

        bc_response = """
[NEW_QUESTION]:
Sebuah komite karnaval akan menyiapkan tiket dengan nomor yang terdiri dari 5 angka. Angka-angka yang digunakan untuk membentuk nomor tiket adalah \( 0, 2, 4, 6, \) dan \( 8 \). Jika angka pertama atau angka terakhir tidak boleh 0, maka karnaval tersebut dapat membuat [FILL] tiket

[NEW_ANSWER]:
Pemahaman Soal dan Langkah Pendekatan:
Soal ini meminta untuk menghitung jumlah kombinasi nomor tiket yang mungkin, dengan menggunakan lima angka: 0, 2, 4, 6, dan 8. Kunci dari soal ini adalah bahwa angka pertama atau angka terakhir tiket tidak boleh 0 untuk memastikannya valid sebagai nomor tiket. 

Langkah 1 - Menghitung jumlah kasus dimana angka pertama bukan 0:
Jika angka pertama bukan 0, ada 4 pilihan (2, 4, 6, 8), dan untuk setiap angka setelahnya, termasuk angka terakhir, ada 5 kemungkinan pilihan (0, 2, 4, 6, 8).
Jadi, \(4 \times 5^4 = 4 \times 625 = 2500\) tiket dapat dibuat ketika angka pertama bukan 0.

Langkah 2 - Menghitung jumlah kasus dimana angka terakhir bukan 0 dan angka pertama adalah 0:
Di sini, angka terakhir tidak boleh 0 tetapi angka pertama bisa 0. Jadi, angka terakhir punya 4 pilihan (2, 4, 6, 8) dan angka di tengah (kedua, ketiga, keempat) masing-masing memiliki 5 kemungkinan.
Jadi, \(5^3 \times 4 = 125 \times 4 = 500\) tiket dapat dibuat ketika angka terakhir bukan 0 dan angka pertama adalah 0.

Langkah 3 - Menghindari duplikasi dalam perhitungan ketika angka berakhir dan angka pertama keduanya bukan 0:
Sebelumnya telah menghitung semua kasus valid di kedua skenario tanpa menghilangkan kasus dimana angka terakhir dan angka pertama keduanya bukan 0, yang tersebar dalam kedua perhitungan itu.
Kasus ini sudah dihitung dalam Langkah 1 sehingga tidak perlu dikurangkan lagi dari total.

Kesimpulan:
Jumlah total tiket yang dapat dibuat adalah 2500 (angka pertama bukan 0) + 500 (angka terakhir bukan 0 dan pertama adalah 0) = 3000 tiket.

[NEW_FINAL_ANSWER]:
3000
"""

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
                                "role": "user", "content": "[ANSWER]: " + bc_answer
                            },
                            {
                                "role": "user", "content": "[FINAL_ANSWER]: " + bc_final_answer
                            },{
                                "role": "assistant", "content": "[OUTPUT]: " + bc_response
                            },
                            {
                "role": "system", "content": task
            },
            {
                                "role": "user", "content": "[QUESTION]: " + question
                            },
                            {
                                "role": "user", "content": "[ANSWER]: " + explanation
                            },
                            {
                                "role": "user", "content": "[FINAL_ANSWER]: " + answer
                            },
                            
            
        ]
    )

        result = complation.choices[0].message.content

        return create_question_isian.build_regex(result)
