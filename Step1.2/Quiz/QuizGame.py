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

class UserManager:
    def user_manager(self):
        """7. 사용자 관리 메뉴"""
        while True:
            # 최신 데이터를 항상 다시 불러옵니다.
            state_data = load_data('state.json')
            current_user = state_data.get('current_user', 'Guest') # .get()으로 안전하게 값 가져오기

            print(f"\n--- 사용자 관리 (현재 사용자: {current_user}) ---")
            self._list_users() # 메뉴를 보여주기 전에 항상 목록을 먼저 출력
            
            print("\n1. 사용자 추가")
            print("2. 사용자 선택")
            print("3. 사용자 삭제")
            print("0. 메인 메뉴로 돌아가기")

            try:
                choice = input("메뉴를 선택하세요: ").strip()
                if not choice.isdigit():
                    raise InvalidInputError()
                
                choice = int(choice)

                if choice == 1:
                    self._add_user()
                elif choice == 2:
                    self._select_user()
                elif choice == 3:
                    self._delete_user()
                elif choice == 0:
                    print("메인 메뉴로 돌아갑니다.")
                    break
                else:
                    print("\n[!] 메뉴에 없는 번호입니다.")
            
            except InvalidInputError as e:
                print(f"\n{e}")

    def select_user_for_game(self):
        """퀴즈를 풀기 전, 플레이할 사용자를 선택하는 기능"""
        print("\n--- 플레이할 사용자를 선택하세요 ---")
        self._list_users() # 기존에 만들어둔 사용자 목록 보여주기 메서드 재사용!
        
        users_data = load_data('user.json')
        if not users_data:
            print("\n[!] 등록된 사용자가 없습니다. 'Guest'로 플레이합니다.")
            # state.json의 current_user를 'Guest'로 확실히 해줍니다.
            state_data = load_data('state.json')
            state_data['current_user'] = "Guest"
            save_data('state.json', state_data)
            return True # Guest로 게임을 계속 진행

        while True:
            username_to_select = input("사용자 이름을 입력하세요 (취소하려면 엔터): ").strip()

            if not username_to_select: # 그냥 엔터를 치면
                print("사용자 선택을 취소하고 메인 메뉴로 돌아갑니다.")
                return False # 게임 시작을 취소한다는 의미로 False 반환

            if username_to_select in users_data:
                state_data = load_data('state.json')
                state_data['current_user'] = username_to_select
                save_data('state.json', state_data)
                print(f"\n[+] '{username_to_select}'님, 환영합니다! 퀴즈를 시작합니다.")
                return True # 사용자를 성공적으로 선택했으니 True 반환
            else:
                print(f"\n[!] '{username_to_select}' 사용자를 찾을 수 없습니다. 다시 입력해주세요.")

    def _list_users(self):
        """현재 등록된 모든 사용자를 출력"""
        users_data = load_data('user.json')
        print("\n[ 등록된 사용자 목록 ]")
        if not users_data:
            print("- 등록된 사용자가 없습니다.")
            return
        # items()를 사용해 이름과 점수 정보를 함께 출력
        for username, data in users_data.items():
            print(f"- {username} (점수: {data.get('score', 0)})")

    def _add_user(self):
        """새로운 사용자를 추가"""
        new_username = input("추가할 사용자 이름을 입력하세요: ").strip()
        if not new_username:
            print("\n[!] 사용자 이름은 공백일 수 없습니다.")
            return

        users_data = load_data('user.json')
        if new_username in users_data:
            print(f"\n[!] '{new_username}' 사용자는 이미 존재합니다.")
        else:
            users_data[new_username] = {"score": 0, "solved_count": 0}
            save_data('user.json', users_data)
            print(f"\n[+] 사용자 '{new_username}'이(가) 추가되었습니다.")

    def _select_user(self):
        """플레이할 사용자를 선택"""
        users_data = load_data('user.json')
        username_to_select = input("선택할 사용자 이름을 입력하세요: ").strip()

        if username_to_select in users_data:
            state_data = load_data('state.json')
            state_data['current_user'] = username_to_select
            save_data('state.json', state_data)
            print(f"\n[+] 현재 사용자가 '{username_to_select}'(으)로 변경되었습니다.")
        else:
            print(f"\n[!] '{username_to_select}' 사용자를 찾을 수 없습니다.")

    def _delete_user(self):
        """사용자를 삭제"""
        users_data = load_data('user.json')
        username_to_delete = input("삭제할 사용자 이름을 입력하세요: ").strip()

        if username_to_delete not in users_data:
            print(f"\n[!] '{username_to_delete}' 사용자를 찾을 수 없습니다.")
            return
        
        if username_to_delete == "Guest":
            print("\n[!] 'Guest' 사용자는 삭제할 수 없습니다.")
            return

        confirm = input(f"정말 '{username_to_delete}' 사용자를 삭제하시겠습니까? (y/n): ").lower()
        if confirm == 'y':
            # 삭제하려는 유저가 현재 유저라면, Guest로 변경
            state_data = load_data('state.json')
            if state_data['current_user'] == username_to_delete:
                state_data['current_user'] = "Guest"
                save_data('state.json', state_data)
                print("[!] 현재 사용자가 삭제되어 'Guest'로 변경됩니다.")

            del users_data[username_to_delete]
            save_data('user.json', users_data)
            print(f"\n[+] '{username_to_delete}' 사용자가 삭제되었습니다.")
        else:
            print("\n삭제가 취소되었습니다.")

