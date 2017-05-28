# badint ( 2017 defcon quals )

## descriptdion
SEQ 와 Offset, 그리고 Data 를 입력 받아서 저장한다. 기능 자체는 단순하지만 많은 구조체를 이용해서 코드가 복잡하다. 대충 인풋을 저장하는 구조체, 출력하는 데이터를 위한 구조체 (LSF를 Yes로 했을 때), 그리고 전체 SEQ를 관리하는 구조체 등이 있는 것 같다.

## vulnerability
LSF를 Yes로 줬을 때, 출력을 위해 만드는 구조체에 데이터를 복사하는데 이 때
```
malloc(len);
...
memcpy(dst + offset, src, len);
```
이렇게 데이터를 복사한다. offset은 우리가 임의로 주는 값이므로 heap overflow를 일으킬 수 있다.

## exploit
문제를 푼 방법이 정밀한 분석을 통해서 한 것이 아니라, pwndbg의 힘으로 풀었다.

일단, offset 을 8로 주고 fastbin을 초과하는 사이즈로 할당받으면 데이터를 출력할 때 앞의 8 바이트가 이전의 값이 그대로 출력된다. 그리고 이것은 main_arena + 88 이다.

libc 주소 릭을 얻은 다음, fastbin에 해당되면서 사이즈 차이가 나도록 두 개의 SEQ를 할당받은 후, pwndbg로 힙 상태를 보면 0x20의 fastbin 하나와 0x70의 fastbin 이 freelist에 들어와 있는 걸 볼 수 있다. 이 상태에서 0x20의 청크를 할당받는데, offset을 0x70 fastbin free chunk의 fd 포인터를 덮을 수 있도록 준다.

fd pointer를 malloc_hook 근처의 곳으로 준다. 이 때 size가 맞아야 하므로 사이즈가 0x7f가 되도록 잘 조절한다.

그리고 0x70 fastbin이 할당될 크기의 데이터를 주면서 oneshot gadget으로 malloc_hook을 덮는다.

