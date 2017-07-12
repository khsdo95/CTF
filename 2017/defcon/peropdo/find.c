#include<stdio.h>
#include<stdlib.h>
int main(){
  int i, j, tmp;
  int val = 0x080507b6;
  for(i=0; i<0xffffffff; i++){
    srand(i);
    for(j=0; j<24; j++)
      rand();
    for(j=0; j<100000; j++){
      tmp = rand();
      if (val == tmp){
        printf("seed %d\n", i);
        printf("count %d\n", j + 24);
        break;
      }
    }
  }
}
