from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import Form

class PredictingTaskType(BaseModel):
    question: Annotated[str, Form()]
    main_type: Annotated[str, Form()]

class ParaphraseQuestion(BaseModel):
    question: Annotated[str, Form()]
    choice: Annotated[str, Form()]
    content: Annotated[str, Form()]
    raw_answer: Annotated[str, Form()]

class CreateQuestion(BaseModel):
    question: Annotated[str, Form(), Field(default= """
Misalkan sudut pada segitiga \( A B C \) adalah \( A, B, C \). jika \( \sin B+\sin C=2 \sin A \), maka nilai dari \( \tan \frac{B}{2} \tan \frac{C}{2} \) adalah ...
""")]
    choice: Annotated[str, Form(), Field(default= """
A. \( \frac{1}{3} \)
B. \( \frac{4}{3} \)
C. \( \frac{1}{2} \sqrt{6} \)
D. \( \frac{1}{6} \sqrt{3} \)
E. \( \frac{21}{12} \)
""")]
    raw_answer: Annotated[str, Form(), Field(default = """
Karena \( A, B, C \) adalah sudut-sudut pada segitiga maka berlaku \( A+B+C=180^{\circ} \)
\[
A=180^{\circ}-(B+C)
\]

Sehingga,
\[
\begin{array}{l}
\sin B+\sin C=2 \sin A \\
\sin B+\sin C=2 \sin \left(180^{\circ}-(B+C)\right) \\
2 \sin \left(\frac{B+C}{2}\right) \cos \left(\frac{B-C}{2}\right)=2 \sin (B+C) \\
2 \sin \left(\frac{B+C}{2}\right) \cos \left(\frac{B-C}{2}\right)=4 \sin \left(\frac{B+C}{2}\right) \cos \left(\frac{B+C}{2}\right) \\
\cos \left(\frac{B-C}{2}\right)=2 \cos \left(\frac{B+C}{2}\right) \\
\cos \left(\frac{B}{2}\right) \cos \left(\frac{C}{2}\right)+\sin \left(\frac{B}{2}\right) \sin \left(\frac{C}{2}\right)=2 \cos \left(\frac{B}{2}\right) \cos \left(\frac{C}{2}\right)-2 \sin \left(\frac{B}{2}\right) \sin \left(\frac{C}{2}\right) \\
3 \sin \left(\frac{B}{2}\right) \sin \left(\frac{C}{2}\right)=\cos \left(\frac{B}{2}\right) \cos \left(\frac{C}{2}\right) \\
\frac{\sin \left(\frac{B}{2}\right)}{\cos \left(\frac{B}{2}\right)} \frac{\sin \left(\frac{C}{2}\right)}{\cos \left(\frac{C}{2}\right)}=\frac{1}{3} \\
\tan \left(\frac{B}{2}\right) \tan \left(\frac{C}{2}\right)=\frac{1}{3} \\
\end{array}
\] 
""")]

class CreateAnswer(BaseModel):
    question: Annotated[str, Form()]
    choice: Annotated[str, Form()]

class CreateAnswerIsian(BaseModel):
    question: Annotated[str, Form(), Field(default="Panitia jalan sehat akan membuat kupon bernomor yang terdiri atas 4 angka yang disusun oleh angkaangka \( 0,1,3,5 \) dan 7 . Jika angka pertama atau terakhir tidak 0 , maka banyak kupon yang dapat dibuat adalah ....")]
    answer: Annotated[str, Form(), Field(default="600")]
    description: Annotated[str, Form(), Field(default="Banyaknya kupon yang dapat dibuat adalah \( 5^{4}-5^{2}=625-25=600 \)")]


class CreateMaterial(BaseModel):
    topic: Annotated[str, Form()]

class CreateQuestionIsian(BaseModel):
    question: Annotated[str, Form()]
    explanation: Annotated[str, Form()]
    answer: Annotated[str, Form()]


class CreateQuestionTrueFalse(BaseModel):
    question: Annotated[str, Form(), Field(default = """
Penggunaan plastik ternyata menimbulkan masalah-masalah tertentu. Padahal, penggunaan plastik telah meluas hampir ke seluruh bidang kehidupan. Berbagai produk dan perala tan dihasilkan dari bahan ini karena dinilai lebih ekonornis, tidak mudah pecah, fleksibel, dan ringan. Salah satu contoh produk berbahan plastik yang paling sering dipakai oleh masyarakat adalah botol plastik.
Peningkatan jumlah pemakaian botol plastik menimbulkan dampak bagi lingkungan ketika sudah tidak terpakai. Plastik adalah benda yang sulit terurai. Proses terurai plastik dapat berJangsung an tara 450 sampai 1.000 tahun. Padahal, di seluruh dunia, setiap tahun digunakan sekitar 50 miliar botol plastik sehingga diprediksikan pada mas a depan, lokasi pembuangan sampah hampir tidak akan cukup untuk menampung semuanya.
Upaya dam ulang dan penggunaan kembali botol plastik tidak sepenuhnya mengatasi masalah lingkungan karena tingkat penggunaan botol plastik sangat tinggi. Selain itu, penggunaan kembali plastik yang didaur ulang menimbulkan masalah baru, yaitu masalah kesehatan. Hal ini disebabkan plastik yang terurai akan melepaskan zat kimia yang disebut Bisphenol A (BPA) ke dalam air. Zat BPAini memiliki beberapa efek negatif pada hormon tubuh yang dapat menimbulkan gangguan kesehatan, seperti gangguan perilaku, penurunan kekebalan, gangguan belajar, diabetes, dan obesitas.
Kutipan di atas memiliki gagasan pokok …
""" )]
    total_question: Annotated[str, Form(),Field(default="5")]

