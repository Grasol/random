# mtpech

Wielowątkowa aplikacja, zliczająca [liczby pechowe](https://sio2.mimuw.edu.pl/c/oij14-1/p/pec/)
z zakresu 1 do N. Aplikacja powstała w ramach nauki zestawu instrukcji AVX-512 dla procesorów Intela.

#### Użycie:

- ```mtpech threads_number max_range```
- ```mtpech2 threads_number max_range```

Program uruchamia się na takiej ilości wątków, jaką podamy.
'mtpech' od 'mtpech2' różnią się algorytmem. 
'mtpech' używa rejesestrów ymm (256-bitowych), natomiast 'mtpech2' rejstrów zmm (512-bitowych).

Do uruchomienia binarek wymagany jest procesor z instrukcjami AVX-512(F, VL, DQ, BW). 
Kod został napisany pod Windowsa.
