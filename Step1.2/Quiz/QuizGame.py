# QuizGame.py

import json
from Quiz import Quiz

# --- 데이터 로드/저장 함수 (이전과 동일) ---
def load_data(filename):
    try:
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

def start_quiz():
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

def add_quiz():
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

def view_quizzes():
    """3. 퀴즈 목록 보기"""
    state_data = load_data('state.json')
    print("\n--- 전체 퀴즈 목록 ---")
    if not state_data['questions']:
        print("등록된 퀴즈가 없습니다.")
        return
        
    for i, q in enumerate(state_data['questions']):
        print(f"{i+1}. {q['question']} (정답: {q['answer']})")
    print("--------------------")

def check_score():
    """4. 점수 확인"""
    user_data = load_data('user.json')
    print("\n--- 최근 점수 기록 ---")
    print(f"사용자: {user_data['username']}")
    print(f"점수: {user_data['score']}점")
    print(f"푼 문제 수: {user_data['solved_count']}개")
    print("--------------------")

def add_hint():
    """5. 힌트 추가"""
    state_data = load_data('state.json')
    view_quizzes() # 먼저 퀴즈 목록을 보여줌
    
    q_num = int(input("힌트를 추가할 퀴즈 번호를 선택하세요: "))
    if 1 <= q_num <= len(state_data['questions']):
        hint_text = input("추가할 힌트 내용을 입력하세요: ")
        state_data['questions'][q_num - 1]['hint'] = hint_text
        save_data('state.json', state_data)
        print("\n[+] 힌트가 추가되었습니다.")
    else:
        print("\n[!] 잘못된 번호입니다.")

def delete_quiz():
    """6. 퀴즈 삭제"""
    state_data = load_data('state.json')
    view_quizzes()

    q_num = int(input("삭제할 퀴즈 번호를 선택하세요: "))
    if 1 <= q_num <= len(state_data['questions']):
        state_data['questions'].pop(q_num - 1) # 리스트에서 해당 문제 삭제
        save_data('state.json', state_data)
        print("\n[+] 퀴즈가 삭제되었습니다.")
    else:
        print("\n[!] 잘못된 번호입니다.")

# --- 메인 실행 부분 ---
if __name__ == "__main__":
    while True:
        print("\n===== 파이썬 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 점수 확인")
        print("5. 힌트 추가")
        print("6. 퀴즈 삭제")
        print("0. 종료")
        choice = input("메뉴를 선택하세요: ")

        if choice == '1':
            start_quiz()
        elif choice == '2':
            add_quiz()
        elif choice == '3':
            view_quizzes()
        elif choice == '4':
            check_score()
        elif choice == '5':
            add_hint()
        elif choice == '6':
            delete_quiz()
        elif choice == '0':
            print("게임을 종료합니다.")
            break
        else:
            print("\n[!] 잘못된 입력입니다. 다시 선택해주세요.")