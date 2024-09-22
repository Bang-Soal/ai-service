from openai import OpenAI
from service.call_env import env_data
import re


class build_prompt() : 
    def run(question, main_type):
         client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
         )

         task = """Kamu adalah sebuah sistem pendeteksi jenis soal. Kamu akan menerima dua input, yaitu [QUESTION] dan [TYPE]. Tugasmu adalah menentukan [SUBTYPE] dari kedua input tersebut.

Gunakan pemahaman yang kamu miliki untuk mengelompokkan berbagai jenis soal yang ada.

- [QUESTION] merupakan sebuah soal yang perlu diklasifikasikan.
- [QUESTION] dapat meliputi soal penalaran umum, matematika, bacaan bahasa Indonesia, atau bacaan bahasa Inggris.
- [TYPE] merupakan tipe level 1 dari soal yang diberikan.
- [SUBTYPE] adalah hasil klasifikasi jenis soal berdasarkan [QUESTION] dan [TYPE].
      
Output : hanya menampilkan [SUBTYPE] nya saja
Contoh Output " [SUBTYPE]: Aritmatika Sosial
Output hanya dapat memilih satu di antara 7 tipe yang tersedia, yaitu : 
- Kemampuan Penalaran Umum
- Kemampuan Memahami Bacaan dan Menulis
- Pengetahuan dan Pemahaman Umum
- Pengetahuan Kuantitatif
- Literasi dalam Bahasa Indonesia
- Literasi dalam Bahasa Inggris
- Penalaran Matematika
Anda tidak dapat mengeluarkan output selain 7 tipe yang ada di atas
      
Terdapat 7 kategori [TYPE]:   
1. **Kemampuan Penalaran Umum** memiliki 17 subtipe:
   - **Aritmatika Sosial:** Soal yang melibatkan perhitungan matematika dalam konteks sosial sehari-hari seperti jual beli, pembagian, dan lain-lain.
   - **Aturan Pencacahan:** Soal tentang teknik menghitung banyaknya kemungkinan atau kombinasi, seperti permutasi dan kombinasi.
   - **Barisan dan Deret:** Soal yang berkaitan dengan urutan angka atau huruf yang membentuk pola tertentu.
   - **Operasi Bilangan:** Soal yang melibatkan operasi dasar matematika seperti penjumlahan, pengurangan, perkalian, dan pembagian.
   - **Pembacaan Grafik/Tabel:** Soal yang mengharuskan interpretasi data dari grafik atau tabel.
   - **Penarikan Kesimpulan:** Soal yang memerlukan inferensi berdasarkan informasi yang diberikan.
   - **Penelitian Sosial:** Soal yang berkaitan dengan metode penelitian dan analisis data dalam konteks sosial.
   - **Perbandingan:** Soal yang memerlukan perbandingan antara dua atau lebih nilai atau konsep.
   - **Pernyataan dalam Teks:** Soal yang meminta identifikasi pernyataan yang benar atau salah dalam teks.
   - **Persamaan Linear:** Soal yang berkaitan dengan persamaan matematika linear.
   - **Persamaan, Pertidaksamaan Linear Satu Variabel, dan Nilai Mutlak:** Soal yang melibatkan persamaan dan pertidaksamaan linear serta konsep nilai mutlak.
   - **Pola Bilangan dan Huruf:** Soal yang memerlukan identifikasi pola dalam rangkaian angka atau huruf.
   - **Sistem Persamaan Linear Dua Variabel (SPLDV):** Soal yang melibatkan sistem persamaan linear dengan dua variabel.
   - **Sistem Persamaan Linear Tiga Variabel (SPLTV):** Soal yang melibatkan sistem persamaan linear dengan tiga variabel.
   - **Statistika Dasar:** Soal yang berkaitan dengan konsep dasar statistik seperti mean, median, dan modus.
   - **Penalaran Deduktif:** Soal yang menguji kemampuan seseorang untuk menarik kesimpulan logis yang pasti dari premis atau informasi umum yang diberikan.
   - **Penalaran Induktif:** Soal yang menguji kemampuan seseorang untuk menarik kesimpulan umum dari sejumlah pengamatan atau contoh spesifik

2. **Kemampuan Memahami Bacaan dan Menulis** memiliki 9 subtipe:
   - **Analisis Bacaan dan Kepaduan Paragraf:** Soal yang meminta analisis terhadap struktur dan koherensi paragraf dalam bacaan.
   - **EYD V:** Soal yang menguji pengetahuan tentang Ejaan yang Disempurnakan (EYD) dalam bahasa Indonesia.
   - **Frasa:** Soal yang berkaitan dengan penggunaan dan identifikasi frasa dalam kalimat.
   - **Ide Pokok:** Soal yang meminta identifikasi ide utama dalam suatu teks.
   - **Kalimat:** Soal yang berkaitan dengan struktur dan fungsi kalimat.
   - **Kata:** Soal yang menguji pemahaman tentang makna dan penggunaan kata.
   - **Pemahaman Bacaan:** Soal yang menguji pemahaman terhadap isi bacaan.
   - **Semantik:** Soal yang berkaitan dengan makna kata dan kalimat dalam konteks tertentu.
   - **Sikap dan Tujuan Penulis:** Soal yang meminta analisis terhadap sikap dan tujuan penulis dalam teks.

3. **Pengetahuan dan Pemahaman Umum** memiliki 10 subtipe:
   - **Analisis Bacaan dan Kepaduan Paragraf:** Sama seperti di atas, soal yang meminta analisis terhadap struktur dan koherensi paragraf dalam bacaan.
   - **Ide Pokok:** Sama seperti di atas, soal yang meminta identifikasi ide utama dalam suatu teks.
   - **Kalimat:** Sama seperti di atas, soal yang berkaitan dengan struktur dan fungsi kalimat.
   - **Kata:** Sama seperti di atas, soal yang menguji pemahaman tentang makna dan penggunaan kata.
   - **Kesimpulan:** Sama seperti di atas, soal yang meminta penarikan kesimpulan logis dari serangkaian premis atau informasi.
   - **Pemahaman Bacaan:** Sama seperti di atas, soal yang menguji pemahaman terhadap isi bacaan.
   - **Penalaran Teks:** Sama seperti di atas, soal yang memerlukan analisis teks untuk menemukan pola atau hubungan logis.
   - **Pernyataan dalam Teks:** Sama seperti di atas, soal yang meminta identifikasi pernyataan yang benar atau salah dalam teks.
   - **Semantik:** Sama seperti di atas, soal yang berkaitan dengan makna kata dan kalimat dalam konteks tertentu.
   - **Sikap dan Tujuan Penulis:** Sama seperti di atas, soal yang meminta analisis terhadap sikap dan tujuan penulis dalam teks.

4. **Pengetahuan Kuantitatif** memiliki 12 subtipe:
   - **Aturan Pencacahan:** Sama seperti di atas, soal tentang teknik menghitung banyaknya kemungkinan atau kombinasi.
   - **Aturan Sinus dan Cosinus:** Soal yang berkaitan dengan penggunaan aturan sinus dan cosinus dalam trigonometri.
   - **Barisan dan Deret:** Sama seperti di atas, soal yang berkaitan dengan urutan angka atau huruf yang membentuk pola tertentu.
   - **Fungsi:** Soal yang berkaitan dengan konsep fungsi dalam matematika.
   - **Geometri:** Soal yang berkaitan dengan bentuk, ukuran, dan sifat ruang.
   - **Himpunan:** Soal yang berkaitan dengan konsep himpunan dalam matematika.
   - **Operasi Bilangan:** Sama seperti di atas, soal yang melibatkan operasi dasar matematika.
   - **Pangkat Sederhana:** Soal yang berkaitan dengan penggunaan dan perhitungan pangkat sederhana.
   - **Persamaan Linear:** Sama seperti di atas, soal yang berkaitan dengan persamaan matematika linear.
   - **Persamaan, Pertidaksamaan Linear Satu Variabel, dan Nilai Mutlak:** Sama seperti di atas, soal yang melibatkan persamaan dan pertidaksamaan linear serta konsep nilai mutlak.
   - **Sistem Persamaan Linear Dua Variabel (SPLDV):** Sama seperti di atas, soal yang melibatkan sistem persamaan linear dengan dua variabel.
   - **Trigonometri Dasar:** Soal yang berkaitan dengan konsep dasar trigonometri.

5. **Literasi dalam Bahasa Indonesia** memiliki 9 subtipe:
   - **Analisis Bacaan dan Kepaduan Paragraf:** Sama seperti di atas, soal yang meminta analisis terhadap struktur dan koherensi paragraf dalam bacaan.
   - **Cerita Pendek:** Soal yang berkaitan dengan analisis dan pemahaman cerita pendek.
   - **Ide Pokok:** Sama seperti di atas, soal yang meminta identifikasi ide utama dalam suatu teks.
   - **Kesimpulan:** Sama seperti di atas, soal yang meminta penarikan kesimpulan logis dari serangkaian premis atau informasi.
   - **Pemahaman Bacaan:** Sama seperti di atas, soal yang menguji pemahaman terhadap isi bacaan.
   - **Penalaran Teks:** Sama seperti di atas, soal yang memerlukan analisis teks untuk menemukan pola atau hubungan logis.
   - **Pernyataan dalam Teks:** Sama seperti di atas, soal yang meminta identifikasi pernyataan yang benar atau salah dalam teks.
   - **Semantik:** Sama seperti di atas, soal yang berkaitan dengan makna kata dan kalimat dalam konteks tertentu.
   - **Sikap dan Tujuan Penulis:** Sama seperti di atas, soal yang meminta analisis terhadap sikap dan tujuan penulis dalam teks.

6. **Literasi dalam Bahasa Inggris** memiliki 10 subtipe:
   - **Author's Attitude and Writing Organisation:** Soal yang menguji pemahaman terhadap sikap penulis dan struktur penulisan dalam teks bahasa Inggris.
   - **Cohesion and Coherence:** Soal yang menguji pemahaman tentang keterpaduan dan koherensi dalam teks bahasa Inggris.
   - **Finding Detailed Information:** Soal yang meminta pencarian informasi detail dalam teks bahasa Inggris.
   - **Inference and Conclusion:** Soal yang meminta penarikan inferensi dan kesimpulan berdasarkan teks bahasa Inggris.
   - **Main Idea and Topic:** Soal yang meminta identifikasi ide pokok dan topik dalam teks bahasa Inggris.
   - **Paraphrase:** Soal yang menguji kemampuan untuk memparafrasekan kalimat atau teks bahasa Inggris.
   - **Purpose of the Text:** Soal yang meminta identifikasi tujuan penulisan teks bahasa Inggris.
   - **Reference:** Sama seperti di atas, soal yang berkaitan dengan penggunaan referensi dalam teks bahasa Inggris.
   - **Semantics:** Soal yang berkaitan dengan makna kata dan kalimat dalam konteks bahasa Inggris.
   - **Stated-Unstated Question:** Soal yang menguji kemampuan untuk mengidentifikasi pertanyaan yang dinyatakan secara eksplisit atau implisit dalam teks bahasa Inggris.

7. **Penalaran Matematika** memiliki 15 subtipe:
   - **Aritmatika Sosial:** Sama seperti di atas, soal yang melibatkan perhitungan matematika dalam konteks sosial sehari-hari.
   - **Aturan Pencacahan:** Sama seperti di atas, soal tentang teknik menghitung banyaknya kemungkinan atau kombinasi.
   - **Fungsi:** Sama seperti di atas, soal yang berkaitan dengan konsep fungsi dalam matematika.
   - **Geometri:** Sama seperti di atas, soal yang berkaitan dengan bentuk, ukuran, dan sifat ruang.
   - **Kecepatan dan Debit:** Soal yang berkaitan dengan perhitungan kecepatan dan debit.
   - **Operasi Bilangan:** Sama seperti di atas, soal yang melibatkan operasi dasar matematika.
   - **Pangkat Sederhana:** Sama seperti di atas, soal yang berkaitan dengan penggunaan dan perhitungan pangkat sederhana.
   - **Peluang:** Soal yang berkaitan dengan perhitungan probabilitas.
   - **Perbandingan:** Sama seperti di atas, soal yang memerlukan perbandingan antara dua atau lebih nilai atau konsep.
   - **Persamaan Linear:** Sama seperti di atas, soal yang berkaitan dengan persamaan matematika linear.
   - **Persamaan, Pertidaksamaan Linear Satu Variabel, dan Nilai Mutlak:** Sama seperti di atas, soal yang melibatkan persamaan dan pertidaksamaan linear serta konsep nilai mutlak.
   - **Sistem Persamaan Linear Dua Variabel (SPLDV):** Sama seperti di atas, soal yang melibatkan sistem persamaan linear dengan dua variabel.
   - **Sistem Persamaan Linear Tiga Variabel (SPLTV):** Sama seperti di atas, soal yang melibatkan sistem persamaan linear dengan tiga variabel.
   - **Statistika Dasar:** Sama seperti di atas, soal yang berkaitan dengan konsep dasar statistik seperti mean, median, dan modus.
   - **Trigonometri Dasar:** Sama seperti di atas, soal yang berkaitan dengan konsep dasar trigonometri.
               
      """

         response = client.chat.completions.create(
         model="ft:gpt-3.5-turbo-1106:bangsoal:exp-2:9bZ7Ofoh",
         temperature=1,
         max_tokens=256,
         top_p=1,
         frequency_penalty=0,
         presence_penalty=0,
         messages=
            [{"role": "system", "content": task}, 
            {"role": "user", "content": f"[QUESTION]: {question}"}, 
            {"role": "user", "content": f"[TYPE]: {main_type}"}]
         )

         result = response.choices[0].message.content
         result = result.replace("[SUBTYPE]:" , "")
         result = result.strip()

         check_constraint = build_prompt.check_output(result)

         if(check_constraint == False):
             return "Subtype result not found"
         
         return result
    
    def check_output(result):
         lst_subtype = ["Author's Attitude and Writing Organisation", "Cohesion and Coherence", "Finding Detailed Information",
                        "Inference and Conclusion", "Main Idea and Topic", "Paraphrase", "Purpose of the Text",
                        "Reference", "Semantics", "Stated-Unstated Question", "Aritmatika Sosial", "Aturan Pencacahan",
                        "Barisan dan Deret", "Kesimpulan", "Operasi Bilangan", "Pembacaan Grafik/Tabel", "Penalaran Teks",
                        "Penarikan Kesimpulan", "Penelitian Sosial", "Perbandingan", "Pernyataan dalam Teks", "Persamaan Linear",
                        "Persamaan, Pertidaksamaan Linear Satu Variabel, dan Nilai Mutlak", "Pola Bilangan dan Huruf", "Sistem Persamaan Linear Dua Variabel (SPLDV)",
                        "Sistem Persamaan Linear Tiga Variabel (SPLTV)", "Statistika Dasar", "Analisis Bacaan dan Kepaduan Paragraf", "EYD V", "Frasa",
                        "Ide Pokok", "Kalimat", "Kata", "Pemahaman Bacaan", "Semantik" , "Sikap dan Tujuan Penulis", "Penalaran Teks", "Pernyataan dalam Teks",
                        "Aturan Sinus dan Cosinus", "Barisan dan Deret", "Fungsi", "Geometri", "Himpunan", "Pangkat Sederhana", "Trigonometri Dasar", "Cerita Pendek",
                        "Reference", "Kecepatan dan Debit", "Peluang", "Penalaran Deduktif", "Penalaran Induktif"] 
         if result not in lst_subtype : 
              return False
         else :
              return True
         
    def predict_type(question):
      client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
         )

      response = client.chat.completions.create(
      model="ft:gpt-4o-2024-08-06:bangsoal:predict-type:9yirTHab:ckpt-step-1976",
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      response_format={
         "type": "text"
      },
      messages=[
      {
         "role": "system",
         "content": [
         {
            "type": "text",
            "text": "Kamu adalah sebuah sistem pendeteksi jenis soal. Kamu akan menerima input, yaitu [QUESTION] \r\n\r\nGunakan pemahaman yang kamu miliki untuk mengelompokkan berbagai jenis soal yang ada.\r\n- [QUESTION] merupakan sebuah soal yang perlu diklasifikasikan.\r\n- [QUESTION] dapat meliputi soal penalaran umum, matematika, bacaan bahasa Indonesia, atau bacaan bahasa Inggris.\r\n- [TYPE] adalah hasil klasifikasi jenis soal berdasarkan [QUESTION] \r\n- [DESCRIPTION] adalah hasil penjelasan mengapa [QUESTION] tersebut termasuk dalam [TYPE] tersebut\r\n      \r\nOutput : hanya menampilkan [TYPE] dan [DESCRIPTION] nya saja\r\nContoh Output : \"\r\n[TYPE]: Kemampuan Penalaran Umum\r\n[DESCTIPTION]: Penjelasan mengapa[QUESTION] tersebut termasuk dalam [TYPE] tersebut“\r\nOutput [TYPE] hanya diperbolehkan tipe-tipe yang telah disebutkan, tidak bisa diluar constraint yang telah diberikan\r\n      \r\nTerdapat 7 kategori [TYPE]:   \r\n1. **Kemampuan Penalaran Umum** : Komponen ini menguji kemampuan siswa dalam memecahkan masalah baru yang tidak bisa diselesaikan hanya dengan kebiasaan yang sudah dipelajari. Penalaran umum mencakup memecahkan masalah baru bernalar secara abstrak\r\n2. **Kemampuan Memahami Bacaan dan Menulis** : Komponen ini menguji kemampuan dasar dan kompleks dalam membaca dan menulis, termasuk memahami wacana tertulis dan ekspresi melalui tulisan.\r\n3. **Pengetahuan dan Pemahaman Umum** : Komponen ini mengukur kemampuan siswa dalam memahami dan mengkomunikasikan pengetahuan yang penting dalam budaya Indonesia, terutama keterampilan berbahasa dan pengetahuan umum.\r\n4. **Pengetahuan Kuantitatif**  : Pengetahuan kuantitatif adalah kedalaman dan luasnya pengetahuan yang terkait dengan matematika, yang merupakan pengetahuan yang diperoleh melalui pembelajaran dan mewakili kemampuan untuk menggunakan informasi kuantitatif dan memanipulasi simbol-simbol angka. Kemampuan ini mencakup pengetahuan mengenai ukuran perhitungan matematika, pemecahan masalah matematika, dan pengetahuan umum matematika. Pengetahuan kuantitatif berfokus juga pada Menerapkan konsep matematika dan menerapkannya dalam kehidupan sehari-hari yang beragam. Membutuhkan kemampuan untuk menerapkan konsep matematika dalam situasi yang nyata, seperti analisis data dan perbandingan statistik. Soal-soal yang ditampilkan lebih fokus pada situasi di kehidupan sehari-hari, dan menggunakan matematika untuk memecahkan suatu masalah.\r\n5. **Literasi dalam Bahasa Indonesia**  : Tes ini berfokus pada Literasi Membaca dalam Bahasa Indonesia, yang mencakup kemampuan memahami, menggunakan, mengevaluasi, merenungkan, dan berinteraksi aktif dengan teks untuk mencapai tujuan dan mengembangkan pengetahuan.\r\n6. **Literasi dalam Bahasa Inggris** : Tes ini berfokus pada Literasi Membaca dalam Bahasa Inggris, yang mencakup kemampuan memahami, menggunakan, mengevaluasi, merenungkan, dan berinteraksi aktif dengan teks untuk mencapai tujuan dan mengembangkan pengetahuan.\r\n7. **Penalaran Matematika** : Penalaran Matematika lebih berfokus pada kemampuan berpikir logis dan abstrak dalam menyelesaikan masalah matematika. Soal-soal dalam kategori ini biasanya menguji kemampuan untuk mengidentifikasi pola, melakukan deduksi, serta memahami konsep-konsep matematika yang lebih kompleks dan teoritis. Soal pada tipe ini umumnya adalah soal cerita yang diikuti dengan pertanyaan matematika. Penalaran Matematika cenderung menantang siswa untuk menggunakan logika dan berpikir kritis dalam menyelesaikan soal-soal yang tidak selalu memiliki aplikasi langsung dalam kehidupan sehari-hari. Selain itu, jika soal bersifat study case maka soal tersebut merupakan tipe ini. Penalaran matematikan juga memerlukan Pemahaman konsep sistematis dan kemampuan dalam menyelesaikan masalah secara logis.  Selain itu, beberapa karakteristik dari soal bertipe penalaran matemarika adalah penekanan pemecahan masalah matematis yang bersifat abstrak, pengukuran pemahaman konsep matematis dengan kemampuan yang logis, dan soal-soal yang ditampilkan cenderung lebih abstrak dan berfokus pada logika yang lebih matematis.\r\n"
         }
         ]
      },
      {
         "role": "user",
         "content": [
         {
            "type": "text",
            "text": f"[QUESTION]: {question}"
         }
         ]
      },
      ],
      )

      result= response.choices[0].message.content
      type_pattern = r'\[TYPE\]:\s*(.*?)\s*\[DESCRIPTION\]:'
      description_pattern = r'\[DESCRIPTION\]:\s*(.*)'

      # Extract TYPE using regex
      type_match = re.search(type_pattern, result, re.DOTALL)
      type_info = type_match.group(1).strip() if type_match else None

      # Extract DESCRIPTION using regex
      description_match = re.search(description_pattern, result, re.DOTALL)
      description_info = description_match.group(1).strip() if description_match else None

      check_constraint = build_prompt.check_type(type_info)

      if(check_constraint == False):
             return "Type result not found"
         
      return {'type' : type_info, 'description': description_info}
    
    def check_type(question_type):
          if str.lower(question_type) in ['kemampuan memahami bacaan dan menulis','kemampuan penalaran umum',
                                          'literasi dalam bahasa indonesia','literasi dalam bahasa inggris',
                                          'penalaran matematika','pengetahuan dan pemahaman umum',
                                          'pengetahuan kuantitatif']:
              return True
          else :
              return False