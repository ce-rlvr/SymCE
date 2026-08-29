import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            S = witness.get('S')
            N = witness.get('N')
        else:
            G, S, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: S is a normal solvable subgroup of G
    try:
        is_S_subgroup = all(s in G for s in S.generators)
        
        is_normal = True
        for g in G.generators:
            for s in S.generators:
                if (g * s * ~g) not in S:
                    is_normal = False
                    break
            if not is_normal:
                break
                
        solvable_attr = S.is_solvable
        if callable(solvable_attr):
            is_solvable = bool(solvable_attr())
        else:
            is_solvable = bool(solvable_attr)
            
        h2 = is_S_subgroup and is_normal and is_solvable
    except Exception:
        h2 = False

    # ¬Q: The intersection of N and S is not the trivial subgroup
    try:
        is_N_subgroup = all(n in G for n in N.generators)
        if not is_N_subgroup:
            neg_q = False
        else:
            count = 0
            for x in S.generate():
                try:
                    if x in N:
                        count += 1
                        if count > 1:
                            break
                except Exception:
                    pass
            neg_q = count > 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: S is a normal solvable subgroup of G",
    "¬Q: The intersection of N and S is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2