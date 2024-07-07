## DUH to ENG Example
한글 모드로 쳐버린 영타를 영어로 바뀌주는 Python Example Code입니다. (기준 : 두벌식)<br>
지금은 파이썬 3이면 전부 다 동작하는 것 같지만 아마 해당 작업을 역으로 수행하는 gks2han는 match-case문을 쓸 것 같아서 나중에는 파이썬 3.10버전 이상에서만 동작할 것 같습니다.<br>
Change english sentence/word typed with dubeolsik korean keyboard, as korean mode, to english.<br>
At now you just need python 3, but future you will need python 3.10+ because I'll use match-case to gks2han.<br>
gks2han은 아직 만드는 중입니다. gks2han is not completed.

### example
```
C:\Programming\SkyWare\duh2eng_example>python main.py
테스트용 문장 입력 : ㅑ ㅈ뭇 새 해 새 ㅏㅕㄱ묘ㅐ노ㅑ! ㅏㅕㄱ묘ㅐ노ㅑ ㅑㄴ ㅁ ㅣㅐㅊㅁ샤ㅐㅜ ㅐㄹ ㅗㅑㅜ뮤ㅑㅅㅁ.
결과               : I want to go to kurayoshi! kurayoshi is a location of hinabita.
```