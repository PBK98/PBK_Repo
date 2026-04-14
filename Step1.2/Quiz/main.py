from QuizGame import * # QuizGame.py를 가져와서 그 안의 함수들을 사용하겠다.

manageuser = UserManager() # UserManager 클래스의 인스턴스를 manageuser이라는 변수에 담는다.

# -> *** SolveQuiz Class에서 UserManager Class를 사용하기 때문에 SolveQuiz보다 UserManager 인스턴스가 먼저 생성되어야함.

quizsolve = SolveQuiz(manageuser) # SolveQuiz 클래스의 인스턴스를 quizsolve이라는 변수에 담는다.
addquiz = AddQuiz() # AddQuiz 클래스의 인스턴스를 addquiz이라는 변수에 담는다.
viewquiz = QuizList() # QuizList 클래스의 인스턴스를 viewquiz이라는 변수에 담는다.
checkscore = ShowScore() # ShowScore 클래스의 인스턴스를 checkscore이라는 변수에 담는다.
addhint = AddHint() # AddHint 클래스의 인스턴스를 addhint이라는 변수에 담는다.
removequiz = RemoveQuiz() # RemoveQuiz 클래스의 인스턴스를 removequiz이라는 변수에 담는다.

if __name__ == "__main__":
    while True:
        print("\n===== 파이썬 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 점수 확인")
        print("5. 힌트 추가")
        print("6. 퀴즈 삭제")
        print("7. 사용자 관리")
        print("0. 종료")


        try:

            choice = int(input("메뉴를 선택하세요: "))

            if choice == 1:
                quizsolve.solve_quiz()
            elif choice == 2:
                addquiz.add_quiz()
            elif choice == 3:
                viewquiz.view_quizzes()
            elif choice == 4:
                checkscore.check_score()
            elif choice == 5:
                addhint.add_hint()
            elif choice == 6:
                removequiz.delete_quiz()
            elif choice == 7:
                manageuser.manage_users()
            elif choice == 0:
                print("게임을 종료합니다.")
                break
            else:
              print("\n[!] 잘못된 입력입니다. 다시 선택해주세요.")
             # ✨ InvalidInputError를 잡아서 메시지를 출력합니다.
        
        except ValueError:
            print("\n[!] 숫자로 된 메뉴 번호를 입력해주세요.")

        # ✨ KeyboardInterrupt (Ctrl+C)를 별도로 처리합니다.
        except KeyboardInterrupt:
            print("\n\n[!] 작업을 취소하고 메뉴로 돌아갑니다.")

        # ✨ 그 외 예상치 못한 모든 오류에 대한 안전망
        except Exception as e:
            print(f"\n[!] 예상치 못한 오류가 발생했습니다: {e}")
            print("메뉴로 돌아갑니다.")
