from openai import OpenAI
from service.call_env import env_data
import re


class create_answer_tf() : 
    def run(question, choice, description):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = f"""Anda adalah sebuah sistem penjawab soal berbahasa indonesia dengan jenis benar salah
URUTAN INPUT : [QUESTION], [CHOICE], [DESCRIPTION]
URUTAN OUTPUT : [FINAL_ANSWER]

Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
Pilihan jawaban dengan label [CHOICE] yang berisikan pilihan jawaban
Pembahasan jawaban dengan label [DESCRIPTION] dengan label TRUE/FALSE

Anda ditugaskan untuk membuat jawaban berdasarkan soal yang telah diberikan dengan cara memahami [QUESTION], [CHOICE], dan [DESCRIPTION]
[FINAL_ANSWER] menjelaskan secara rinci mengenai argumen-argumen yang ada pada [CHOICE] mengapa argumen tersebut dapat bernilai TRUE atau FALSE
Format dari [FINAL_ANSWER] untuk setiap argumen-argumen yang ada pada [CHOICE] adalah 
Argumen - TRUE/FALSE
Explanation : [penjelasan argumen] 

contoh : 
Rising ocean temperatures will reduce the frequency of hurricanes and typhoons. - FALSE
Explanation: Naiknya suhu laut sebenarnya meningkatkan kekerapan dan intensitas badai seperti angin topan dan hurricane karena menyediakan lebih banyak energi dan uap air.


Contoh Output : 
[FINAL_ANSWER]:
1. Kantong plastik dapat bertahan hingga 500 tahun di lingkungan - TRUE
Explanation: Kantong plastik terbuat dari polimer yang sangat tahan lama dan tidak mudah terurai secara biologis, sehingga memungkinkan mereka bertahan di lingkungan hingga berabad-abad.

2. Penggunaan kembali kantong plastik tidak mempengaruhi kesehatan manusia - FALSE
Explanation: Penggunaan kembali kantong plastik, terutama yang sudah tua dan mulai terurai, dapat melepaskan zat kimia seperti Bisphenol A (BPA), yang diketahui memberikan efek negatif pada kesehatan, termasuk pengaruh pada hormon dan potensi gangguan kesehatan serius lainnya.

3. Kebijakan larangan penggunaan kantong plastik telah efektif mengurangi polusi plastik di seluruh dunia - FALSE
Explanation: Meskipun telah ada upaya dan kebijakan larangan penggunaan kantong plastik di beberapa negara, penggunaannya masih tinggi di beberapa bagian dunia dan efektivitas kebijakan ini dalam mengurangi polusi secara global masih terbatas.
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