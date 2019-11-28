:- table solve(_,lattice(or/3)).

or(P1,P2,(P1;P2)).

solve(true,true) :- !.
solve((A,B),(ProofA,ProofB)) :- !, solve(A,ProofA), solve(B,ProofB).
solve(A) :- predicate_property(A, builtin), !, A, recordz(proof,A:-builtin(A)).
solve(A) :- predicate_property(A, foreign), !, A, recordz(proof,A:-foreign(A)).
solve(A,A:-ProofB) :- cl(A,B),solve(B,ProofB).
solve(A,::(I,P,A)) :- fa(I,P,A).

prove(Q,Proofs) :- findall(Q:-Proof,solve(Q,Proof),Proofs).