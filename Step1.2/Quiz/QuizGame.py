# QuizGame.py

import json #json의 표준 라이브러리를 가져와서 json의 기능을 사용하겠다.
from Quiz import Quiz # Quiz.py 를 가져와서 그 안의 Quiz 클래스를 사용하겠다.

# --- 데이터 로드/저장 함수 (이전과 동일) ---
# load_data(filename) 에서 filename은 이 함수를 사용해서 불러올 파일명을 담을 변수이고, load_data는 함수의 이름이다.
def load_data(filename):
    try:
        # json의 open 함수를 사용해서 filename에 담긴 파일을 읽기 모드('r')로 열고, encoding은 utf-8로 설정한다. 그리고 그 파일을 f라는 변수에 담는다.(as f)
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        if "user" in filename:
            return {"username": "Guest", "solved_count": 0, "score": 0}
        if "state" in filename:
            return {"description": "", "questions": []}
        return None

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- 사용자 정의 예외 클래스 ---
class InvalidInputError(ValueError):
    """숫자가 아닌 값을 입력했을 때 발생하는 예외"""
    def __init__(self, message="잘못된 입력입니다. 숫자를 입력해주세요."):
        self.message = message
        super().__init__(self.message)

# --- 메뉴 기능별 함수 ---
class SolveQuiz:
    def start_quiz(self):
        """1. 퀴즈 풀기"""
        state_data = load_data('state.json')
        user_data = load_data('user.json')

        if not state_data['questions']:
            print("\n[!] 풀 수 있는 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        username = input("이름을 입력하세요: ")
        user_data['username'] = username

        print(f"\n{state_data['description']}")
        quiz = Quiz(state_data['questions'])
        score, total_questions = quiz.run_quiz()

        user_data['score'] = score
        user_data['solved_count'] = total_questions
        save_data('user.json', user_data)

        print(f"\n{user_data['username']}님, 퀴즈가 끝났습니다!")
        print(f"최종 점수는 {score}점 입니다.")

class AddQuiz:
    def __init__(self):
        pass

    def add_quiz(self):
        """2. 퀴즈 추가"""
        state_data = load_data('state.json')

        question = input("문제를 입력하세요: ")
        choices = []
        for i in range(4):
            choice = input(f"{i+1}번 선택지를 입력하세요: ")
            choices.append(f"{i+1}. {choice}")
        
        answer_num = int(input("정답 번호를 입력하세요 (1-4): "))
        answer = choices[answer_num - 1]

        new_quiz = {
            "question": question,
            "choices": choices,
            "answer": answer,
            "hint": "" # 힌트는 처음엔 비워둠
        }
        state_data['questions'].append(new_quiz)
        save_data('state.json', state_data)
        print("\n[+] 퀴즈가 성공적으로 추가되었습니다.")

class QuizList:
    def view_quizzes(self):
        """3. 퀴즈 목록 보기"""
        state_data = load_data('state.json')
        print("\n--- 전체 퀴즈 목록 ---")
        print(f"퀴즈 설명: {state_data['description']}")

        if not state_data['questions']:
            print("등록된 퀴즈가 없습니다.") 
        
        for i, q in enumerate(state_data['questions'], start=1):
            print(f"{i}. {q['question']}")
            print(f"{q['choices']})")
        print("--------------------")
        
        return
        
        
class ShowScore:
    def check_score(self):
        """4. 점수 확인"""
        user_data = load_data('user.json')
        print("\n--- 최근 점수 기록 ---")
        print(f"사용자: {user_data['username']}")
        print(f"점수: {user_data['score']}점")
        print(f"푼 문제 수: {user_data['solved_count']}개")
        print("--------------------")

class AddHint:
    def add_hint(self):
        """5. 힌트 추가"""
        state_data = load_data('state.json')
        quiz_list = QuizList()
        quiz_list.view_quizzes() # 먼저 퀴즈 목록을 보여줌

        q_num = int(input("힌트를 추가할 퀴즈 번호를 선택하세요: "))
        if 1 <= q_num <= len(state_data['questions']):
            hint_text = input("추가할 힌트 내용을 입력하세요: ")
            state_data['questions'][q_num - 1]['hint'] = hint_text
            save_data('state.json', state_data)
            print("\n[+] 힌트가 추가되었습니다.")
        else:
            print("\n[!] 잘못된 번호입니다.")
class RemoveQuiz:
    def delete_quiz(self):
        """6. 퀴즈 삭제"""
        state_data = load_data('state.json')
        quiz_list = QuizList()
        quiz_list.view_quizzes()
        
        q_num = int(input("삭제할 퀴즈 번호를 선택하세요: "))

        if 1 <= q_num <= len(state_data['questions']):
            # 1. 먼저 삭제합니다.
            state_data['questions'].pop(q_num - 1) 
            print("\n[+] 퀴즈가 삭제되었습니다.")

            # 2. 삭제 후, 남은 퀴즈들의 번호를 재정렬합니다.
            for new_num, quiz in enumerate(state_data['questions'], start=1):
                quiz['question'] = str(new_num)
            
            # 3. 모든 작업이 끝난 최종 데이터를 저장합니다.
            save_data('state.json', state_data)
            print("[+] 퀴즈 번호가 재정렬되었습니다.")
        else:
            print("\n[!] 잘못된 번호입니다.")
            
class AddUser:
    def manage_user(self):
        """7. 사용자 관리"""
        while True:
            user_data = load_data('user.json')
            print(f"\n--- 사용자 관리 (현재: {user_data['username']}) ---")
            print("1. 사용자 이름 변경")
            print("2. 사용자 정보 초기화 (점수 포함)")
            print("0. 메인 메뉴로 돌아가기")
            
            try:
                choice = input("메뉴를 선택하세요: ")
                if not choice.isdigit():
                    raise InvalidInputError() # 우리가 만든 예외 활용!
                
                choice = int(choice)

                if choice == 1:
                    self._change_username(user_data)
                elif choice == 2:
                    self._reset_user_data(user_data)
                elif choice == 0:
                    print("메인 메뉴로 돌아갑니다.")
                    break
                else:
                    print("[!] 메뉴에 없는 번호입니다.")

            except InvalidInputError as e:
                print(f"\n{e}")

    def _change_username(self, user_data):
        """사용자 이름 변경 (내부 함수)"""
        new_username = input("새로운 사용자 이름을 입력하세요: ").strip()
        
        if new_username: # 입력값이 있으면
            user_data['username'] = new_username
            user_data['score'] = 0 # 사용자가 바뀌면 점수 초기화
            user_data['solved_count'] = 0
            save_data('user.json', user_data)
            print(f"\n[+] 사용자가 '{new_username}'(으)로 변경되었습니다.")
        else:
            print("\n[!] 입력이 없어 변경되지 않았습니다.")

    def _reset_user_data(self, user_data):
        """사용자 정보 초기화 (내부 함수)"""
        confirm = input("정말 모든 사용자 정보를 초기화하시겠습니까? (y/n): ").lower()
        if confirm == 'y':
            user_data['username'] = "Guest"
            user_data['score'] = 0
            user_data['solved_count'] = 0
            save_data('user.json', user_data)
            print("\n[+] 사용자 정보가 'Guest'로 초기화되었습니다.")
        else:
            print("\n취소되었습니다.")
