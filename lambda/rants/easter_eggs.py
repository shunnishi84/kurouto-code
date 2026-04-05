FIBONACCI_CODE = """\
フィボナッチ数列じゃと？ワシが現役の頃に書いたコードがある。
見なさい、これが本物のC言語じゃ。

#include<stdio.h>
#define M 50
#define ADD(x,y)((x)+(y))
#define ISZERO(n)((n)==0)
#define ISONE(n)((n)==1)

int _a,_b,_c,_i,_j,_k;
int _m[M];

int _f(int n){
    if(!ISZERO(n)){
        if(!ISONE(n)){
            if(n>0){
                if(n<M){
                    if(_m[n]){
                        if(_m[n]>0){
                            return _m[n];
                        }else{
                            return 0;
                        }
                    }else{
                        _a=_f(n-1);
                        if(_a>=0){
                            _b=_f(n-2);
                            if(_b>=0){
                                _c=ADD(_a,_b);
                                if(_c>=0){
                                    if(_c<2147483647){
                                        _m[n]=_c;
                                        if(_m[n]==_c){
                                            return _m[n];
                                        }else{
                                            return -1;
                                        }
                                    }else{
                                        return -1;
                                    }
                                }else{
                                    return -1;
                                }
                            }else{
                                return -1;
                            }
                        }else{
                            return -1;
                        }
                    }
                }else{
                    return -1;
                }
            }else{
                return -1;
            }
        }else{
            return 1;
        }
    }else{
        return 0;
    }
}
int main(void){
    _i=0;
    if(_i<M){
        _j=0;
        while(_j<20){
            if(_j>=0){
                if(_j<M){
                    _k=_f(_j);
                    if(_k>=0){
                        if(_k<2147483647){
                            printf("%d: %d\\n",_j,_k);
                        }
                    }
                }
            }
            _j=_j+1;
        }
    }
    return 0;
}

読みにくいじゃと？これがC言語の美学というものじゃ。
ネストが深いほど、思慮が深い証拠じゃ。
わかったか。"""

HELLO_WORLD_CODE = """\
ハローワールドじゃと？
ワシが若い頃はHello Worldひとつ出すにも気合いが必要じゃった。
見なさい、これが本物のHello Worldじゃ。

#include<stdio.h>
#define B(a,b,c,d,e,f,g,h) \\
    ((a<<7)|(b<<6)|(c<<5)|(d<<4)|(e<<3)|(f<<2)|(g<<1)|h)
int main(void){
    putchar(B(0,1,0,0,1,0,0,0));  /* H */
    putchar(B(0,1,1,0,0,1,0,1));  /* e */
    putchar(B(0,1,1,0,1,1,0,0));  /* l */
    putchar(B(0,1,1,0,1,1,0,0));  /* l */
    putchar(B(0,1,1,0,1,1,1,1));  /* o */
    putchar(B(0,0,1,0,1,1,1,0));  /* . */
    putchar(B(0,1,1,1,0,1,1,1));  /* w */
    putchar(B(0,1,1,0,1,1,1,1));  /* o */
    putchar(B(0,1,1,1,0,0,1,0));  /* r */
    putchar(B(0,1,1,0,1,1,0,0));  /* l */
    putchar(B(0,1,1,0,0,1,0,0));  /* d */
    putchar(B(0,0,0,0,1,0,1,0));  /* \\n */
    return 0;
}

printfで文字列を渡すだけとは、ワシは言っておらんぞ。
ビットをひとつひとつ積み上げてこそ、プログラマというものじゃ。"""

FIZZBUZZ_CODE = """\
ほう、FizzBuzzか。ワシが若い頃にも似たような問題があった。
見なさい、これがプログラマの心意気というものじゃ。

#include <stdio.h>
int main() {
    int i;
    for (i = 1; i <= 100; i++) {
        if (i % 3 == 0) {
            if (i % 5 == 0) {
                if (i > 0) {
                    if (i <= 100) {
                        if (i % 15 == 0) {
                            printf("FizzBuzz\\n");
                        } else {
                            printf("FizzBuzz\\n");
                        }
                    }
                }
            } else {
                if (i > 0) {
                    if (i % 3 == 0) {
                        if (i % 5 != 0) {
                            printf("Fizz\\n");
                        } else {
                            printf("Fizz\\n");
                        }
                    }
                }
            }
        } else {
            if (i % 5 == 0) {
                if (i % 3 != 0) {
                    if (i > 0) {
                        printf("Buzz\\n");
                    } else {
                        printf("Buzz\\n");
                    }
                }
            } else {
                if (i % 3 != 0) {
                    if (i % 5 != 0) {
                        if (i > 0) {
                            printf("%d\\n", i);
                        }
                    }
                }
            }
        }
    }
    return 0;
}

これがC言語の力じゃ。ネストが深いほど魂がこもっておる。
読みにくい？読みにくいくらいがちょうどええんじゃ。"""
