from openai import OpenAI
from service.call_env import env_data
import re


class create_material() : 
    def run(topic):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """Kamu adalah sebuah sistem yang dapat membuat sebuah pembahasan materi dari tema yang ditentukan [TOPIC] untuk mengikuti sebuah Ujian SMA di Indonesia (UTBK) berdasarkan pemahaman yang kamu miliki
        Tujuan dari pembahasan materi ini akan digunakan oleh siswa SMA dalam belajar untuk membantu mereka memahami lebih detail terkait tema materi yang diberikan

            Input : [TOPIC] yang mana merupakan sebuah tema materi yang akan dibuat ringkasannya
            Output : [RESULT]
            Langkah-langkah pembuatan [RESULT] 
            1. Anda akan menuliskan [TOPIC] yang diberikan
            2. Anda akan membuat ringkasan materi sesuai [TOPIC] yang diberikan
            3. Apabila materi ini memiliki banyak submateri, anda perlu menjelaskannya juga dalam [RESULT] nanti
            4. Jika materi mengandung rumus-rumus yang umum digunakan pada materi tersebut, anda perlu menulis juga rumus dan bagaimana kasus penggunaan rumus tersebut
            3. Anda akan membuat ringkasan tips and tricks yang bersersuai dengan [TOPIC] yang diberikan
            4. Anda akan membuat contoh soal beserta jawaban yang sesuai dengan [TOPIC] yang diberikan

            Anda tidak perlu menuliskan kembali langkah-langkah pembuatannya. 
        """

        response = client.chat.completions.create(
        model="gpt-4o",
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        messages= [{"role": "system", "content": task},{"role": "user", "content": "[TOPIC]: " + topic }]
        )
        return response.choices[0].message.content