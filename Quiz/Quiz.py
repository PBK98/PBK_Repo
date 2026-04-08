# Quiz.py

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.question_number = 0

    def run_quiz(self):
        # questions 리스트에 있는 모든 문제를 하나씩 반복합니다.
        for q in self.questions:
            self.question_number += 1
            print(f"\nQ{self.question_number}. {q['question']}")

            # 선택지를 출력합니다.
            for choice in q['choices']:
                print(choice)

            # 사용자 입력을 받습니다.
            user_answer_num = input("정답: ")
            user_answer_text = q['choices'][int(user_answer_num) - 1]

            # 정답을 확인합니다.
            if user_answer_text == q['answer']:
                print("정답입니다!")
                self.score += 10 # 정답일 경우 10점 추가
            else:
                print(f"오답입니다. 정답은 {q['answer']} 입니다.")

        # 최종 점수를 반환합니다.
        return self.score, len(self.questions)