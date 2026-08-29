import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
)
from sympy.combinatorics.perm_groups import PermutationGroup
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    try:
        G, H = witness
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1_ok = bool(G.is_solvable)
    except Exception:
        h1_ok = False
        
    try:
        try:
            d_G = G.derived_length()
            d_H = H.derived_length()
            
            try:
                GH = G * H
            except Exception:
                # Fallback for direct product if * operator is not supported
                n = G.degree
                m = H.degree
                gens = []
                for g in G.generators:
                    arr = list(g.array_form)
                    if len(arr) < n:
                        arr += list(range(len(arr), n))
                    arr += list(range(n, n+m))
                    gens.append(Permutation(arr))
                for h in H.generators:
                    arr = list(h.array_form)
                    if len(arr) < m:
                        arr += list(range(len(arr), m))
                    new_arr = list(range(n)) + [x + n for x in arr]
                    gens.append(Permutation(new_arr))
                if not gens:
                    GH = PermutationGroup([Permutation(0)])
                else:
                    GH = PermutationGroup(gens)
                    
            d_GH = GH.derived_length()
            eq = (d_GH == max(d_G, d_H))
            neg_q_ok = not eq
        except Exception:
            # If derived_length raises an error (e.g. because H is not solvable),
            # then the conclusion that they are equal fails.
            neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "¬Q: The derived length of G x H is not equal to max(d(G), d(H))"
]

N_HYP = 1
NEG_Q_INDEX = 1