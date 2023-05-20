# ZÁPOČTOVÝ ÚKOL DO MATEMATICKÉ INFORMATIKY

## Osnova

1. [Benchmarking úloha](#benchmarking-úloha)
2. [Praktická úloha](#praktická-úloha)

## Benchmarking úloha

Dle zadání jsem se rozhodl u všeho pracovat s FES 10000, která sice v některých fázích limitovala, ale představovala
grounded hodnotu, která byla pro všechny algoritmy stejná. Náročnost výsledků je tedy porovnatelná.

### Dejong1

#### Random Search

Random search si vedl dobře v malém prostoru, s dobrou "konsistencí"(heh) se dostal na nízkou hodnotu, ale přiblížit 
se ideálnímu řešení už konsistentně nedokázal. To bylo obzvlášť pozorovatelné u dimenze 10. 

![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_rand_g.png) 
![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_avg_rand_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_rand_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_avg_rand_g.png)

#### Simulated Annealing

Simulated annealing byl lepší ve větším prostoru

![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d5_dej1_avg_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_anneal_g.png)
![D5RandomDJ1](pictures/benchmarks/dejong1/d10_dej1_avg_anneal_g.png)