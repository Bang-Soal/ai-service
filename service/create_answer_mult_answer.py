from openai import OpenAI
from service.call_env import env_data
import re


class create_answer_mult_answer() : 
    def run(question, choice, answer, description):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = f"""Anda adalah sebuah sistem penjawab soal berbahasa indonesia dengan jenis soal multiple answer. Dengan demikian satu soal bisa memiliki lebih dari 1 pilihan jawaban
URUTAN INPUT : [QUESTION], [CHOICE], [ANSWER], [DESCRIPTION]
URUTAN OUTPUT : [FINAL_ANSWER]

Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
Pilihan jawaban dengan label [CHOICE] yang berisikan lima pilihan jawaban (A,B,C,D,E)
Jawaban dengan label [ANSWER]
Pembahasan jawaban dengan label [DESCRIPTION]

Anda ditugaskan untuk membuat jawaban berdasarkan soal yang telah diberikan dengan cara memahami [QUESTION], [CHOICE], [ANSWER], dan [DESCRIPTION]

Pada [FINAL_ANSWER] anda akan membaginya menjadi 3 topik, yaitu : pemahaman soal, pembahasan pilihan jawaban, dan kesimpulan
Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut dengan menggunakan bantuan penjelasan yanga ada pada [DESCRIPTION]
Pembahasan pilihan jawaban adalah paragraf yang menjelaskan masing-masing jawaban (A,B,C,D,E) yang diberikan dengan bantuan analisis yang telah anda lakukan dalam memahami soal sehingga anda menemukan satu jawaban yang paling sesuai dan pembahasan setiap jawaban-jawaban yang ada. Selain itu, beri juga penjelasan mengapa setiap pilihan ini benar atau salah
Kesimpulan adalah paragraf yang menjelaskan jawaban akhir yang dipilih dengan memilih jawaban yang benar dari choice yang disediakan pada [CHOICE]

NOTE:
Apabila soal bertipe matematika atau perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjabarkan secara detail langkah-langkah untuk mengerjakan soal yang tetera bersamaan dengan hasil perhitungannya pada [QUESTION], tidak perlu menjelaskan satu-satu jawaban yang ada pada [CHOICE]
Apabila soal berbahasa inggris, wajib menggunakan bahasa inggris untuk membuat [QUESTION] dan [CHOICE], tetapi untuk penjelasan yang ada pada [FINAL_ANSWER] wajib menggunakan bahasa indonesia.

Contoh Output : 
[FINAL_ANSWER]:
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
                            "role": "user", "content": "[ANSWER]: " + answer
                        },
                        {
                            "role": "user", "content": "[DESCRIPTION]: " + description
                        }]
        )

        result = complation.choices[0].message.content
        result = result.replace("[FINAL_ANSWER]:" , "")
        result = result.strip()
        return result