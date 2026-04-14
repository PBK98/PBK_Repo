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

# --- 메뉴 기능별 함수 ---

# QuizGame.py 파일

class UserManager:
    # ✨ 1. __init__에서 데이터를 '한 번만' 불러와 self에 저장합니다.
    def __init__(self, user_filepath='user.json'):
        """
        UserManager가 생성될 때 사용자 데이터를 불러와 self.users에 저장합니다.
        현재 선택된 사용자인 self.current_user는 None으로 초기화합니다.
        """
        self.filepath = user_filepath
        self.users = load_data(self.filepath) # user.json 데이터를 객체 안에 보관
        self.current_user = None # 현재 사용자를 객체 안에 보관 (처음엔 없음)

    # ✨ 2. 데이터를 파일에 저장하는 기능을 별도 메서드로 분리합니다.
    def save_users(self):
        """현재 self.users에 있는 데이터를 파일에 저장합니다."""
        save_data(self.filepath, self.users)

    # ✨ 3. 이제 메서드들은 self.users를 사용합니다. (파일을 매번 읽지 않음)
    def _list_users(self):
        """현재 등록된 모든 사용자를 출력 (self.users 기반)"""
        print("\n[ 등록된 사용자 목록 ]")
        if not self.users:
            print("- 등록된 사용자가 없습니다.")
            return
        for username, data in self.users.items():
            print(f"- {username}")

    def _add_user(self):
        """새로운 사용자를 self.users에 추가하고 파일에 저장"""
        new_username = input("추가할 사용자 이름을 입력하세요: ").strip()
        if not new_username:
            print("\n[!] 사용자 이름은 공백일 수 없습니다.")
            return

        if new_username in self.users:
            print(f"\n[!] '{new_username}' 사용자는 이미 존재합니다.")
        else:
            self.users[new_username] = {"score": 0, "solved_count": 0}
            self.save_users() # 변경사항을 파일에 저장
            print(f"\n[+] 사용자 '{new_username}'이(가) 추가되었습니다.")

    # ✨ 4. select_user_for_game이 self.current_user를 직접 설정합니다.
    def select_user_for_game(self):
        """퀴즈를 풀 사용자를 선택하고, self.current_user에 저장합니다."""
        self._list_users()
        username = input("사용자 이름을 입력하세요 (취소하려면 엔터): ").strip()

        if not username:
            print("사용자 선택을 취소했습니다.")
            self.current_user = None # 취소 시 초기화
            return False

        if username in self.users:
            self.current_user = username  # ✨ state.json 대신 여기에 바로 저장!
            print(f"\n[+] '{self.current_user}'님, 환영합니다! 퀴즈를 시작합니다.")
            return True
        else:
            print(f"\n[!] '{username}' 사용자를 찾을 수 없습니다.")
            self.current_user = None
            return False

    # ✨ 5. SolveQuiz에서 필요로 하는 메서드들을 추가합니다.
    def update_score(self, score_to_add):
        """현재 사용자의 점수와 푼 횟수를 업데이트합니다."""
        if self.current_user and self.current_user in self.users:
            self.users[self.current_user]['score'] += score_to_add
            self.users[self.current_user]['solved_count'] += 1
            self.save_users() # 점수 변경 후 파일 저장
            print(f"'{self.current_user}'님의 정보가 업데이트되었습니다.")
        else:
            print("[!] 점수를 업데이트할 사용자가 선택되지 않았습니다.")

    def get_current_user_data(self):
        """현재 선택된 사용자의 전체 데이터를 반환합니다."""
        if self.current_user:
            return self.users.get(self.current_user)
        return None



    def _rename_user(self):
        """사용자 이름을 변경합니다."""
        old_username = input("이름을 변경할 사용자 이름을 입력하세요: ").strip()

        if old_username not in self.users:
            print(f"\n[!] '{old_username}' 사용자를 찾을 수 없습니다.")
            return

        new_username = input("새 사용자 이름을 입력하세요: ").strip()
        if not new_username:
            print("\n[!] 새 사용자 이름은 공백일 수 없습니다.")
            return
        if new_username in self.users:
            print(f"\n[!] '{new_username}' 이름은 이미 사용 중입니다.")
            return

        # 딕셔너리에서 키 이름을 변경하는 가장 일반적인 방법입니다.
        # 기존 데이터를 꺼내서(pop) 새 이름으로 저장합니다.
        self.users[new_username] = self.users.pop(old_username)
        
        # 만약 현재 로그인된 사용자의 이름을 바꾼 경우, self.current_user도 업데이트 해줍니다.
        if self.current_user == old_username:
            self.current_user = new_username
            print(f"[!] 현재 사용자의 이름이 '{new_username}'(으)로 변경되었습니다.")

        self.save_users() # 변경사항을 파일에 저장
        print(f"\n[+] '{old_username}' -> '{new_username}'(으)로 이름이 변경되었습니다.")

    def _delete_user(self):
        """사용자를 삭제합니다."""
        username_to_delete = input("삭제할 사용자 이름을 입력하세요: ").strip()

        if username_to_delete not in self.users:
            print(f"\n[!] '{username_to_delete}' 사용자를 찾을 수 없습니다.")
            return

        # 실수를 방지하기 위해 한 번 더 확인합니다.
        confirm = input(f"정말 '{username_to_delete}' 사용자를 삭제하시겠습니까? (y/n): ").lower()
        if confirm == 'y':
            del self.users[username_to_delete]

            # 만약 현재 사용자를 삭제했다면, 선택되지 않은 상태로 되돌립니다.
            if self.current_user == username_to_delete:
                self.current_user = None
                print("[!] 현재 사용자가 삭제되어 로그아웃 처리됩니다.")

            self.save_users() # 변경사항을 파일에 저장
            print(f"\n[+] '{username_to_delete}' 사용자가 삭제되었습니다.")
        else:
            print("\n삭제가 취소되었습니다.")

    # ✨ 이 부분이 바로 학생분이 원하셨던 '관리 메뉴' 기능입니다!
    def manage_users(self):
        """사용자 관리 메뉴를 표시하고 관련 기능을 실행합니다."""
        while True:
            # 요청하신 대로, 메뉴를 보여주기 전에 항상 목록을 먼저 출력합니다.
            self._list_users() 
            
            print("\n--- 사용자 관리 메뉴 ---")
            print("  1. 사용자 추가")
            print("  2. 사용자 이름 변경")
            print("  3. 사용자 삭제")
            print("  4. 메인 메뉴로 돌아가기")
            
            choice = input(">> 선택: ").strip()

            if choice == '1':
                self._add_user()
            elif choice == '2':
                self._rename_user()
            elif choice == '3':
                self._delete_user()
            elif choice == '4':
                print("\n메인 메뉴로 돌아갑니다.")
                break # while 루프를 종료하고 메서드를 빠져나갑니다.
            else:
                print("\n[!] 잘못된 입력입니다. 1~4 사이의 숫자를 입력해주세요.")