class CreateQuestionMultAnswer(BaseModel):
    question: Annotated[str, Form()]

class CreateAnswerMultAnswer(BaseModel):
    question: Annotated[str, Form(), Field(default="etergantungan masyarakat global terhadap penggunaan produk plastik, khususnya botol plastik, telah menyebabkan berbagai dampak lingkungan dan kesehatan yang signifikan. Setiap tahun, miliaran botol plastik digunakan dan banyak di antaranya berakhir di tempat pembuangan sampah, menciptakan masalah tata kelola limbah yang besar karena plastik membutuhkan waktu yang sangat lama untuk terdegradasi, sekitar 450 hingga 1.000 tahun. Selain itu, botol plastik yang didaur ulang pun menghasilkan dampak kesehatan negatif karena pelepasan zat kimia seperti Bisphenol A (BPA), yang berdampak buruk pada keseimbangan hormon tubuh dan berpotensi mengarah pada berbagai gangguan kesehatan seperti diabetes dan obesitas. Pernyataan mana yang secara akurat mendeskripsikan problematika yang diuraikan dalam teks terkait dengan penggunaan plastik ini?")]
    choice: Annotated[str, Form(), Field(default="""A. Meningkatkan penggunaan plastik mengurangi polusi lingkungan 
B. Plastik yang didaur ulang aman untuk kesehatan manusia 
C. Peningkatan penggunaan botol plastik merespons kebutuhan masyarakat namun menciptakan masalah lingkungan dan kesehatan 
D. Plastik terurai dengan cepat sehingga mengurangi beban di tempat pembuangan sampah 
E. Upaya mendaur ulang secara penuh menyelesaikan problem plastik """)]
    answer: Annotated[str, Form(),Field(default="C")]
    description: Annotated[str, Form(),Field(default="Berdasarkan teks, peningkatan kebergantungan terhadap produk plastik, khususnya botol, menciptakan masalah yang serius baik terhadap lingkungan maupun kesehatan manusia, dan usaha daur ulang belum sepenuhnya menyelesaikan masalah tersebut.")]

class CreateAnswerTF(BaseModel):
    question: Annotated[str, Form(), Field(default="""Penggunaan plastik dalam kehidupan sehari-hari memiliki dampak pada kesehatan dan lingkungan. Produk plastik seperti kantong plastik yang sering digunakan dalam berbelanja memiliki sifat yang tahan lama dan tidak mudah terurai. Plastik dapat bertahan di lingkungan selama hingga 500 tahun. Dengan penggunaan yang masif dan berkelanjutan, plastik telah menyumbangkan jumlah sampah yang besar, yang memiliki dampak langsung pada ekosistem dan kesehatan manusia.  

Kantong plastik dianggap sebagai salah satu penyumbang utama polusi karena sifatnya yang tahan lama dan produksinya yang murah. Dampak lingkungan dari kantong plastik muncul ketika mereka tidak dibuang dengan benar, mengakibatkan polusi visual di perkotaan dan bahkan mempengaruhi kehidupan hewan yang salah memakan plastik sebagai makanan. Selain itu, kantong plastik juga dapat merilis zat berbahaya seperti Bisphenol A (BPA) saat terurai, yang memiliki konsekuensi serius terhadap kesehatan, merusak hormon dan meningkatkan risiko penyakit seperti gangguan hormonal, kanker, dan efek reproduktif.

Berbagai upaya telah dilakukan untuk mengurangi penggunaan kantong plastik, termasuk pengenaan tarif, pelarangan penggunaan, dan mempromosikan tas belanja yang dapat digunakan kembali. Meskipun demikian, tantangan tetap ada karena keefektifan kebijakan-kebijakan ini masih terbatas dan penggunaan kantong plastik masih tinggi di berbagai bagian dunia. Manakah pernyataan tersebut yang bernilai benar?""")]
    choice: Annotated[str, Form(), Field(default="""1. Kantong plastik dapat bertahan hingga 500 tahun di lingkungan 
2. Penggunaan kembali kantong plastik tidak mempengaruhi kesehatan manusia 
3. Kebijakan larangan penggunaan kantong plastik telah efektif mengurangi polusi plastik di seluruh dunia 
4. Kantong plastik baik untuk kehidupan manusia""")]
    description: Annotated[str, Form(), Field(default="""1. Kantong plastik dapat bertahan hingga 500 tahun di lingkungan - TRUE
2. Penggunaan kembali kantong plastik tidak mempengaruhi kesehatan manusia - FALSE
3. Kebijakan larangan penggunaan kantong plastik telah efektif mengurangi polusi plastik di seluruh dunia - FALSE
4. Kantong plastik baik untuk kehidupan manusia - FALSE""")]
    
class ExtractTextFromImage(BaseModel):
    image_url: Annotated[str, Form(), Field(default="https://bangsoal.s3.ap-southeast-1.amazonaws.com/assets/CleanShot+2024-10-09+at+12.05.03%402x.png")]