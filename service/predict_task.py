from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class build_prompt() : 
    def run(question, main_type):
         client = OpenAI(
         organization=os.getenv("ORG_KEY_OPENAI"),
         api_key=os.getenv("API_KEY_OPENAI")
         )

         task = """Kamu adalah sebuah sistem pendeteksi jenis soal. Kamu akan menerima dua input, yaitu [QUESTION] dan [TYPE]. Tugasmu adalah menentukan [SUBTYPE] dari kedua input tersebut.

         Gunakan pemahaman yang kamu miliki untuk mengelompokkan berbagai jenis soal yang ada.

         - [QUESTION] merupakan sebuah soal yang perlu diklasifikasikan.
         - [QUESTION] dapat meliputi soal penalaran umum, matematika, bacaan bahasa Indonesia, atau bacaan bahasa Inggris.
         - [TYPE] merupakan tipe level 1 dari soal yang diberikan.
         - [SUBTYPE] adalah hasil klasifikasi jenis soal berdasarkan [QUESTION] dan [TYPE].

         Terdapat 7 kategori [TYPE]:

         1. **Kemampuan Penalaran Umum** memiliki 17 subtipe:
            - **Aritmatika Sosial:** Soal yang melibatkan perhitungan matematika dalam konteks sosial sehari-hari seperti jual beli, pembagian, dan lain-lain.
            - **Aturan Pencacahan:** Soal tentang teknik menghitung banyaknya kemungkinan atau kombinasi, seperti permutasi dan kombinasi.
            - **Barisan dan Deret:** Soal yang berkaitan dengan urutan angka atau huruf yang membentuk pola tertentu.
            - **Kesimpulan:** Soal yang meminta penarikan kesimpulan logis dari serangkaian premis atau informasi.
            - **Operasi Bilangan:** Soal yang melibatkan operasi dasar matematika seperti penjumlahan, pengurangan, perkalian, dan pembagian.
            - **Pembacaan Grafik/Tabel:** Soal yang mengharuskan interpretasi data dari grafik atau tabel.
            - **Penalaran Teks:** Soal yang memerlukan analisis teks untuk menemukan pola atau hubungan logis.
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

         5. **Literasi dalam Bahasa Indonesia** memiliki 10 subtipe:
            - **Analisis Bacaan dan Kepaduan Paragraf:** Sama seperti di atas, soal yang meminta analisis terhadap struktur dan koherensi paragraf dalam bacaan.
            - **Cerita Pendek:** Soal yang berkaitan dengan analisis dan pemahaman cerita pendek.
            - **Ide Pokok:** Sama seperti di atas, soal yang meminta identifikasi ide utama dalam suatu teks.
            - **Kesimpulan:** Sama seperti di atas, soal yang meminta penarikan kesimpulan logis dari serangkaian premis atau informasi.
            - **Pemahaman Bacaan:** Sama seperti di atas, soal yang menguji pemahaman terhadap isi bacaan.
            - **Penalaran Teks:** Sama seperti di atas, soal yang memerlukan analisis teks untuk menemukan pola atau hubungan logis.
            - **Pernyataan dalam Teks:** Sama seperti di atas, soal yang meminta identifikasi pernyataan yang benar atau salah dalam teks.
            - **Reference:** Soal yang berkaitan dengan penggunaan referensi dalam teks.
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
         return result