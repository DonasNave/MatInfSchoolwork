# ZÁPOČTOVÝ ÚKOL DO MATEMATICKÉ INFORMATIKY

## Benchmarking úloha

### Dejong1

Jednoduchá funkce, logika za parametry je co nejmenší odchylka pro normální distribuci
a tedy co nejmenší skoky, jednoduše nechat algoritmus zklouznout do minima. Tomu odpovídá
i fce chlazení, která chladí o poměrnou část a postupně zpomaluje.

Parametry:

```python
- FES = 20000
- temp_target = 0.0001
- temp_init = 2000
- metropolis_n = 10
- std = 0.01
- cooling = lambda temp: temp - temp * 0.99163
- bounds = [-5, 5]
```

#### Dimenze 5

![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_rand_g.png) 
![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_avg_rand_g.png)

![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_avg_anneal_g.png)

#### Dimenze 10

![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_rand_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_avg_rand_g.png)

![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_avg_anneal_g.png)


### Dejong2

Podobná situace, ale přítomnost "sedel" vyžaduje větší skoky, aby byl annealing
schopný vyšplhat z lokálního minima. Ty jsou ale v závěru zase zmenšeny, aby se nadrobno mohlo dohledat minimum.
Z testování vyplynulo, že nejvodnější způsob chlazení je zase poměrový.

Jak u dim 5 tak i 10 je vidět, že pro některé běhy annealingu uvázne alg. u lokálního minima.
 
Parametry:

```python
- FES = 20000
- temp_target = 0.0001
- temp_init = 2000
- metropolis_n = 10
- std = devitation_adaptive2
- cooling = lambda temp: temp - temp * 0.99163
- bounds = [-5, 5]

def devitation_adaptive2(temp):
    if temp > 60:
        return 0.5
    if temp > 1:
        return 0.1
    return 0.005
```

#### Dimenze 5

![D5RandomDJ1](pictures/benchmarks/dejong2/d5_dej2_rand_g.png) 
![D5RandomDJ1](pictures/benchmarks/dejong2/d5_dej2_avg_rand_g.png)

![D5RandomDJ1](pictures/benchmarks/dejong2/d5_dej2_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong2/d5_dej2_avg_anneal_g.png)

#### Dimenze 10

![D5RandomDJ1](pictures/benchmarks/dejong2/d10_dej2_rand_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong2/d10_dej2_avg_rand_g.png)

![D5RandomDJ1](pictures/benchmarks/dejong2/d10_dej2_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong2/d10_dej2_avg_anneal_g.png)

### Schwefel

bbb

Parametry:

```python
- FES = 20000
- temp_target = 0.00001
- temp_init = 1000
- metropolis_n = 20
- std = lambda temp: 2.5 * (1.5 - temp / temp_init) + 0.5
- cooling = lambda temp: temp / (1 + temp * 0.989)
- bounds = [-500, 500]
```

Konzistentní performace annealingu byl ten, že to našlo nějaké lokální minimum a tam to taky zůstalo. V průměru to bylo
cca ideal/2. Random search se v menším prostoru dokázal vydat lepší výsledek.

#### Dimenze 5

![D5RandomDJ1](pictures/benchmarks/schwefel/d5_schwefel_rand_g.png) 
![D5RandomDJ1](pictures/benchmarks/schwefel/d5_schwefel_avg_rand_g.png)

![D5RandomDJ1](pictures/benchmarks/schwefel/d5_schwefel_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/schwefel/d5_schwefel_avg_anneal_g.png)

#### Dimenze 10

V dimenzi 10 podává annealing průměrně lepší výsledek, seč jen o trochu.

![D5RandomDJ1](pictures/benchmarks/schwefel/d10_schwefel_rand_g.png)
![D5RandomDJ1](pictures/benchmarks/schwefel/d10_schwefel_avg_rand_g.png)

![D5RandomDJ1](pictures/benchmarks/schwefel/d10_schwefel_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/schwefel/d10_schwefel_avg_anneal_g.png)

#### Dimenze 12

Kvůli špatným výsledkům pro nižší dimenze jsem se rozhodl otestovat i dimenzi 12, tady už je značně lepší simulované 
žíhání. I tak se ale konzistentně nepřibližuje globálnímu optimu a končí v optimech lokálních.

![D5RandomDJ1](pictures/benchmarks/schwefel/d12_schwefel_rand_g.png)
![D5RandomDJ1](pictures/benchmarks/schwefel/d12_schwefel_avg_rand_g.png)

![D5RandomDJ1](pictures/benchmarks/schwefel/d12_schwefel_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/schwefel/d12_schwefel_avg_anneal_g.png)

## Knapsack úloha

Dle zadání jsem se rozhodl u všeho pracovat 

Parametry:

### Dimenze 15

Random search si vedl dobře v malém prostoru a dokázal se v průměru přiblížit k optimu o 1. Naproti tomu annealing
i v menší dimenzi dokázal v průměru najít téměř 2x lepší řešení.

![D5RandomDJ1](pictures/knapsack/d15_knapsack_rand_g.png) 
![D5RandomDJ1](pictures/knapsack/d15_knapsack_avg_rand_g.png) 

![D5RandomDJ1](pictures/knapsack/d15_knapsack_anneal_g.png) 
![D5RandomDJ1](pictures/knapsack/d15_knapsack_avg_anneal_g.png)  

### Dimenze 30

Random search si vedl dobře v malém prostoru a dokázal se v průměru přiblížit k optimu o 1. Naproti tomu annealing
i v menší dimenzi dokázal v průměru najít téměř 2x lepší řešení.

![D5RandomDJ1](pictures/knapsack/d30_knapsack_rand_g.png) 
![D5RandomDJ1](pictures/knapsack/d30_knapsack_avg_rand_g.png) 

![D5RandomDJ1](pictures/knapsack/d30_knapsack_anneal_g.png) 
![D5RandomDJ1](pictures/knapsack/d30_knapsack_avg_anneal_g.png)  

### Dimenze 50

Ve větší dimenzi annealing podává v průměru víc než 2x lepší výsledek.

![D5RandomDJ1](pictures/knapsack/d50_knapsack_rand_g.png) 
![D5RandomDJ1](pictures/knapsack/d50_knapsack_avg_rand_g.png) 

![D5RandomDJ1](pictures/knapsack/d50_knapsack_anneal_g.png) 
![D5RandomDJ1](pictures/knapsack/d50_knapsack_avg_anneal_g.png)  