class SolveQuiz:
    def __init__(self, user_manager):
        """
        SolveGame 클래스를 초기화합니다.
        UserManager 인스턴스를 받아 사용자 선택 기능을 사용합니다.
        """
        self.user_manager = user_manager # UserManager 인스턴스를 self.user_manager에 저장

    # QuizGame.py 파일의 SolveQuiz 클래스 안에 있는 메서드입니다.

    def solve_quiz(self):
        """1. 퀴즈 풀기 (state.json 기반, 객관식 로직 유지)"""
        if not self.user_manager.select_user_for_game():
            return

        # --- ✨ 다시 이 부분을 추가합니다! ---
        # 1. state.json 파일에서 현재 게임 상태(사용자, 문제)를 불러옵니다.
        try:
            state_data = load_data('state.json')
            questions = state_data['questions']
        except (FileNotFoundError, KeyError):
            # state.json이 없거나, 파일 안에 'questions' 키가 없을 경우
            print("\n[!] 게임 상태를 불러올 수 없습니다. 퀴즈를 시작할 수 없습니다.")
            return

        if not questions:
            print("\n[!] 풀 수 있는 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        current_user = self.user_manager.current_user
        print(f"\n--- {current_user}님, 퀴즈를 시작합니다! ---")
        
        score = 0
        # --- ✨ 순회 대상을 self.quizzes에서 questions로 변경합니다. ---
        for quiz in questions:
            # 이 아래의 객관식 로직은 우리가 방금 만든 것을 그대로 사용합니다.
            print(f"\n문제: {quiz['question']}")

            # 1. 선택지 보여주기
            for i, choice in enumerate(quiz['choices']):
                print(f"  {i+1}. {choice}")

            # 2. 사용자 입력 받기 (숫자로)
            try:
                user_choice = int(input("번호를 입력하세요: ").strip())
                user_answer = quiz['choices'][user_choice - 1]
            except (ValueError, IndexError):
                print("잘못된 입력입니다. 오답으로 처리됩니다.")
                user_answer = ""

            # 3. 정답 확인하기
            if user_answer == quiz['answer']:
                print("정답입니다!")
                score += 10
            else:
                print(f"오답입니다. 정답은 '{quiz['answer']}' 입니다.")
        
        # 점수 업데이트
        self.user_manager.update_score(score)
        user_profile = self.user_manager.get_current_user_data()

        print(f"\n--- 퀴즈 종료! ---")
        print(f"{current_user}님의 이번 게임 점수는 {score}점입니다.")
        print(f"총 점수: {user_profile['score']}점")


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
        """4. 점수 확인 (모든 사용자)"""
        users_data = load_data('user.json') # user.json 파일을 불러옵니다.
        
        print("\n--- 전체 사용자 점수 ---")
        
        # 등록된 사용자가 한 명도 없는 경우를 처리합니다.
        if not users_data:
            print("등록된 사용자가 없습니다.")
            print("--------------------")
            return

        # .items()를 사용해 딕셔너리의 키(사용자 이름)와 값(점수 정보)을 모두 가져와 반복합니다.
        for username, data in users_data.items():
            # 각 사용자의 이름, 점수, 푼 횟수를 형식에 맞춰 출력합니다.
            # .get()을 사용하면 혹시 키가 없더라도 오류 대신 기본값(0)을 반환해 안전합니다.
            score = data.get('score', 0)
            solved_count = data.get('solved_count', 0)
            print(f"- {username}: 점수 {score}점, 푼 횟수 {solved_count}회")
            
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
            