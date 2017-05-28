# peROPdo ( 2017 defcon quals )

## description

처음에 시작하면서 이름을 입력받고, 원하는만큼 랜덤값을 뽑아 스택에 넣을 수 있다.
랜덤값을 뽑는 방식은 이름의 맨 앞 4바이트를 이용해서 srand를 부르고, 그 다음부터 rand()를 통해서 뽑는다.

## vulnerability

취약점은 크게 두 가지가 존재한다.
1. name 에서 bof
2. 랜덤값으로 stack bof

## exploit

처음에 삽질을 좀 많이 했는데, name에서 발생하는 bof로 data 영역을 잘 덮으면 eip가 컨트롤 됨을 발견했다. 그래서 이걸 써서 exploit 하려고 노력해봤는데 망했다. 그 당시 스택의 인자도 쓸모 없고, 한 번에 뛰어서 성공할만한 곳도 없었다.

그래서 방향을 돌려서 랜덤값을 맞추기로 했다. stack bof를 만들때, 랜덤값 24개면 ret를 덮을 수 있고 ret뒤에 바로 name buffer의 주소가 들어있기때문에 pop esp 가젯을 이용해서 name buffer를 커스텀 스택으로 만들고, name buffer에 rop chain을 넣어두는 방법을 이용했다.

* nosolve.py 는 처음의 익스플로잇 시도로 eip 컨트롤까지 한 것.
* solve.py 가 두 번째 방법으로 끝까지 익스플로잇 한 것.
* find.c 는 pop esp; ~~~ ; ret 가젯으로 뛰기 위한 랜덤시드와 랜덤 횟수를 찾는 코드
