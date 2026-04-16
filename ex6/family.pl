% ----------- Gender -----------

male(motilal_nehru).
male(jawaharlal_nehru).
male(feroze_gandhi).
male(rajiv_gandhi).
male(sanjay_gandhi).
male(rahul_gandhi).

female(swarup_rani).
female(kamala_nehru).
female(indira_gandhi).
female(sonia_gandhi).
female(priyanka_gandhi).

% ----------- Parent -----------

parent(motilal_nehru, jawaharlal_nehru).
parent(swarup_rani, jawaharlal_nehru).

parent(jawaharlal_nehru, indira_gandhi).
parent(kamala_nehru, indira_gandhi).

parent(indira_gandhi, rajiv_gandhi).
parent(feroze_gandhi, rajiv_gandhi).

parent(indira_gandhi, sanjay_gandhi).
parent(feroze_gandhi, sanjay_gandhi).

parent(rajiv_gandhi, rahul_gandhi).
parent(sonia_gandhi, rahul_gandhi).

parent(rajiv_gandhi, priyanka_gandhi).
parent(sonia_gandhi, priyanka_gandhi).

% ----------- Marriage -----------

married(jawaharlal_nehru, kamala_nehru).
married(kamala_nehru, jawaharlal_nehru).

married(indira_gandhi, feroze_gandhi).
married(feroze_gandhi, indira_gandhi).

married(rajiv_gandhi, sonia_gandhi).
married(sonia_gandhi, rajiv_gandhi).

% ----------- Basic Relations -----------

father(X,Y) :-
    parent(X,Y),
    male(X).

mother(X,Y) :-
    parent(X,Y),
    female(X).

child(X,Y) :-
    parent(Y,X).

% ----------- Grand Relations -----------

grandparent(X,Y) :-
    parent(X,Z),
    parent(Z,Y).

grandfather(X,Y) :-
    grandparent(X,Y),
    male(X).

grandmother(X,Y) :-
    grandparent(X,Y),
    female(X).

% ----------- Great Grand Relations -----------

great_grandparent(X,Y) :-
    parent(X,A),
    parent(A,B),
    parent(B,Y).

great_grandfather(X,Y) :-
    great_grandparent(X,Y),
    male(X).

great_grandmother(X,Y) :-
    great_grandparent(X,Y),
    female(X).

% ----------- Siblings -----------

sibling(X,Y) :-
    parent(Z,X),
    parent(Z,Y),
    X \= Y.

brother(X,Y) :-
    sibling(X,Y),
    male(X).

sister(X,Y) :-
    sibling(X,Y),
    female(X).

% ----------- Uncle & Aunt -----------

uncle(X,Y) :-
    brother(X,Z),
    parent(Z,Y).

aunt(X,Y) :-
    sister(X,Z),
    parent(Z,Y).

% ----------- Cousins -----------

cousin(X,Y) :-
    parent(A,X),
    parent(B,Y),
    sibling(A,B).

% ----------- In-Law Relations -----------

father_in_law(X,Y) :-
    married(Y,Z),
    father(X,Z).

mother_in_law(X,Y) :-
    married(Y,Z),
    mother(X,Z).

brother_in_law(X,Y) :-
    married(Y,Z),
    brother(X,Z).

sister_in_law(X,Y) :-
    married(Y,Z),
    sister(X,Z).

% ----------- Husband & Wife -----------

husband(X,Y) :-
    married(X,Y),
    male(X).

wife(X,Y) :-
    married(X,Y),
    female(X).

% ----------- Ancestor -----------

ancestor(X,Y) :-
    parent(X,Y).

ancestor(X,Y) :-
    parent(X,Z),
    ancestor(Z,Y).
