from openai import OpenAI
from service.call_env import env_data


class paraphrase_question() : 
    def run(question, choice, content, raw_answer):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        
        if len(content) == 0 : 
            task_template = """
    Anda adalah sebuah pengajar yang ditugaskan untuk menjawab soal-soal yang diberikan
    Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
    Anda akan diberikan sebuah pertanyaan dengan label [QUESTION]
    Pilihan jawaban dengan label [CHOICE] yang berisikan lima pilihan jawaban (A,B,C,D,E)
    Penjelasan jawaban dengan label [RAW_ANSWER]
    Anda ditugaskan untuk menjawab soal tersebut dengan memahami ketiga aspek tersebut : [QUESTION], [CHOICE], dan [RAW_ANSWER] untuk menghasilkan sebuah parafrase jawaban dengan label [PARAPHRASED_ANSWER]
    Anda diharapkan dapat menjelaskan secara detail alasan mengenai mengapa jawaban tersebut dipilih di antara pilihan jawaban-jawaban lainnya dan juga alasan jawaban dari setiap jawaban
    Pada [PARAPHRASED_ANSWER] anda akan membaginya menjadi 3 topik, yaitu : pemahaman soal, pembahasan pilihan jawaban, dan kesimpulan
    Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut
    Pembahasan pilihan jawaban adalah paragraf yang menjelaskan masing-masing jawaban (A,B,C,D,E) yang diberikan dengan bantuan analisis yang telah anda lakukan dalam memahami soal sehingga anda menemukan satu jawaban yang paling sesuai
    Kesimpulan adalah paragraf yang menjelaskan jawaban akhir yang dipilih dengan memilihj salah satu dari choice yang disediakan
    NOTE:
    Pada jawaban [PARAPHRASED_ANSWER] tidak perlu menulis kembali [QUESTION], [CHOICE], dan [RAW_ANSWER] karena ketiga aspek tersebut bersifat rahasia dan tidak perlu diketahui user apabila jawaban diambil dan dimodifikasi dari [RAW_ANSWER]. Dengan demikian, jawaban yang dihasilkan ini adalah murni jawaban anda sendiri
    Apabila soal berbahasa inggris, tetap tampilkan pilihan jawaban dengan bahasa inggris
    Apabila soal bertipe matematika dan perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjawabarkan langkah-langkah pengerjaan secara detail dengan format Latex tanpa perlu mengevaluasi pilihan jawaban satu-satu yang ada pada [CHOICE]
    """
            question_template = r"""
    Beberapa kata yang digunakan pada daerah \( x \) menggunakan bahasa yang unik dengan pola sebagai berikut.
    "Gitar akustik" diterjemahkan menjadi "kusan tara"
    "Musik elektrik" diterjemahkan menjadi "neto masik"
    "Musik akustik" diterjemahkan menjadi "kusan masik"

    Suatu toko di daerah tersebut menjual instrument musik. Jika seseorang ingin memesan "gitar elektrik" di toko tersebut, bagaimana ia mengucapkannya? 
    dmdndk lexnrwd gdul lqgrqhuld? 
    """
            choice_template = r"""
    A. Neto kusan
    B. Kusan masik
    C. Tara kusan
    D. Neto tara
    E. Tara neto
    """
            raw_answer_template = r"""
    "Gitar elektrik" mempunyai pola yang mirip dengan "gitar akustik". Kata
    "gitar" berarti "tara";
    "akustik" berarti "kusan";
    "musik" berarti "masik";
    "elektrik" berarti "neto".
    Dengan demikian, "gitar elektrik" menjadi "neto tara" ("elektrik" dulu kemudian "gitar"). 
    """

            paraphrased_template = r"""
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

            model = 'gpt-4o'

            messages = [
                            {
                                "role": "system", "content": task_template
                            },
                            {
                                "role": "user", "content": "[QUESTION]: " + question_template
                            },
                            {
                                "role": "user", "content": "[CHOICE]: " + choice_template
                            },
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + raw_answer_template 
                            },
                            {
                                "role": "assistant", "content": "[PARAPHRASED_ANSWER]: " + paraphrased_template
                            },


                            {
                                "role": "system", "content": task_template
                            },
                            {
                                "role": "user", "content": "[QUESTION]: " + question
                            },
                            {
                                "role": "user", "content": "[CHOICE]: " + choice
                            },
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + raw_answer
                            },
                        
                        ]


        else : 
            task_template = """
    Anda adalah sebuah pengajar yang ditugaskan untuk menjawab soal-soal yang diberikan
    Soal-soal ini dapat meliputi soal penalaran umum, matematika, bacaan bahasa indonesia, atau bacaan bahasa inggris
    Anda akan diberikan sebuah pertanyaan dengan label [QUESTION] yang diikuti dengan gambar. Gunakanlah gambar ini untuk memahami pertanyaan dan menjawab soal
    Pilihan jawaban dengan label [CHOICE] yang berisikan lima pilihan jawaban (A,B,C,D,E)
    Penjelasan jawaban dengan label [RAW_ANSWER]
    Anda ditugaskan untuk menjawab soal tersebut dengan memahami ketiga aspek tersebut : [QUESTION], [CHOICE], dan [RAW_ANSWER] untuk menghasilkan sebuah parafrase jawaban dengan label [PARAPHRASED_ANSWER]
    Anda diharapkan dapat menjelaskan secara detail alasan mengenai mengapa jawaban tersebut dipilih di antara pilihan jawaban-jawaban lainnya dan juga alasan jawaban dari setiap jawaban
    Pada [PARAPHRASED_ANSWER] anda akan membaginya menjadi 3 topik, yaitu : pemahaman soal, pembahasan pilihan jawaban, dan kesimpulan
    Pemahaman soal adalah paragraf yang menjelaskan maksud dan tujuan soal yang akan dibahas dengan cara menganalisis tujuan [QUESTION] yang diberikan. Selain itu, pada bagian ini anda mengambil poin-poin penting dari soal yang diberikan untuk membuat analisis anda terhadap soal tersebut
    Pembahasan pilihan jawaban adalah paragraf yang menjelaskan masing-masing jawaban (A,B,C,D,E) yang diberikan dengan bantuan analisis yang telah anda lakukan dalam memahami soal sehingga anda menemukan satu jawaban yang paling sesuai
    Kesimpulan adalah paragraf yang menjelaskan jawaban akhir yang dipilih dengan memilihj salah satu dari choice yang disediakan
    NOTE:
    Pada jawaban [PARAPHRASED_ANSWER] tidak perlu menulis kembali [QUESTION], [CHOICE], dan [RAW_ANSWER] karena ketiga aspek tersebut bersifat rahasia dan tidak perlu diketahui user apabila jawaban diambil dan dimodifikasi dari [RAW_ANSWER]. Dengan demikian, jawaban yang dihasilkan ini adalah murni jawaban anda sendiri
    Apabila soal berbahasa inggris, tetap tampilkan pilihan jawaban dengan bahasa inggris
    Apabila soal bertipe matematika dan perhitungan, diharapkan pada bagian pemahaman soal anda dapat menjawabarkan langkah-langkah pengerjaan secara detail dengan format Latex tanpa perlu mengevaluasi pilihan jawaban satu-satu yang ada pada [CHOICE]
    """
            question_template = "Sebuah tempat air terbuat dari plat baja yang berbentuk separuh tabung (sesuai gambar). Bagian atas terbuka dan kapasitasnya \( 125 \pi \) liter. Agar bahan pembuatannya sehemat mungkin, nilai \( h=\ldots \) meter."
            choice_template = r"""
    A. 1
    B. 5
    C. 10
    D. 50
    E. 100
    """
            raw_answer_template = r"""
    Misal, \( V \) menyatakan volume tempat air dan \( L \) menyatakan luas permukaan tempat air maka kita dapat
    \[
    125=V=\frac{1}{2} \pi r^{2} h
    \]

    Sehingga,
    \[
    r=\sqrt{\frac{250}{h}}
    \]

    Luas permukaan tempat air
    \[
    \begin{aligned}
    L=\frac{1}{2}\left(2 \pi r^{2}+2 \pi r h\right) & \\
    & =\pi \frac{250}{h}+\pi \sqrt{\frac{250}{h}} \cdot h \\
    & =\frac{250 \pi}{h}+\pi \sqrt{250 h}
    \end{aligned}
    \]

    Syarat agar \( L \) minimum adalah
    \[
    L^{\prime}=0
    \]

    Sehingga,
    \[
    \begin{aligned}
    L^{\prime}=-\frac{250 \pi}{h^{2}}+\frac{\pi \sqrt{250}}{2 \sqrt{h}} & =0 \\
    -500 \pi+\pi \sqrt{250} h^{\frac{3}{2}} & =0 \\
    \sqrt{250} h^{\frac{3}{2}} & =500 \\
    h^{\frac{3}{2}} & =2 \sqrt{250} \\
    h & =10
    \end{aligned}
    \]

    Jadi, \( h=10 \mathrm{dm}=1 \) meter
    """
            paraphrased_template = r"""
    Pemahaman soal:
    Pertama-tama, kita diberitahu bahwa volume tempat air adalah \( 125 \pi \) liter. Kita tahu bahwa tempat air tersebut berbentuk separuh tabung. Oleh karena itu, kita dapat menulis hubungan volume (\( V \)) tempat air dengan jari-jari (\( r \)) dan tinggi (\( h \)) sebagai berikut:

    \[
    V = \frac{1}{2} \pi r^{2} h
    \]

    Kita substitusi nilai \( V \) dengan \( 125 \pi \):

    \[
    125 \pi = \frac{1}{2} \pi r^{2} h
    \]

    Untuk memudahkan, kita bagi kedua sisi dengan \( \pi \) dan kalikan dengan 2, kita peroleh:

    \[
    250 = r^{2} h
    \]

    Sekarang, kita selesaikan persamaan tersebut untuk \( r \):

    \[
    r = \sqrt{\frac{250}{h}}
    \]

    Selanjutnya, kita mencari luas permukaan (\( L \)) dari tempat air. Luas permukaan terdiri dari separuh lingkaran bagian bawah dan tembok tabung, sehingga kita dapat menulisnya sebagai:

    \[
    L = \frac{1}{2} (2 \pi r^{2}) + \pi r h = \pi r^{2} + \pi r h
    \]

    Kemudian, kita substitusi \( r \) dengan nilai yang telah kita temukan sebelumnya:

    \[
    L=\frac{250 \pi}{h} + \pi \sqrt{\frac{250}{h}} h
    \]

    Agar luas \( L \) minimum, kita perlu mencari nilai \( h \) yang membuat turunan pertama \( L \) terhadap \( h \) sama dengan nol (\( L' = 0 \)):

    \[
    L' = -\frac{250 \pi}{h^{2}} + \frac{\pi \sqrt{250}}{2 \sqrt{h}} = 0
    \]

    Kemudian, kita selesaikan persamaan tersebut untuk \( h \):

    \[
    -\frac{500 \pi}{h^{2}} + \pi \sqrt{250} h^{\frac{3}{2}} = 0
    \]
    \[
    \pi \sqrt{250} h^{\frac{3}{2}} = 500 \pi
    \]
    \[
    h^{\frac{3}{2}} = 2 \sqrt{250}
    \]
    \[
    h = 10 \text{ (dalam desimeter)}
    \]

    Karena 10 desimeter sama dengan 1 meter, maka kita peroleh nilai \( h \) yaitu:

    \[
    h = 10 \text{ dm} = 1 \text{ meter}
    \]

    Pembahasan pilihan jawaban:
    A. 1, sesuai dengan hasil perhitungan yang telah dilakukan
    B. 5, tidak sesuai dengan hasil perhitungan yang telah dilakukan
    C. 10, tidak sesuai dengan hasil perhitungan yang telah dilakukan
    D. 50, tidak sesuai dengan hasil perhitungan yang telah dilakukan
    E. 100 , tidak sesuai dengan hasil perhitungan yang telah dilakukan

    Kesimpulan:
    Dengan demikian, jawaban yang sesuai adalah A. 1
    """
            content_template = "https://drive.usercontent.google.com/download?id=1csGErPlT5nCBQDZE0_XTCSD4DP1vhP16"
            content_text_template = "Gambar ini digunakan untuk memperjelas soal yang diberikan"

            model = "gpt-4o"
            messages = [
                            {
                                "role": "system", "content": task_template
                            },
                            {
                                "role": "user", "content": "[QUESTION]: " + question_template
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": content_text_template},
                                    {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": content_template,
                                        "detail": "high"
                                    },
                                    },
                                ],
                            },
                            {
                                "role": "user", "content": "[CHOICE]: " + choice_template
                            },
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + raw_answer_template 
                            },
                            {
                                "role": "assistant", "content": "[PARAPHRASED_ANSWER]: " + paraphrased_template
                            },


                            {
                                "role": "system", "content": task_template
                            },
                            {
                                "role": "user", "content": "[QUESTION]: " + question
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": content_text_template},
                                    {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": content,
                                        "detail": "high"
                                    },
                                    },
                                ],
                            },
                            {
                                "role": "user", "content": "[CHOICE]: " + choice
                            },
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + raw_answer
                            },
                        
                        ]
        response = client.chat.completions.create(
            model = model,
            messages = messages
        )

        result = response.choices[0].message.content
        result = result.split('[PARAPHRASED_ANSWER]:')[1]
        result = result.replace("[RAW_ANSWER]" , "pembahasan ini")
        return result