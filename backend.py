import pandas as pd
import time
import os
import bcrypt
import pickle
import bookfinder

# 비밀번호 해싱과 salt 추가 함수 (bcrypt 사용)
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()  # bcrypt로 salt 생성
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # 비밀번호 해시화
    return hashed_password

# 사용자 정보 관리 클래스
class UserManager:
    def __init__(self):
        self.users_file = 'users.pkl'
        # 사용자 정보를 저장할 데이터프레임 생성 (파일에서 로드)
        if os.path.exists(self.users_file):
            with open(self.users_file, 'rb') as f:
                self.users_df = pickle.load(f)
        else:
            self.users_df = pd.DataFrame(columns=['Username', 'PasswordHash'])

    def add_user(self, username: str, password: str):
        # 비밀번호를 해싱하여 저장
        hashed_password = hash_password(password)
        new_user = pd.DataFrame([[username, hashed_password]], columns=['Username', 'PasswordHash'])
        self.users_df = pd.concat([self.users_df, new_user], ignore_index=True)
        with open(self.users_file, 'wb') as f:
            pickle.dump(self.users_df, f)  # pickle로 저장

    def authenticate(self, username: str, password: str) -> bool:
        # 사용자 아이디가 존재하는지 확인
        if username in self.users_df['Username'].values:
            user_data = self.users_df[self.users_df['Username'] == username].iloc[0]
            # 입력된 비밀번호는 encode() 후 bcrypt.checkpw로 비교
            return bcrypt.checkpw(password.encode('utf-8'), user_data['PasswordHash'])
        return False

# 책 정보 기록 클래스
class logger:
    def __init__(self):
        # DataFrame 생성
        self.columns = ["Name", "Author", "Year", "Month", "Day", "Hour", "Minute", "Second", "Memo", "Username"]
        # CSV 파일에서 기존에 저장된 책 정보를 불러옵니다.
        if os.path.exists('book_log.csv'):
            self.df = pd.read_csv('book_log.csv')
        else:
            self.df = pd.DataFrame(columns=self.columns)

    def timelog(self, y, m, d, h, mi, s):  # 시간 로거
        self.y = y
        self.m = m
        self.d = d
        self.h = h
        self.mi = mi
        self.s = s

    def bookinfolog(self, name, author):  # 책 정보 로거
        self.name = name
        self.author = author

    def memolog(self, memo):  # 메모 로거
        self.memo = memo

    def save_to_df(self, username):  # 입력된 정보를 DataFrame에 추가
        new_data = [self.name, self.author, self.y, self.m, self.d, self.h, self.mi, self.s, self.memo, username]
        self.df.loc[len(self.df)] = new_data

    def save_to_csv(self):  # DataFrame을 CSV 파일로 저장
        self.df.to_csv('book_log.csv', index=False)  # 파일이 없다면 생성하고, 있으면 덮어씀

    def view_books(self, username):  # 사용자가 등록한 책 목록 조회
        # 사용자 이름에 해당하는 책만 필터링하여 출력
        user_books = self.df[self.df['Username'] == username]
        if user_books.empty:
            print("등록된 책이 없습니다.")
        else:
            print(user_books[['Name', 'Author', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'Memo']])

    def output(self):
        print(self.name + " " + self.author + " " + self.y + "/" + self.m + "/" + self.d + "/" + self.h + "/" + self.mi + "/" + self.s + " " + self.memo)

# 사용자 관리 및 데이터 입력 함수
def runner():
    user_manager = UserManager()

    state = input("N: 신규 사용자 등록, C: 로그인 : ")
    if state == 'N':
        # 사용자 등록
        username = input("사용자 아이디를 입력해주세요: ")
        password = input("사용자 비밀번호를 입력해주세요: ")
        user_manager.add_user(username, password)
        print("사용자가 등록되었습니다.")

    # 로그인 절차
    login_username = input("로그인 아이디를 입력해주세요: ")
    login_password = input("로그인 비밀번호를 입력해주세요: ")

    if user_manager.authenticate(login_username, login_password):
        print("로그인 성공!")
        log = logger()

        # 책 등록 여부
        while True:
            action = input("책을 등록하시겠습니까? (Y: 등록, V: 등록한 책 보기, Q: 종료): ").upper()
            if action == 'Y':
                # 책 정보 입력
                name, author = map(str, input("책 제목과 저자를 입력해주세요 : ").split())
                log.bookinfolog(name, author)

                state = input("책을 읽으신 년 원 일 시를 입력해주세요 (N을 입력 시 현재 시간이 적용됩니다.) : ")
                if state == 'N':
                    timestamp = time.time()
                    lt = time.localtime(timestamp)
                    formatted = time.strftime("%Y,%m,%d,%H,%M,%S", lt)
                    y, m, d, h, mi, s = map(str, formatted.split(','))
                    log.timelog(y, m, d, h, mi, s)
                else:
                    y, m, d, h = map(str, state.split())
                    log.timelog(y, m, d, h, '0', '0')

                memo = input("간단한 메모가 있으면 남겨주세요 : ")
                if memo == '':
                    memo = "메모없음"
                
                log.memolog(memo)

                state = input("책 검색 기능 활성화? : Y / N : ")
                if state == 'Y':
                    bookfinder.find()

                # 로그를 DataFrame에 저장
                log.save_to_df(login_username)

                # DataFrame을 CSV 파일로 저장
                log.save_to_csv()

                # 로그 출력
                log.output()

            elif action == 'V':
                log.view_books(login_username)  # 등록한 책 보기

            elif action == 'Q':
                print("프로그램을 종료합니다.")
                break

            else:
                print("잘못된 입력입니다. 다시 시도해주세요.")

    else:
        print("로그인 실패! 아이디 또는 비밀번호를 확인해주세요.")

runner()
