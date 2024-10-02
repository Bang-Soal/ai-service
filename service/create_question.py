from openai import OpenAI
from service.call_env import env_data
import re


class create_question() : 
    def build_regex(result):
        question_pattern = r"\[NEW_QUESTION\]:\s*(.+?)\n"
        answer_pattern = r"\[NEW_ANSWER\]:\s*(.+?)(?=\[NEW_CHOICE\])"
        choice_pattern = r"\[NEW_CHOICE\]:\s*((?:[A-Z]\..+?-\s*(?:TRUE|FALSE)\n?)+)"

        # Extract using regex
        question = re.search(question_pattern, result, re.DOTALL).group(1).strip()
        answer = re.search(answer_pattern, result, re.DOTALL).group(1).strip()

        # Extract and format choices
        choice_matches = re.search(choice_pattern, result, re.DOTALL).group(1)
        choices = []
        for line in choice_matches.splitlines():
            match = re.match(r"([A-Z])\.\s*(.+?)\s*-\s*(TRUE|FALSE)", line)
            if match:
                key, content, is_true = match.groups()
                choices.append({
                    'key': key,
                    'content': content,
                    'is_true': is_true == 'TRUE'
                })

        # Create the final dictionary
        formatted_output = {
            'Question': question,
            'Answer': answer,
            'choice': choices
        }

        return formatted_output
    
    def run(question, choice, raw_answer):
        client = OpenAI(
         organization=env_data.org_key(),
         api_key=env_data.api_key()
        )
        task = """
You are a system for creating questions, answer choices, and explanations with a higher difficulty level than the current questions provided for the UTBK, which are questions for university admissions in Indonesia. The language used can be either Indonesian or English, depending on the input provided. Additionally, provide answer explanations in a relaxed manner with a language style appropriate for high school students.

INPUT ORDER: [QUESTION], [CHOICE], [RAW_ANSWER]
OUTPUT ORDER: [NEW_QUESTION], [NEW_ANSWER], [NEW_CHOICE]

The questions you create can cover general reasoning, mathematics, Indonesian language reading, or English language reading. The questions you create must be NEW questions, and you cannot refer to previous questions. You need to explain what is required once again. If the question contains a text in Indonesian or English, you need to create a new text so that the question is not referring to the previous text. If the question and answer use English, you must continue using English to create the new question and answer. Your goal is not to translate or change the question and answer into Indonesian.

You will be given a question labeled [QUESTION], answer choices labeled [CHOICE] containing five answer options (A, B, C, D, E) with the TRUE or FALSE, and an answer explanation labeled [RAW_ANSWER]. You are tasked with creating a new question by understanding the three given aspects: [QUESTION], [CHOICE], and [RAW_ANSWER] to produce a similar question but with a higher difficulty level [NEW_QUESTION], new answer choices based on the new question [NEW_CHOICE], and a relaxed explanation suitable for high school students [NEW_ANSWER].

Creation Steps:

1. The first thing to create is the question that will become [NEW_QUESTION].
2. First, detect the language used in [NEW_QUESTION], whether it's Indonesian or English.
3. If the question contains an Indonesian or English reading text, meaning a reading text that consists of at least 2 paragraphs or a minimum of 200 words, you need to rewrite the text with at least 3 paragraphs or at least 300 words (MINIMUM 3 PARAGRAPHS OR 250 WORDS) in [NEW_QUESTION] that remains relevant to the topic of the reading in [QUESTION]. It is forbidden to provide a reading text that consists of only 1 paragraph or is below 200 words in [NEW_QUESTION] for this case.
4. If [QUESTION] and [CHOICE] use English, you must continue using English to create [NEW_QUESTION] and [NEW_CHOICE]. Your task is not to translate it into Indonesian but to create a question with the same topic along with its answer. Thus, [NEW_QUESTION] and [NEW_CHOICE] must NOT use Indonesian.
5. After that, a detailed explanation is made for [NEW_QUESTION] to create [NEW_ANSWER].
6. The answer in [NEW_ANSWER] is based on [NEW_QUESTION], not using the same thing from [RAW_ANSWER].
7. The explanation in [NEW_ANSWER] should be written in a more relaxed manner with a language style suitable for high school students, so users will find the explanation more appealing.
8. For math questions, [NEW_ANSWER] is expected to display step-by-step solutions leading to the final answer, but still with a language style suitable for high school students, so users will find the explanation more appealing.
At this stage, you have obtained [NEW_QUESTION] and [NEW_ANSWER].

After obtaining the answer in [NEW_ANSWER], you will continue to create [NEW_CHOICE]. The method for creating [NEW_QUESTION] follows this format: 
A. Answer 1 - TRUE/FALSE
B. Answer 2 - TRUE/FALSE
C. Answer 3 - TRUE/FALSE
D. Answer 4 - TRUE/FALSE
E. Answer 5 - TRUE/FALSE
Ensure that the correct answer in [NEW_ANSWER] is included in one of the choices in [NEW_QUESTION] and every choices have TRUE or FALSE description like the format. And then ensure that have 5 choices, there are (A,B,C,D,E)

At this stage, you have obtained [NEW_QUESTION], [NEW_ANSWER], and [NEW_CHOICE].

After that, you will update the answer contained in [NEW_ANSWER] by following the steps below (the choices in [NEW_CHOICE] must not differ from those in [NEW_ANSWER]):
- In [NEW_ANSWER], divide it into 3 topics: "Pemahaman soal", "Pembahasan pilihan jawaban", and "Kesimpulan".
- "Pemahaman soal" is a paragraph explaining the meaning and purpose of the question that will be discussed by analyzing the intent of the provided [NEW_QUESTION]. Additionally, in this section, you should take key points from the question to make your analysis of the question.
- "Pembahasan pilihan jawaban" is a paragraph that explains each of the given answer choices (A, B, C, D, E) with the help of the analysis you have done in understanding the question, so you can find the most appropriate answer and explain each of the answer choices provided. You must explain every choice why the choice is true or why the choice is false based on context ont the [NEW_QUESTION]
- "Kesimpulan" is a paragraph that explains the final answer chosen by selecting one of the choices provided in [NEW_CHOICE].

Format of [NEW_ANSWER]
Pemahaman soal :
[isi pemahaman soal]

Pembahasan pilihan jawaban :
[isi pembahasan pilihan jawaban]

Kesimpulan :
[isi kesimpulan]

Note:
- If the question involves mathematics or calculations, it is expected that the understanding of the question section will explain in detail the steps to solve the problem, along with the calculation results in [NEW_QUESTION], without the need to explain each answer in [NEW_CHOICE].
- If the question is in English, you are required to use English to create [NEW_QUESTION] and [NEW_CHOICE], but the explanation in [NEW_ANSWER] must be in Indonesian. However, the output order must remain as follows: [NEW_QUESTION], followed by [NEW_ANSWER], and ending with [NEW_CHOICE].
- Before outputting, please make sure the output order is [NEW_QUESTION], [NEW_ANSWER], and then [NEW_CHOICE]. ([NEW_QUESTION] -> [NEW_ANSWER] -> [NEW_CHOICE])
""" 
        bc_question = """
        Tika, Pita, Ana, Ira, dan Retha pergi bersama ke toko buah. Empat orang diantara mereka membeli jeruk. Pita dan Ira tidak membeli apel seperti lainnya. pita hanya membeli anggur. Tika dan Retha juga tidak membeli anggur seperti yang lainnya. siapakah yang membeli jenis buah yang sama persis?
        """
        bc_choice = """
        A. Tika dan Ira
        B. Ana dan Ira
        C. Tika dan Ana
        D. Tika dan Pita
        E. Tika dan Retha
        """

        bc_answer = """
        Tika, Pita, Ana, Ira, Retha
        4 orang membeli jeruk
        Pita dan Ira tidak membeli apel
        Pita hanya membeli anggur.
        Tika dan Retha tidak membeli anggur Kesimpulan
        Pita membeli anggur Tika membeli Jeruk, Apel Ana membeli Jeruk, Apel, anggur Ira membeli Jeruk, Anggur Retha membeli Jeruk, Apel
        """

        bc_regenerate = """
[NEW_QUESTION]:
Dalam sebuah acara arisan, Lima teman yaitu Budi, Doni, Eka, Fina, dan Gita membeli beberapa jenis buah untuk dihidangkan. Tiga dari mereka memilih untuk membeli pisang. Budi dan Eka tidak membeli semangka berbeda dengan yang lain. Doni hanya membeli melon. Gita dan Fina juga tidak membeli melon seperti yang lainnya. Siapakah yang membeli jenis buah yang sama persis?

[NEW_ANSWER]:
Pemahaman soal: 
Di acara arisan, ada lima teman: Budi, Doni, Eka, Fina, dan Gita. Mereka beli beberapa jenis buah untuk disantap bareng-bareng. Dari soal ini, kita tahu beberapa informasi penting:
- Tiga orang beli pisang.
- Budi dan Eka nggak beli semangka.
- Doni cuma beli melon.
- Gita dan Fina nggak beli melon.
Sekarang, kita harus mencari siapa yang beli jenis buah yang sama persis.

Pembahasan pilihan jawaban: 
A. Budi dan Doni - Nggak mungkin. Doni cuma beli melon, sementara Budi nggak beli melon dan juga semangka. Jadi, mereka nggak beli buah yang sama.
B. Eka dan Doni - Sama kayak yang sebelumnya, nggak cocok. Doni cuma beli melon, sementara Eka nggak beli melon, jadi buah yang mereka beli pasti beda.
C. Budi dan Eka - Mungkin bisa aja mereka beli pisang yang sama, tapi nggak ada info pasti apakah mereka beli buah lain selain pisang. Jadi, masih belum pasti.
D. Fina dan Gita - Ini cocok! Mereka berdua beli pisang dan semangka, terus sama-sama nggak beli melon. Jadi, jenis buah yang mereka beli sama persis.
E. Gita dan Doni - Nggak mungkin juga. Doni cuma beli melon, sementara Gita nggak beli melon.

Kesimpulan: 
Dari analisis ini, jelas bahwa Fina dan Gita adalah dua orang yang membeli jenis buah yang sama persis, yaitu pisang dan semangka.

[NEW_CHOICE]:
A. Budi dan Doni - FALSE
B. Eka dan Doni - FALSE
C. Budi dan Eka - FALSE
D. Fina dan Gita - TRUE
E. Gita dan Doni - FALSE
"""

        complation = client.chat.completions.create(
        model = 'gpt-4o',
        messages = [
            {
                "role": "system", "content": task
            },
            {
                                "role": "user", "content": "[QUESTION]: " + bc_question
                            },
                            {
                                "role": "user", "content": "[CHOICE]: " + bc_choice
                            },
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + bc_answer 
                            },
                            {
                                "role": "assistant", "content": "[OUTPUT]: " + bc_regenerate
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
                            {
                                "role": "user", "content": "[RAW_ANSWER]: " + raw_answer 
                            }
            
            ]
        )

        result = complation.choices[0].message.content

        return create_question.build_regex(result)
