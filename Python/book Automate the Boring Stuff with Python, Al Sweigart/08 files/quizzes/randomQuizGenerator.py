#! python3
""" My implementation of Quiz Generator.
    Creates quizzes with questions and answers in
    random order, along with the answer key. """
import sys
import random

# The quiz data; keys are states and values are their capitals:
CAPITALS = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix', 'Arkansas': 'Little Rock',
            'California': 'Sacramento', 'Colorado': 'Denver', 'Connecticut': 'Hartford', 'Delaware': 'Dover',
            'Florida': 'Tallahassee', 'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise',
            'Illinois': 'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas': 'Topeka',
            'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine': 'Augusta', 'Maryland': 'Annapolis',
            'Massachusetts': 'Boston', 'Michigan': 'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson',
            'Missouri': 'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada': 'Carson City',
            'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany',
            'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
            'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence', 'South Carolina': 'Columbia',
            'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City',
            'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston',
            'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

TEMPLATE_HEADER = """\t\tState Capital's Test, Ticket {quiz}.
Name:
Date:
Course:
"""
TEMPLATE_ANSWERS = """{question}. State of {state}:
\t{A}
\t{B}
\t{C}
\t{D}
"""

capitals_items = list(CAPITALS.items())
random_answers = list(CAPITALS.values())

quiz = 1
try:
    # create 35 tickets:
    while quiz <= 35:

        quiz_file = open(f"quiz{quiz}.txt", 'w')
        quiz_answers = open(f"quiz{quiz}AnswersKey.txt", 'w')

        print(TEMPLATE_HEADER.format(quiz=quiz), file=quiz_file)

        # each ticket contains len(capitals) questions in random order;
        question = 1
        random.shuffle(capitals_items)
        for state, correct_answer in capitals_items:

            # 3 random answers for each question, only 1 correct;
            variants = []
            random.shuffle(random_answers)
            variants.append(correct_answer)
            for i in range(len(capitals_items)):
                false_variant = random_answers[i]
                if false_variant == correct_answer:
                    continue
                variants.append(false_variant)
                if len(variants) == 4:
                    break
            # variants in random order;
            random.shuffle(variants)

            # output each question to a text file;
            output = {'A': variants[0], 'B': variants[1], 'C': variants[2], 'D': variants[3]}
            print(TEMPLATE_ANSWERS.format(
                question=question,
                state=state,
                A=f"A. {output['A']}",
                B=f"B. {output['B']}",
                C=f"C. {output['C']}",
                D=f"D. {output['D']}"
            ), file=quiz_file)

            # output each correct answer to answers key;
            for key in output:
                if output[key] == correct_answer:
                    line = f"Question {question}: {key}, {output[key]}"
                    print(line, file=quiz_answers)

            # next question.
            question += 1

        # next quiz.
        quiz_file.close()
        quiz_answers.close()
        quiz += 1

except OSError as error:
    print(f"ERROR on quiz {quiz}:", error)

# Done.
sys.exit(0)
