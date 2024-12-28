import pandas as pd
import time

import bookfinder

class logger:
    def __init__(self):
        pass

    def timelog(self, y, m, d, h, mi, s): #시간 로거
        self.y = y
        self.m = m
        self.d = d
        self.h = h
        self.mi = mi
        self.s = s

    def bookinfolog(self, name, author): #책 정보 로거
        self.name = name
        self.author = author

    def memolog(self, memo): #메모 로거
        self.memo = memo

    def output(self):
        print(self.name + " " + self.author + " " + self.y + "/" + self.m + "/" + self.d + "/" + self.h + "/" + self.mi + "/" + self.s + " " + self.memo)


def runner(): #메인로직
    log = logger()
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

    #logpart
    log.output()

runner() #실행