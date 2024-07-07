자모음 = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
자모음conv = ['r', 'R', 'rt', 's', 'sw', 'sg', 'e', 'E', 'f', 'fr', 'fa', 'fq', 'ft', 'fx', 'fv', 'fg', 'a', 'q', 'Q', 'qt', 't', 'T', 'd', 'w', 'W', 'c', 'z', 'x', 'v', 'g', 'k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l']
초성 = ['r', 'R', 's', 'e', 'E', 'f', 'a', 'q', 'Q', 't', 'T', 'd', 'w', 'W', 'c', 'z', 'x', 'v', 'g']
중성 = ['k', 'o', 'i', 'O', 'j', 'p', 'u', 'P', 'h', 'hk', 'ho', 'hl', 'y', 'n', 'nj', 'np', 'nl', 'b', 'm', 'ml', 'l']
종성 = ['', 'r', 'R', 'rt', 's', 'sw', 'sg', 'e', 'f', 'fr', 'fa', 'fq', 'ft', 'fx', 'fv', 'fg', 'a', 'q', 'qt', 't', 'T', 'd', 'w', 'c', 'z', 'x', 'v', 'g']

def duh2eng(arg:str) -> str:
    result = ''
    for i in arg:
        code = ord(i)
        if code >= 0xac00 and code <= 0xd7a3:
            code -= 0xac00
            result += 초성[code // (len(중성) * len(종성))] + 중성[(code % (len(중성) * len(종성))) // len(종성)] + 종성[code % len(종성)]
        else:
            if i in 자모음:  result += 자모음conv[자모음.index(i)]
            else:  result += i
    return result

def gks2han(arg:str) -> str:
    result = ''
    mode = 0
    code = 0
    pending_char = ''
    for i in arg:
        if i not in 'QWERT':
            i = i.lower()
        match mode:
            case 0: # 버퍼에 아무것도 없는 경우
                if i in 초성:
                    code = (초성.index(i) * len(중성) * len(종성))
                    mode = 1
                else: #맨 처음에 중성이 나온 경우, 초성도 중성도 아니면 error 뜨겠지. 어짜피 정상적인 글자가 안 됨
                    result += 자모음conv[중성.index(i) + 30]
            case 1: # 버퍼에 초성이 들어가 있는 경우
                if i in 중성: #정상적으로 중성이 나온 경우, 이거 h n m는 pending 처리 해 줘야 함(모드 7로)
                    code += (중성.index(i) * len(종성))
                    mode = 2
                else: #초성 다음에 초성이 나온 경우, 초성도 중성도 아니면 error 뜨겠지.
                    result += chr(0x1100 + (code // (len(중성) * len(종성))))
                    code = (초성.index(i) * len(중성) * len(종성))
            case 2: # 버퍼에 초성 + 중성이 들어가 있는 경우
                if i in 종성: #자음이 나온 경우, 일단 판정 보류
                    pending_char = i
                    mode = 3
                else: #모음이 나온 경우, 자ㅑ 이런 식이라서 버퍼에 있는 글자 + 그 글자를 추가해버리고 모드 0으로 되돌림
                    result += chr(0xac00 + code) + 자모음conv[중성.index(i) + 30]
                    mode = 0
            case 3: # 버퍼에 초성 + 중성 + 종성1글자가 들어가 있는 경우
                if i in 종성: # 또 다시 자음이 나옴
                    if (pending_char + i) in 종성: #만약 ㄳ, ㄵ, ㄻ, ㅄ 같은 겹받침이면 또 pending (날무 s k f a (n), 낢이 s k f a (d) 의 두가지 가능성이 있음)
                        pending_char += i
                        mode = 4
                    else: #강한 r k d g 같은 경우, ㅇㅎ이 합쳐질 수는 없으니까 이미 끝난 거
                          #code에 pending_char을 더해 result에 추가하고 다시 현재 나온 글자를 code로 한 다음 mode 1로
                        code += 종성.index(pending_char)
                        result += chr(0xac00 + code)
                        code = (초성.index(i) * len(중성) * len(종성))
                        mode = 1
                else: #r k s 가 나온 상태에서 k가 나온 경우 (가나) : 가를 result에 추가, 버퍼(code)는 나, mode는 2 또는 7
                    pass
            case 4: # 버퍼에 초성 + 중성 + 종성2글자가 들어가 있는 경우
                if i in 종성: # 종성이 나옴 : 값어치 r k q t d 같은 경우, ㅄㅇ이 합쳐질 수는 없으니까
                              # ㅄ을 더한 다음에 ㅇ은 code로 놔두고 모드 1로
                        code += 종성.index(pending_char)
                        result += chr(0xac00 + code)
                        code = (초성.index(i) * len(중성) * len(종성))
                        mode = 1
                else: # 간나 r k s s k 같은 경우
                      # code에 pending_char[0]을 더해 result에 추가, code는 pending_char[1]에 i를 한 걸로 함, mode는 2 또는 7
                      # 이 부분 위쪽에서 예외처리 하면 수정해줘야 함
                    code += 종성.index(pending_char[0])
                    result += chr(0xac00 + code)
                    code = (초성.index(pending_char[1]) * len(중성) * len(종성)) + (중성.index(i) * len(종성))
                    mode = 2
            case 7: #모음 예외처리
                pass

def __알아서__(arg:str):
    ko_exist = False
    for i in arg:
        if i >= 0xac00 and i <= 0xd7a3:
            ko_exist = True
            break
    if ko_exist:
        return duh2eng(arg)
    else:
        return gks2han(arg)

if __name__ == '__main__':
    print(f'결과               : {__알아서__(input('테스트용 문장 입력 : ')).capitalize()}')