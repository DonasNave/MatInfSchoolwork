# ZÁPOČTOVÝ ÚKOL DO MATEMATICKÉ INFORMATIKY

## Osnova

1. [Benchmarking úloha](#benchmarking-úloha)
2. [Praktická úloha](#praktická-úloha)
3. [Good to know](#poznámky-k-úkolu)

## Benchmarking úloha

Vaším úkolem bude implementace 2 stochastických heuristických algoritmů a vytvoření jednoduchých statistických (a grafických) křížových srovnání.

### Algoritmy

- Random Search (RS) (jako baseline metoda)
- Simulované žíhání (SA)
- Testovací funkce (Dimenze D=5 a D=10)
  - 1st DeJong function
  - 2nd DeJong function
  - Schweffel function

Pro porovnání algoritmů musíte zachovat „přibližně“ stejnou hodnotu FES (Cost Function Evaluations). FES lze nastavit např. na 10 000, tj. pokud implementujete SA s 10 voláními metropolise (pro generování okolního řešení, ohodnocení a rozhodnutí co dělat), v každé JEDNÉ iteraci SA (pro jednu fixní teplotu) algoritmu provedete 10 FES, takže můžete mít celkem max. 1000 iterací. RS - logicky existuje pouze jedno FES za 1 iteraci

Oba dva algoritmy se musí spustit opakovaně 30x pro každou zkušební funkci a nastavení dimenze - pro získání nějakého statistického základu - vypočítáte (z 30 nejlepších výsledků) Min, Max, Mean, Median a Std. Dev. hodnoty a porovnejte tyto hodnoty mezi 2 algoritmy pro každou zkušební funkci. Musíte také potvrdit vaše výsledky vykreslením nejlepších řešení z každé iterace - tj. konvergenční graf. Vaším úkolem je vykreslit:

- Konvergenční graf všech 30 běhů v jednom grafu (30 čar v 1 grafu) - celkem 12 grafů (2 algoritmy x 3 funkce x 2 nastavení dimenze)
- Konvergenční graf průměrného nejlepšího výsledků - tj. Průměrné nejlepší řešení v každé iteraci (jeden graf – z těch 30 čar výše uděláte v každé iteraci průměr) - celkem 12 grafů (2 algoritmy x 3 funkce x 2 nastavení dimenze)
- Porovnání těchto průměrných konvergencí pro 2 algoritmy v jednom grafu pro každou testovací funkci - celkem 6 grafů (3 funkce x 2 nastavení dimenze)

### Příklady

1. 30 konvergencí v jednom grafu ![Konvergence](/pictures/Benchmark_ex1_1.png)
2. Průměrná konvergence ![Evoluce](/pictures/Benchmark_ex1_2.png)
3. porovnání konvergenčních grafů (zde jsou ještě 3 algoritmy – vy budete mít 2) ![Srovnání evolucí](/pictures/Benchmark_ex1_3.png)

### Berte v úvahu následující

- Nelze opustit vyhledávací prostor - při vytváření sousedních řešení - zkontrolujte hranice typické pro každou testovací funkci (-500 až 500 pro Schwefel, -5 až 5 pro obě funkce DeJong). Pokud opustíte vyhledávací prostor - vygenerujete nový bod okolí.
- Nastavení:
  - Max FES 10000,
  - Dimension: 5, 10,
počet volání metropolise pro 1 teplotu: nt = min 10, max ??, okolí max 10% prohledávacího prostoru,
max temp ?? (1000),
min temp ?? (0,01),
cooling decr 0.98?
- Zde proveďte parameter tuning a vlastní výzkum vhodných max/min parametrů teploty/decr konstanty a počtu volání metropolise pro jednu teplotu – zda max/min = 1000/0.1, nebo 10000/1, 1000/0.01 atd... zkuste nastavit maxT. minT, počet volání metropolise, dekrement teploty, abyste dosáhli (využili) hodnoty maxFES

## Praktická úloha

Vaším úkolem bude vyřešení zvoleného typu problému batohu pomocí stochastického algoritmu (Simulované žíhání).

### Algoritmy

- Random Search (RS) (nepovinné - jako baseline metoda)
- Simulované žíhání (SA)
- Varianty problému batohu (vyberte si libovolnou dle odvahy)
  - Klasický základní (tzv. 0-1 KP)
  - Problém batohu s vícenásobnou volbou (Multiple-choice knapsack problem, MCKP)

**Cílem č.1 bude nalezení řešení hrubou silou.**
Pro to bude potřeba

- Vytvořit účelovou funkci, která bude počítat cenu zadané kombinace itemů, ale zároveň dbát na maximální kapacitu. Cílem bude hledání řešení s MAXIMÁLNÍ cenou, ale splňující kapacitu.
- Vygenerovat si instanci problému pro KP/MCKP
  - Min počet 10 předmětů pro KP
  - Objem předmětu – náhodný, rozsah 1 až 50
  - Cena předmětu – náhodná, rozsah 1 až 50
  - Dále pro MCKP i id třídy do které náleží (počet 3-10-??) m a pak jasně id předmětu v dané třídě n (rozsah 1-3 – budeme uvažovat vždy 3 předměty na 1 třídu pro zjednodušení).
  - Např. pro KP můžete mít 2 vektory p (price) a w (weight/volume), které budou stejně dlouhé a pozice ve vektoru je zároveň id předmětu a udává z obou vektorů jeho cenu a hmotnost/objem. Nebo vytvořte strukturu. U MCKP je také možností více – 2 datové struktury (matice) cenová a matice objemová/hmotnostní m x n, nebo složitá struktura, kde např. {1, 3, 15, 35} je předmět ze třídy 1, s Id 3, objemem 15 a cenou 35.
- Stanovit kapacitu batohu, objem (hmotnost), která je nepřekročitelná
  - Pro 10-15 předmětů (KP) nebo 3 až 5 tříd (MCKP) je kapacita = 100 o Pro 16-30 předmětů (KP) nebo 6 až 10 (MCKP) tříd je kapacita = 200 o Pro více předmětů/tříd je kapacita = 300
- Vytvořit ukázku instance (menší – např 5 tříd (MCKP), nebo 15 předmětů (KP))

<center>

| Třída  | Id     | Objem  | Cena   |
| :----: | :----: | :----: | :----: |
| 1 | 1 | 9 | 22 |
| 1 | 2 | 43 | 28 |
| 1 | 3 | 40 | 28 |
| 2 | 1 | 1 | 42 |
| 2 | 2 | 47 | 27 |
| 2 | 3 | 19 | 48 |
| 3 | 1 | 28 | 47 |
| 3 | 2 | 38 | 41 |
| 3 | 3 | 33 | 6 |
| 4 | 1 | 35 | 15 |
| 4 | 2 | 45 | 12 |
| 4 | 3 | 32 | 36 |
| 5 | 1 | 21 | 4 |
| 5 | 2 | 50 | 30 |
| 5 | 3 | 5 | 4 |
| Suma: || 446 | 390 |

</center>

- Vyřešit problém hrubou silou (tedy projít všechny kombinace)
  - Poskytnout finální výsledek tedy seznam vybraných předmětů s nejvyšší
možnou cenou a splňujících podmínky (dodržena maximální kapacita batohu, a pro MCKP z každé třídy je vybrán právě jeden předmět, ...)
  - Celkový čas potřebný pro nalezení nejlepšího řešení.
  - Ukázku toho, kolik tříd jste na vašem stroji schopni vyřešit do hodiny.

<center>

| Trida  | Id     | Objem  | Cena   |
| :----: | :----: | :----: | :----: |
| 1 | 1 | 9 | 22 |
| 2 | 3 | 19 | 48 |
| 3 | 1 | 28 | 47 |
| 4 | 3 | 32 | 36 |
| 5 | 3 | 5 | 4 |
| Suma: || 93 | 157 |

</center>

### Cílem č. 2 bude vyřešení úlohy heuristikou

Pro to bude potřeba

- **Využít účelovou funkci z řešení výše**
- **Zvolit vhodnou reprezentaci řešení/jedince**
- např. vektor idček itemů v jednotlivých třídách (tedy vektor celých čísel v rozsahu stejném jako id o délce rovné počtu tříd (dimenze))
- Upravit funkci pro generování sousedního řešení
  - Pro KP: S pravděpodobností 1/dimenze (dimenze = n předmětů) můžete
invertovat bit 0 = neberu, 1 = beru předmět ve vektoru id-ček. Můžete zkusit i trik, že ze začátku může být i pravděpodobnost výběru vyšší (větší explorace) – abyste invertovali třeba 2-3 bity.
  
  - Pro MCKP: Zde je již vícero variant. Nejpřímočařejší - s určenou pravděpodobností (např 1/dimenze) budete měnit idčka v aktuálním řešení. Tady ale může být dimenzí např. počet tříd (m), a obsah vektoru ideček bude zároveň identifikovat i předmět ze třídy. Tedy {2, 3, 1, 2, 1} znamená, že beru předmět č. 2 z třídy 1, č. 3 z třídy 2, č. 1 z třídy 3... Sousední okolní řešení je pak náhodná změna idčka předmětu v třídě, třeba {3, 3, 1, 2, 1}. Tím je zajištěna I kontrola, že z každé třídy bude vybrán jen 1 předmět (heuristika do toho nešahá), a zároveň “okolnost” – většinou se změní jen obsah jedné třídy (při pravděpodobnosti 1/m). Pozor na vygenerování shodného řešení, to by nemělo smysl ohodnocovat

- **Cílem je dosáhnut „efektivního“ řešení za kratší dobu, než brute force (to podá samozřejměvždy nejlepší možné řešení)**
  - Upravte tedy parametry SA (počet „iterací, max, min teplota), a zkoumejte za jaký čas získáte velmi dobré (při troše štěstí i nejlepší řešení) při porovnání
s brute force.
  
  - **Pozor na maxFES heuristika by neměla jít přes maxFES brute force, tedy max. počtu kombinací**

Pro zobrazení výkonu algoritmu je dobré též si zaznamenávat průběh nejlepšího nalezeného řešení a zobrazit konvergenční graf a porovnání s naivní/brute force metodou. Samozřejmostí je opakované spuštění heuristiky.

## Poznámky k úkolu

- Testovací funkce schweffel, deJong... atd, a dále je účelovou/hodnotící funkcí pro algoritmus. Je to umělý zástupný problém, pro demostraci funkcionality algoritmu

- Dimenze problémů znamená, kolik parametrů hledáme (kolik souřadnic na hyperploše řešení), které když pošleme do testovací funkce, ta nám vrátí kvalitu řešení. Pro 2D problém, to znamená že hledáme řešení X = {x1, x2}, které když pošleme do test. funkce, získáme třetí dimenzi (D+1) což je kvalita řešení - pro 2D problém je třetí dimenzí "výška" té plochy nad bodem určeným souřadnicemi x1 a x2. Pro 10D, tedy pracujeme v 11D prostoru, hledáme řešení X = {x1, x2,...,x10} a 11-tou dimenzí je návratová hodnota testovací funkce, kterou "tlačím" dolů (hledám minimum této hyperplochy - v případě minimalizačního problému)

- Pozor na rozsah - je to zadané šalamounsky, aby jste byli ve střehu, některé funkce -5, +5, některé -500, +500 pro každou dimenzi

- Tomuto rozsahu je nutné přizpůsobit i relativní velikosti okolí pro local search/hill climber/simulované žíhání. V dokumentu je uvedeno max 10% rozsahu. Takže pokud máme funkci deJong v rozsahu -5, 5, tak rozsah této funkce je 10 pro danou dimenzi, okolí tedy max o velikosti 1, tedy +-0.5 od středoveho pracovního bodu (naroubovat i na normální rozdělení). U schveffela byste se ale s tímto okolím max sklouzli po kousky sinusovky a vyčerpali si iterace, tedy nutné relativně scalovat k rozsahu funkce

- Teploty - tady budete muset experimentovat - uvedené jsou hodnoty, které moc fungovat nebudou (opět záměr Vás dotlačit k výzkumu) #### nebojte se jít až třeba do 0.1 pro chládnoucí teplotu, ne-li níže

- Pozor na funkci simulovaného žíhání - logika podobná jak local search->hillclimber->simulovane zihani. Jedna iterace (main loop) je chapana pro jednu hodnotu teploty! V rámci této jedné teploty provádíte nt-krát tvorbu nového okolí a volání metropolise. Tedy nt-krát vytvoříte okolí ("stejně" jako u local search), ale v něm vytvoříte pouze 1 okolní bod a pošlete jej do metropolise  - pokud je lepší než aktuálně dostupný - update, pokud horší, tak si spočítáte práh metropolise a pokud vygenerovaná random hodnota je pod tento práh - update (ikdyž je horší), nebo prostě se nestane nic... a nedojde k update řešení. Ale do vyčerpání hodnoty nt znovu vygenerujete okolí (pro updatlý/neupdatlý střed) a zase spustíte metropolise. Proto se často nastavuje nt =  počet bodů okolí, protože prověřujete vždy jen 1 náhodné řešení z okolí třeba velikosti 10 řešení, a uděláte to 10x (pro jednu iteraci main loop - tedy 1 teplotu). Poměrem nt vs velikost okolí, natsavením teplot ovládáte, jak moc dlouho se heuristika zdržuje při 1 teplotě, jak rychle chládne atd

- Jako report stačí třeba statistická tabulka průměrných hodnot, min, max median, std dev (finální pro 30 běhů) pro jednotlivé nastavení D. Takže třeba tabulka o 10 funkcích x 5 statistických veličin

- OBECNĚ - Spouštějte vždy heuristiky pokaždé z náhodně vygenerovaného bodu napříč všemi dimenzemi. Pracujeme v prostoru R - tedy rozhodně ne s celými čísly

- Konvergenční graf zachycuje průběh hodnoty účelové funkce! Tedy to nejlepší co máte v dané iteraci k dispozici si ukládejte, a to dostaňte do grafu

- Praktická úloha - velikost instance (počet předmětůzkuste zvolit nějak rozumnně a pak případně přidávat, abyste si ověřili komplexitu úlohy). Případně můžete zabrousit do KPlib, nebo najít něco z benchmarků 0-1 KP problému
