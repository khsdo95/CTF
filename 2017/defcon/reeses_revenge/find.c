unsigned int find(unsigned int seed) {
  unsigned int i;
  unsigned int arr[32];
  unsigned int v3, v4;

  arr[0] = seed;

  for(i=0; i<31; i++) {
    arr[i+1] = 0x7ffff * (((arr[i] >> 30) + i + 1) ^ arr[i]);
  }

  v3 = (arr[3] >> 8) ^ arr[0] ^ arr[3];
  v4 = (arr[10] << 14) ^ (arr[24] << 19) ^ arr[24] ^ arr[10];
  return (v4 << 13) ^ (v3 << 7) ^ v4 ^ v3 ^ (arr[31] << 11) ^ arr[31];
}

int main(int argc, char **argv) {
  unsigned int i;
  unsigned int start = atoi(argv[1]);
  unsigned int target = atoi(argv[2]);

  for(i=start; ; i++) {
    if (find(i) == target) {
      printf("%x\n", i);
      break;
    }
  }
}
