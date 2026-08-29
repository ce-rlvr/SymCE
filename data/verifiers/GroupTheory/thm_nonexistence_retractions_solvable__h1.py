import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, S, r = witness
    except Exception:
        return [False, False, False]

    # H1: S is a solvable subgroup of G
    try:
        h1 = True
        for g in S.generators:
            if g not in G:
                h1 = False
                break
        if h1:
            h1 = bool(S.is_solvable)
    except Exception:
        h1 = False

    # H2: r: G \to S is a group homomorphism such that r(s) = s for all s \in S
    try:
        if callable(r):
            r_func = r
        else:
            r_func = lambda x: r[x]
            
        h2 = True
        S_elems = set(S.generate())
        
        # Check r(s) = s for all s in S
        for s in S_elems:
            if r_func(s) != s:
                h2 = False
                break
                
        if h2:
            # Check homomorphism and well-definedness
            G_elems = list(G.generate())
            for x in G_elems:
                rx = r_func(x)
                if rx not in S_elems:
                    h2 = False
                    break
                for y in G_elems:
                    if r_func(x * y) != rx * r_func(y):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: S is not the trivial subgroup
    try:
        neg_q = bool(S.order() > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a solvable subgroup of G",
    "H_2: r: G -> S is a group homomorphism such that r(s) = s for all s in S",
    "¬Q: S is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2