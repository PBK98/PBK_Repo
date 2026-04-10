# Quiz.py

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.question_number = 0

    def run_quiz(self):
        print("\n(힌트를 보려면 'hint'를 입력하세요. 5점이 차감됩니다.)")

        for q in self.questions:
            self.question_number += 1
            print(f"\nQ{self.question_number}. {q['question']}")

            for choice in q['choices']:
                print(choice)
            
            hint_used = False

            while True:
                # 사용자가 'hint' 대신 '힌트'라고 입력할 수도 있으니, 둘 다 처리해주는 것이 좋습니다.
                user_input = input("정답(번호) 또는 '힌트'를 입력하세요: ")

                # 1. '힌트' 입력 처리
                if user_input == '힌트' or user_input.lower() == 'hint':
                    hint_text = q.get('hint', "")
                    
                    if hint_text and not hint_used:
                        print(f"💡 힌트: {hint_text}")
                        self.score -= 5
                        hint_used = True
                        print("(-5점) 힌트를 사용했습니다. 다시 정답을 입력해주세요.")
                    elif hint_used:
                        print("[!] 이미 이 문제의 힌트를 사용했습니다.")
                    else:
                        print("[!] 이 문제에는 힌트가 없습니다.")
                    continue # 힌트를 봤으니 다시 입력을 받습니다.

                # 2. 정답/오답 처리 로직 추가
                # (예외 처리는 나중에 하신다고 하니, 일단 숫자가 잘 입력되었다고 가정합니다.)
                user_answer_num = int(user_input)
                user_answer_text = q['choices'][user_answer_num - 1]

                if user_answer_text == q['answer']:
                    print("정답입니다!")
                    self.score += 10
                else:
                    # 오답일 경우, 점수 변경 없이 메시지만 출력합니다.
                    print(f"오답입니다.")
                
                # 정답이든 오답이든, 답변을 했으므로 while 루프를 빠져나가 다음 문제로 갑니다.
                break

        return self.score, len(self.questions)