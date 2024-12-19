% #const maxtime = 23.

% Posizioni sulla griglia 3x3
posizione(1..3, 1..3).

% Tessere numerate da 0 a 8
tessera(0..8).

% Fluenti
fluent(posizione_tessera(Tessera, X, Y)) :- tessera(Tessera), posizione(X, Y).

% Stato iniziale
% initially(posizione_tessera(1, 1, 1)).
% initially(posizione_tessera(7, 1, 2)).
% initially(posizione_tessera(8, 1, 3)).
% initially(posizione_tessera(4, 2, 1)).
% initially(posizione_tessera(5, 2, 2)).
% initially(posizione_tessera(6, 2, 3)).
% initially(posizione_tessera(2, 3, 1)).
% initially(posizione_tessera(0, 3, 2)). % Spazio vuoto
% initially(posizione_tessera(3, 3, 3)).

% Configurazione obiettivo
goal(posizione_tessera(1, 1, 1)).
goal(posizione_tessera(2, 1, 2)).
goal(posizione_tessera(3, 1, 3)).
goal(posizione_tessera(4, 2, 1)).
goal(posizione_tessera(5, 2, 2)).
goal(posizione_tessera(6, 2, 3)).
goal(posizione_tessera(7, 3, 1)).
goal(posizione_tessera(8, 3, 2)).
goal(posizione_tessera(0, 3, 3)).

% Azioni
azione(muovi(Tessera, X1, Y1, X2, Y2)) :-
    tessera(Tessera), Tessera != 0,
    posizione(X1, Y1), posizione(X2, Y2),
    adiacente(X1, Y1, X2, Y2).

% Definizione di adiacenza
adiacente(X1, Y1, X2, Y2) :-
    posizione(X1, Y1), posizione(X2, Y2),
    X1 = X2, Y1 = Y2 + 1.

adiacente(X1, Y1, X2, Y2) :-
    posizione(X1, Y1), posizione(X2, Y2),
    X1 = X2, Y1 = Y2 - 1.

adiacente(X1, Y1, X2, Y2) :-
    posizione(X1, Y1), posizione(X2, Y2),
    Y1 = Y2, X1 = X2 + 1.

adiacente(X1, Y1, X2, Y2) :-
    posizione(X1, Y1), posizione(X2, Y2),
    Y1 = Y2, X1 = X2 - 1.

% Azione possibile
possibile(muovi(Tessera, X1, Y1, X2, Y2), T) :-
    holds(posizione_tessera(Tessera, X1, Y1), T),
    holds(posizione_tessera(0, X2, Y2), T),
    adiacente(X1, Y1, X2, Y2),
    time(T).

% Scelta dell'azione
{ occurs(muovi(Tessera, X1, Y1, X2, Y2), T) } :-
    possibile(muovi(Tessera, X1, Y1, X2, Y2), T),
    time(T).

% Effetti delle azioni
holds(posizione_tessera(Tessera, X2, Y2), T+1) :-
    occurs(muovi(Tessera, X1, Y1, X2, Y2), T),
    time(T).

holds(posizione_tessera(0, X1, Y1), T+1) :-
    occurs(muovi(Tessera, X1, Y1, X2, Y2), T),
    time(T).

% Persistenza dei fluenti
holds(posizione_tessera(Tessera, X, Y), T+1) :-
    holds(posizione_tessera(Tessera, X, Y), T),
    not occurs(muovi(_, X, Y, _, _), T),
    not occurs(muovi(_, _, _, X, Y), T),
    not goal_reached(T),
    time(T).

%  Nessuna regola propaghi stati o azioni dopo il tempo TG in cui il goal viene raggiunto.
:- holds(_, T), goal_reached(TG), T > TG, time(T).

% Vincoli di dominio
:- occurs(muovi(Tessera, X1, Y1, X2, Y2), T),
   not possibile(muovi(Tessera, X1, Y1, X2, Y2), T),
   time(T).

% Vincolo: non possono avvenire due azioni diverse nello stesso istante
:- occurs(muovi(T1, _, _, _, _), T), occurs(muovi(T2, _, _, _, _), T), T1 != T2, time(T).

% Vincolo: nessuna azione deve avvenire dopo il raggiungimento del goal
:- occurs(_, T), T > TG, goal_reached(TG), time(TG), time(T).

% Vincolo: Non bisogna andare avanti e indietro
:- occurs(muovi(Tessera, X1, Y1, X2, Y2), T),
   occurs(muovi(_, X2, Y2, X1, Y1), T+1).

% Distanza di Manhattan attuale per una tessera in una mossa
distanza_manhattan(Tessera, D, T) :-
    tessera(Tessera), Tessera != 0,
    holds(posizione_tessera(Tessera, X1, Y1), T),
    goal(posizione_tessera(Tessera, Xg, Yg)),
    D = |X1 - Xg| + |Y1 - Yg|.

:~ occurs(muovi(Tessera, X1, Y1, X2, Y2), T),
    distanza_manhattan(Tessera, D1, T),
    distanza_manhattan(Tessera, D2, T+1),
    D2 > D1. [D2 - D1@1]

% Intervallo temporale
time(0..maxtime).

% Stato iniziale al tempo 0
holds(F, 0) :- initially(F).

% Raggiungimento dell'obiettivo
goal_reached(T) :-
    time(T),
    #count { Tessera, X, Y :
        goal(posizione_tessera(Tessera, X, Y)),
        holds(posizione_tessera(Tessera, X, Y), T)
    } = 9.
    
% Minimizzare il numero di mosse
#minimize { T : goal_reached(T) }.

:- not goal_reached(_).
% Output
% #show occurs/2.
% #show possibile/2.
#show holds/2.
#show goal_reached/1.



% Models       : 1
%   Optimum    : yes
% Optimization : 1 23
% Calls        : 1
% Time         : 81.032s (Solving: 80.77s 1st Model: 77.38s Unsat: 3.40s)
% CPU Time     : 80.480s

% Choices      : 888818  
% Conflicts    : 641126   (Analyzed: 641125)
% Restarts     : 1532     (Average: 418.49 Last: 490)
% Model-Level  : 13.0    
% Problems     : 1        (Average Length: 0.00 Splits: 0)
% Lemmas       : 641125   (Deleted: 525104)
%   Binary     : 10613    (Ratio:   1.66%)
%   Ternary    : 10282    (Ratio:   1.60%)
%   Conflict   : 641125   (Average Length:   57.9 Ratio: 100.00%) 
%   Loop       : 0        (Average Length:    0.0 Ratio:   0.00%) 
%   Other      : 0        (Average Length:    0.0 Ratio:   0.00%) 
% Backjumps    : 641125   (Average:  1.37 Max:  93 Sum: 877066)
%   Executed   : 641125   (Average:  1.37 Max:  93 Sum: 877066 Ratio: 100.00%)
%   Bounded    : 0        (Average:  0.00 Max:   0 Sum:      0 Ratio:   0.00%)

% Rules        : 124113  
%   Choice     : 4984    
%   Minimize   : 2       
% Atoms        : 45167   
% Bodies       : 90924   
% Equivalences : 233508   (Atom=Atom: 690 Body=Body: 420 Other: 232398)
% Tight        : Yes
% Variables    : 45607    (Eliminated:    0 Frozen:   25)
% Constraints  : 234765   (Binary:  82.7% Ternary:   2.1% Other:  15.2%)