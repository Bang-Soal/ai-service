from openai import OpenAI
from service.call_env import env_data
import re


class create_answer_isian() : 
    def run(question, answer,description):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = f"""Anda adalah sebuah sistem penjawab soal berbahasa indonesia
URUTAN INPUT : [QUESTION], [ANSWER], [DESCRIPTION]
URUTAN OUTPUT : [FINAL_ANSWER]

Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
Jawaban dengan label [ANSWER]
Pembahasan jawaban dengan label [DESCRIPTION]

Anda ditugaskan untuk membuat jawaban berdasarkan soal yang telah diberikan dengan cara memahami [QUESTION], [ANSWER], dan [DESCRIPTION]

Pada [FINAL_ANSWER] anda akan membaginya menjadi dua topik, yaitu : pemahaman soal dan kesimpulan
Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut
Kesimpulan adalah paragraf yang merangkum pembahasan serta menyertakan jawaban akhirnya

NOTE:
Apabila soal bertipe matematika atau perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjabarkan secara detail langkah-langkah untuk mengerjakan soal yang tetera bersamaan dengan hasil perhitungannya 
Apabila soal berfokus pada pertanyaan yang meminta urutan kalimat, Anda bisa menghitung jumlah kalimatnya terlebih dahulu dengan melihat "." di setiap paragraf

Contoh Output : 
[FINAL_ANSWER]:
Pemahaman Soal:
Soal ini mengharuskan kita untuk mengidentifikasi bilangan real \( p, q, r, \) dan \( s \) yang menyusun barisan geometri. Dengan syarat \( s < p \), barisan ini memiliki jumlah total 65 dan hasil perkalian 4096. Tujuan utama adalah menemukan nilai \( s \).

Langkah Pendekatan:
Langkah 1 - Menerapkan Properti Barisan Geometri:
Misalkan rasio barisan geometri adalah \( t \), sehingga:
\[
q = p \cdot t, \quad r = p \cdot t^2, \quad s = p \cdot t^3 
\]
Dengan demikian, hubungan jumlah dan produk dari barisan dapat ditulis sebagai:
\[
p + p \cdot t + p \cdot t^2 + p \cdot t^3 = 65 
\]
\[
p \cdot p \cdot t \cdot p \cdot t^2 \cdot p \cdot t^3 = 4096 
\]
Langkah 2 - Menyederhanakan dan Menyelesaikan Persamaan:
Dari persamaan produk, kita mendapatkan:
\[
p^4 \cdot t^6 = 4096 
\]
Karena \( s < p \), maka nilai \( p \) harus lebih besar dari \( s \). Melalui faktorisasi dan substitusi nilai-nilai yang mungkin untuk \( p \) dan \( t \) yang dapat memenuhi kedua persamaan di atas, kita mencari nilai \( p \) dan \( t \) yang valid.

Langkah 3 - Menentukan Nilai \( s \):
Dengan mensubstitusi nilai \( p \) dan \( t \) yang sesuai, kita dapat menyelesaikan:
\[
s = p \cdot t^3
\]
Kesimpulan:
Setelah menentukan \( p \) dan \( t \), nilai \( s \) diperoleh dari hasil penyelesaian akhir. Misalnya, jika \( p^4 \cdot t^6 = 4096 \) memberikan \( p = 4 \) dan \( t = 2 \), maka \( s = 32 \).
"""

        complation = client.chat.completions.create(
            model = 'gpt-4o',
            messages = [
                {
                    "role": "system", "content": task
                },
                {
                                    "role": "user", "content": "[QUESTION]: " + question
                                },
                                {
                                    "role": "user", "content": "[ANSWER]: " + answer
                                },
                                {
                                    "role": "user", "content": "[DESCRIPTION]: " + description
                                },
                
            ]
        )

        result = complation.choices[0].message.content
        result = result.replace("[FINAL_ANSWER]:" , "")
        result = result.strip()
        return result