# Gioco del 15

Il gioco del 15 prevede di spostare una delle possibili 4 celle mobili al posto dello spazio. Se lo
spazio si trova adiacente ad un bordo le celle di riducono a 3 (2 nel caso di uno spazio nell’angolo).
Modellare una pianificazione che porta alla risoluzione del gioco a partire da una configurazione
iniziale coerente

## Necessatio per poter eseguire il codice

- clingo
- python

```bash
cd 3x3 

clingo initial_state/state_2.pl gioco_8.asp -t 8 -c maxtime=25
```

```bash
Optimization: 1 22
OPTIMUM FOUND

Models       : 3
  Optimum    : yes
Optimization : 1 22
Calls        : 1
Time         : 43.966s (Solving: 43.71s 1st Model: 40.42s Unsat: 0.09s)
CPU Time     : 267.611s
Threads      : 8        (Winner: 1)
```

Si può sfruttare lo script python myclingo.py per eseguire il codice

```bash
cd ..
python myclingo.py
```
Tale script salva i gli hold dentro a hold.txt, per plottare i risultati si può eseguire il seguente comando
```bash
python plot.py
```

Si creerà il video dentro a output_images