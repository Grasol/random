<h1>mtpech</h1>

<p>
  Wielowątkowa aplikacja, zliczająca <a href src="https://sio2.mimuw.edu.pl/c/oij14-1/p/pec/">liczby pechowe</a>
  z zakresu 1 do N. Aplikacja powstała w ramach nauki zestawu instrukcji AVX-512 dla procesorów Intela.
</p>
<h4>Użycie:</h4>
<ul style="font-family:'Consolas';">
  <li>mtpech threads_number max_range</li>
  <li>mtpech2 threads_number max_range</li>
</ul>
<p>
  Algorytm uruchamia się na takiej ilości wątków, jaką podamy.
  'mtpech' od 'mtpech2' różnią się algorytmem. 
  'mtpech' używa rejesestrów ymm (256-bitowych), natomiast 'mtpech2' rejstrów zmm (512-bitowych).
</p>
<p>
  Do uruchomienia binarek wymagany jest procesor z instrukcjami AVX-512(F, VL, DQ, BW). 
  Kod został napisany pod Windowsa.
</p>
