from openai import OpenAI
from service.call_env import env_data
import re


class create_answer() : 
    def run(question, choice):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """
        Anda adalah sebuah sistem penjawab soal berbahasa indonesia
URUTAN INPUT : [QUESTION], [CHOICE]
URUTAN OUTPUT : [ANSWER]

Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
Pilihan jawaban dengan label [CHOICE] yang berisikan lima pilihan jawaban (A,B,C,D,E)
Anda ditugaskan untuk membuat jawaban berdasarkan soal yang telah diberikan

Pada [ANSWER] anda akan membaginya menjadi 3 topik, yaitu : pemahaman soal, pembahasan pilihan jawaban, dan kesimpulan
Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [NEW_QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut
Pembahasan pilihan jawaban adalah paragraf yang menjelaskan masing-masing jawaban (A,B,C,D,E) yang diberikan dengan bantuan analisis yang telah anda lakukan dalam memahami soal sehingga anda menemukan satu jawaban yang paling sesuai dan pemabahasan setiap jawaban-jawaban yang ada
Kesimpulan adalah paragraf yang menjelaskan jawaban akhir yang dipilih dengan memilih salah satu dari choice yang disediakan pada [NEW_CHOICE]

NOTE:
Apabila soal bertipe matematika atau perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjabarkan secara detail langkah-langkah untuk mengerjakan soal yang tetera bersamaan dengan hasil perhitungannya 
Apabila soal berfokus pada pertanyaan yang meminta urutan kalimat, Anda bisa menghitung jumlah kalimatnya terlebih dahulu dengan melihat "." di setiap paragraf
        """
        bc_question2 = """
Beberapa kata yang digunakan pada daerah \( x \) menggunakan bahasa yang unik dengan pola sebagai berikut.
"Gitar akustik" diterjemahkan menjadi "kusan tara"
"Musik elektrik" diterjemahkan menjadi "neto masik"
"Musik akustik" diterjemahkan menjadi "kusan masik"

Suatu toko di daerah tersebut menjual instrument musik. Jika seseorang ingin memesan "gitar elektrik" di toko tersebut, bagaimana ia mengucapkannya? 
dmdndk lexnrwd gdul lqgrqhuld? 
"""
        bc_choice2 = """
A. Neto kusan
B. Kusan masik
C. Tara kusan
D. Neto tara
E. Tara neto
"""

        bc_answer2 = """
Pemahaman soal:
Untuk mengetahui bagaimana menyebut "gitar elektrik" dalam bahasa unik daerah ini, kita bisa menganalisis pola terjemahan yang diberikan dalam soal. Berikut ini analisisnya:

1. "Gitar akustik" diterjemahkan menjadi "kusan tara":
   - "Gitar" diterjemahkan menjadi "tara"
   - "Akustik" diterjemahkan menjadi "kusan"
   
2. "Musik elektrik" diterjemahkan menjadi "neto masik":
   - "Musik" diterjemahkan menjadi "masik"
   - "Elektrik" diterjemahkan menjadi "neto"
   
3. "Musik akustik" diterjemahkan menjadi "kusan masik":
   - Kita sudah tahu bahwa "akustik" diterjemahkan menjadi "kusan" dan "musik" menjadi "masik".

Mencari Terjemahan "Gitar Elektrik":
- Kita sudah tahu bahwa "gitar" adalah "tara".
- "Elektrik" dalam "musik elektrik" adalah "neto".

Jadi, "gitar" + "elektrik" akan menjadi "tara" + "neto".

Namun, karena dalam bahasa daerah tersebut kata sifat tampaknya datang sebelum kata benda (dilihat dari posisi "neto" sebelum "masik" dan "kusan" sebelum "tara" atau "masik"), maka kata "elektrik" seharusnya datang sebelum kata "gitar" saat diterjemahkan.

Jadi, "gitar elektrik" dalam bahasa daerah itu adalah "neto tara", bukan "tara neto".

Pembahasan pilihan jawaban:
Dengan demikian, arti dari setiap jawaban yang ada adalah 
A. Neto kusan = elektrik musik
B. Kusan masik = musik akustik
C. Tara kusan = elektrik akustik
D. Neto tara = gitar elektrik
E. Tara neto = elektrik gitar

Kesimpulan:
Dengan demikian jawaban yang benar adalah D. Neto tara
"""

        complation = client.chat.completions.create(
            model = 'gpt-4o',
            messages = [
                {
                    "role": "system", "content": task
                },
                {
                                    "role": "user", "content": "[QUESTION]: " + bc_question2
                                },
                                {
                                    "role": "user", "content": "[CHOICE]: " + bc_choice2
                                },
                                {
                                    "role": "assistant", "content": "[ANSWER]: " + bc_answer2
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
                
            ]
        )

        result = complation.choices[0].message.content
        result = result.replace("[ANSWER]:" , "")
        result = result.strip()
        return result