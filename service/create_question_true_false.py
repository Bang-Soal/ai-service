from openai import OpenAI
from service.call_env import env_data
import re


class create_question_true_false() : 
    def build_regex(result):
        question_pattern = r"\[NEW_QUESTION\]:\s*(.*?)\n\[NEW_CHOICE\]"
        choice_pattern  = r"\[NEW_CHOICE\]:\s*(.*?)\n\[NEW_ANSWER\]"
        answer_pattern = r"\[NEW_ANSWER\]:\s*(.*?)$"

        question_match = re.search(question_pattern, result, re.DOTALL)
        question = question_match.group(1).strip() if question_match else None

        answer_match = re.search(answer_pattern, result, re.DOTALL)
        answer = answer_match.group(1).strip() if answer_match else None

        choice_match = re.search(choice_pattern, result, re.DOTALL)
        choice_block = choice_match.group(1).strip() if choice_match else None

        choices = []
        for line in choice_block.splitlines():
            match = re.match(r"([A-Z])\.\s*(.+?)\s*-\s*(TRUE|FALSE)", line)
            if match:
                key, content, is_true = match.groups()
                choices.append({
                    'key': key,
                    'content': content,
                    'is_true': is_true == 'TRUE'
                })
        
        return {
            'question' : question,
            'choice' : choices,
            'answer' : answer
            }

        
    
    def run(question, total_question):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """
You are a system designed to generate TRUE-FALSE questions based on a given argument and provide detailed answer explanations. The difficulty level of the questions you create should be higher than the current ones provided. The language used will adapt to the input, either Indonesian or English, but explanations must always be in Indonesian, as the target users are Indonesian students.

INPUT ORDER:
1. [QUESTION]
2. [TOTAL_QUESTION]

OUTPUT ORDER:
1. [NEW_QUESTION]
2. [NEW_CHOICE]
3. [NEW_ANSWER]

The questions you generate may include general reasoning, mathematics, reading comprehension in Indonesian, or reading comprehension in English. All questions you create must be NEW, meaning you cannot reference any previous questions. You need to restate the question clearly and, when applicable, create new text if the question involves a reading passage in either Indonesian or English.

If the original question or answer uses English, you must still create the new question and answer in English. The goal is not to translate or modify the question but to create a new one. Explanations should remain in Indonesian.

You will be provided with a [QUESTION] and the total number of TRUE-FALSE arguments to generate [TOTAL_QUESTION]. Based on these, you must produce a new question with a higher difficulty level [NEW_QUESTION], a set of TRUE-FALSE options based on the new question [NEW_CHOICE], and a detailed explanation of each option [NEW_ANSWER].

FORMAT OF [NEW_CHOICE]:
[Letter]. Argument - TRUE/FALSE

Steps:
1. First, create the new question that will be used as [NEW_QUESTION].
   - Detect the language of the original [QUESTION]: Indonesian or English.
   - If the question involves a text passage in either Indonesian or English (at least 2 paragraphs or 200 words), you must create a new text passage with a minimum of 3 paragraphs or 300 words for [NEW_QUESTION]. This must still be relevant to the topic in the original [QUESTION]. Do not provide passages shorter than 3 paragraphs or below 200 words.
   - For mathematical questions, [NEW_ANSWER] must include step-by-step solutions along with the final answer, and detailed explanations of the TRUE/FALSE options are not required.

2. If the [QUESTION] is in English, ensure the new question and answer remain in English, but the explanation will still be in Indonesian.

3. The paragraph in [NEW_QUESTION] must end with the statement: 
   "Pernyataan-pernyataan di bawah ini yang tepat adalah ..."

4. Create the necessary TRUE/FALSE arguments for [NEW_CHOICE], based on the number specified in [TOTAL_QUESTION].

5. Provide a detailed explanation of each argument in [NEW_ANSWER], clearly explaining why each argument is TRUE or FALSE.

FORMAT FOR [NEW_ANSWER]:
[Number] Argument – TRUE/FALSE
Explanation: [Explain the reasoning]

Example:
1. Rising ocean temperatures will reduce the frequency of hurricanes and typhoons. – FALSE 
Explanation: Naiknya suhu laut sebenarnya meningkatkan frekuensi dan intensitas badai seperti angin topan dan hurricane, karena menyediakan lebih banyak energi dan uap air.

NOTE:
- For mathematics-based questions, detailed steps and calculations should be provided in [NEW_ANSWER], but it is not necessary to explain each option in [NEW_CHOICE] separately.
- If the question is in Indonesian, use Indonesian for both [NEW_QUESTION] and [NEW_CHOICE], but the explanation in [NEW_ANSWER] must still be in Indonesian. Ensure that the output follows this sequence: [NEW_QUESTION], [NEW_ANSWER], and [NEW_CHOICE].

Before generating the final output, please double-check to ensure that the output follows this order:
1. [NEW_QUESTION]
2. [NEW_CHOICE]
3. [NEW_ANSWER]

Example output : 
[NEW_QUESTION]:
Dampak penggunaan plastik terhadap lingkungan dan kesehatan manusia telah menjadi perhatian utama dalam beberapa dekade terakhir. Plastik, karena keunggulannya yang termasuk ringan, fleksibel, dan tahan lama, telah secara luas digunakan dalam berbagai produk konsumsi, salah satu yang paling umum adalah botol plastik. Material ini memang memiliki banyak keuntungan, tetapi juga menyajikan risiko yang signifikan terutama terkait dengan pengelolaan limbah dan dampak kesehatan.
Peningkatan produksi dan pemakaian botol plastik menimbulkan tantangan besar dalam pengelolaan sampah. Sangat sulit untuk mendaur ulang plastik dalam jumlah besar yang digunakan, dan sebagai hasilnya, banyak dari plastik tersebut berakhir di TPA (Tempat Pembuangan Akhir), di mana mereka bisa bertahan hingga ribuan tahun sebelum terurai. Penelitian menunjukkan bahwa plastik dapat memakan waktu sekitar 450 sampai 1000 tahun untuk terurai sepenuhnya, yang berarti bahwa plastik yang dibuang hari ini akan tetap ada untuk generasi yang akan datang.
Selain masalah lingkungan, ada juga masalah kesehatan yang terkait dengan penggunaan dan paparan plastik terutama yang berkaitan dengan zat kimia berbahaya seperti Bisphenol A (BPA). BPA telah terbukti lepas ke dalam makanan atau minuman dari kemasan yang terbuat dari plastik yang mengandungnya. Zat ini diketahui memiliki efek estrogenik yang dapat mengganggu keseimbangan hormon dan berpotensi menyebabkan berbagai masalah kesehatan termasuk efek pada perilaku, penurunan sistem kekebalan tubuh, gangguan belajar, serta peningkatan risiko penyakit seperti diabetes dan obesitas. Mengingat masalah tersebut, penting untuk mempertimbangkan alternatif yang lebih ramah lingkungan dan aman bagi kesehatan.
Pernyataan-pernyataan di bawah ini yang tepat adalah...
[NEW_CHOICE]:
A. Botol plastik dapat terurai sepenuhnya dalam kurun waktu kurang dari 50 tahun - FALSE
B. Zat BPA yang meresap dari botol plastik dapat menyebabkan gangguan kesehatan seperti gangguan perilaku dan diabetes - TRUE
C. Daur ulang semua jenis plastik merupakan solusi paling efektif untuk mengurangi dampak lingkungan dari pembuangan plastik - FALSE
[NEW_ANSWER]:
1. Botol plastik dapat terurai sepenuhnya dalam kurun waktu kurang dari 50 tahun - FALSE
Explanation: Botol plastik sangat sulit terurai dan memerlukan waktu antara 450 sampai 1000 tahun untuk terurai sepenuhnya. Pernyataan bahwa botol plastik dapat terurai dalam kurun waktu kurang dari 50 tahun adalah tidak benar, karena proses degradasi plastik membutuhkan waktu yang sangat lama disebabkan oleh komposisi kimianya yang kuat.
2. Zat BPA yang meresap dari botol plastik dapat menyebabkan gangguan kesehatan seperti gangguan perilaku dan diabetes - TRUE
Explanation: Bisphenol A (BPA) adalah zat kimia yang sering ditemukan dalam banyak plastik dan dapat lepas ke makanan atau minuman. BPA menunjukkan efek sifat mirip estrogen yang berpotensi mengganggu fungsi hormon dan dikaitkan dengan berbagai masalah kesehatan seperti gangguan perilaku, gangguan sistem imun, gangguan belajar, diabetes, dan obesitas.
3. Daur ulang semua jenis plastik merupakan solusi paling efektif untuk mengurangi dampak lingkungan dari pembuangan plastik - FALSE
Explanation: Meskipun daur ulang plastik bisa berperan dalam mengurangi dampak lingkungan, tidak semua jenis plastik dapat didaur ulang dengan efektif. Beberapa plastik, karena alasan teknis atau ekonomis, tidak dapat didaur ulang, dan meskipun daur ulang membantu, itu bukan solusi mutlak untuk masalah sampah plastik, terutama mengingat volume produksi dan konsumsi plastik yang sangat tinggi saat ini.
"""

        complation = client.chat.completions.create(
        model = 'gpt-4-turbo',
        messages = [
            {
                "role": "system", "content": task
            },
            {
                                "role": "user", "content": "[QUESTION]: " + question
                            },
                            {
                                "role": "user", "content": "[TOTAL_QUESTION]: " + total_question
                            },

        ]
        )
        result = complation.choices[0].message.content

        return create_question_true_false.build_regex(result)
