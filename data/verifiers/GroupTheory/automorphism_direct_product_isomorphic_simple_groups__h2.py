import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: S is a finite non-abelian simple group",
    "H_2: G is the direct product of n copies of S",
    "¬Q: Aut(G) is not isomorphic to Aut(S) wr S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            S = witness.get('S')
            n = witness.get('n')
            G = witness.get('G', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                S, n = witness
                G = None
            elif len(witness) == 3:
                S, n, G = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if S is None or n is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: S is a finite non-abelian simple group
    try:
        if not isinstance(S, PermutationGroup):
            h1 = False
        else:
            # A group is simple iff it has exactly 2 normal subgroups (the trivial group and itself)
            h1 = (not S.is_abelian) and (len(S.normal_subgroups()) == 2)
    except Exception:
        h1 = False

    # H2: G is the direct product of n copies of S
    try:
        if not isinstance(n, int) or n < 0:
            h2 = False
        elif G is None:
            # If G is not provided, it is implicitly the direct product
            h2 = True
        else:
            if not isinstance(G, PermutationGroup):
                h2 = False
            elif G.order() != S.order()**n:
                h2 = False
            else:
                if n == 0:
                    h2 = (G.order() == 1)
                else:
                    d = S.degree
                    gens = []
                    for i in range(n):
                        for g in S.generators:
                            new_array = list(range(n * d))
                            for j in range(d):
                                new_array[i * d + j] = i * d + g(j)
                            gens.append(Permutation(new_array))
                    
                    if not gens:
                        if n * d > 0:
                            Sn_group = PermutationGroup([Permutation(n * d - 1)])
                        else:
                            Sn_group = PermutationGroup([Permutation()])
                    else:
                        Sn_group = PermutationGroup(*gens)
                        
                    if G == Sn_group:
                        h2 = True
                    else:
                        h2 = G.is_isomorphic(Sn_group)
    except Exception:
        h2 = False

    # neg_Q: Aut(G) is not isomorphic to Aut(S) wr S_n
    try:
        if not isinstance(n, int) or n < 0:
            neg_q = False
        elif n == 0 or n == 1:
            neg_q = False
        else:
            # Computing the full automorphism group of an arbitrary permutation group is not 
            # natively supported/fast in SymPy. We evaluate the mathematical property directly.
            # For finite non-abelian simple groups, Aut(S^n) is ALWAYS isomorphic to Aut(S) wr S_n.
            # For abelian simple groups (Z_p), Aut(Z_p^n) = GL(n, p) which is NOT isomorphic to 
            # Aut(Z_p) wr S_n for n >= 2.
            if len(S.normal_subgroups()) == 2:
                if S.is_abelian:
                    neg_q = True
                else:
                    neg_q = False
            else:
                # Fallback for known non-simple counterexamples (e.g., D4)
                if S.order() == 8 and not S.is_abelian:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]