class SolveQuiz:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def solve_quiz(self):
        """1. 퀴즈 풀기 (힌트 기능 및 점수 차감 추가)"""
        if not self.user_manager.select_user_for_game():
            return

        try:
            state_data = load_data('state.json')
            questions = state_data['questions']
        except (FileNotFoundError, KeyError):
            print("\n[!] 퀴즈 데이터를 불러올 수 없습니다.")
            return

        if not questions:
            print("\n[!] 풀 수 있는 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        current_user_name = self.user_manager.current_user
        print(f"\n--- {current_user_name}님, 퀴즈를 시작합니다! ---")
        
        score = 0
        for quiz in questions:
            # ✨ 1. 각 문제마다 얻을 수 있는 점수를 10점으로 초기화합니다.
            points_for_this_question = 10

            print(f"\n문제: {quiz['question']}")
            for i, choice in enumerate(quiz['choices']):
                print(f"{choice}")

            # ✨ 2. 힌트가 있는지 확인하고, 사용자에게 사용 여부를 묻습니다.
            # .get('hint')는 힌트가 없거나(key 자체가 없음) 비어있을 때(value가 "") None이나 빈 문자열을 반환합니다.
            if quiz.get('hint'):
                use_hint = input("힌트를 보시겠습니까? (y/n) (사용 시 5점 차감): ").strip().lower()
                if use_hint == 'y':
                    print(f"💡 힌트: {quiz['hint']}")
                    points_for_this_question -= 5 # 힌트를 사용하면 점수를 5점 차감합니다.

            # 사용자 입력 받기 (이전과 동일)
            try:
                user_choice = int(input("번호를 입력하세요: ").strip())
                
                # ✅ 사용자가 입력한 '숫자'가 범위 안에 있는지 먼저 확인합니다.
                if not (1 <= user_choice <= 4):
                    # 1~4 범위를 벗어나면 에러를 발생시킵니다.
                    raise ValueError
                
                # 범위를 통과했다면, 그 다음에 정답 텍스트를 가져옵니다.
                user_answer = quiz['choices'][user_choice - 1]

            except ValueError:
                raise InvalidInputError("정답은 1-4 사이의 숫자로 입력해야 합니다.")

            # ✨ 3. 정답 확인 시, 고정된 10점이 아닌 '이번 문제의 점수'를 더합니다.
            if user_answer == quiz['answer']:
                print(f"정답입니다! +{points_for_this_question}점")
                score += points_for_this_question # 힌트를 썼다면 5점, 안 썼다면 10점이 더해집니다.
            else:
                print(f"오답입니다.")
        
        # 점수 업데이트 및 결과 출력 (이전과 동일)
        print(f"\n--- 퀴즈 종료! ---")
        print(f"{current_user_name}님의 이번 게임 점수는 {score}점입니다.")
        
        self.user_manager.update_score(score)

        user_profile = self.user_manager.get_current_user_data()
        if user_profile:
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
            