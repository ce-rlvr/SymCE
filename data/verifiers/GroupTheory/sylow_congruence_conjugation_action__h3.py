import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import isprime

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

def get_all_sylow_p_subgroups(G, p):
    try:
        base_P = G.sylow_subgroup(p)
    except Exception:
        return set()
    sylows_sets = set()
    base_P_elems = list(base_P.generate())
    for g in G.generate():
        H_elems = frozenset([g * h * ~g for h in base_P_elems])
        sylows_sets.add(H_elems)
    return sylows_sets

def conditions(witness) -> list[bool]:
    try:
        G, p, S, P = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p is a prime dividing the order of G
    try:
        h2 = isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False

    # H_3: S is the set of all Sylow p-subgroups of G
    try:
        S_sets = set()
        h3_valid_S = True
        for H in S:
            if isinstance(H, PermutationGroup):
                S_sets.add(frozenset(H.generate()))
            elif isinstance(H, (set, frozenset, list, tuple)):
                S_sets.add(frozenset(H))
            else:
                h3_valid_S = False
                break
        if h3_valid_S:
            expected_S_sets = get_all_sylow_p_subgroups(G, p)
            h3 = (S_sets == expected_S_sets) and (len(S) == len(S_sets))
        else:
            h3 = False
    except Exception:
        h3 = False

    # H_4: P acts on S by conjugation
    try:
        h4 = True
        if isinstance(P, PermutationGroup):
            P_elems = list(P.generate())
        elif isinstance(P, (list, set, tuple)):
            P_elems = list(P)
        else:
            h4 = False
            
        if h4:
            for H_set in S_sets:
                for g in P_elems:
                    H_conj = frozenset([g * h * ~g for h in H_set])
                    if H_conj not in S_sets:
                        h4 = False
                        break
                if not h4:
                    break
    except Exception:
        h4 = False

    # ¬Q: The number of Sylow p-subgroups of G (the cardinality of S) is not congruent to 1 modulo p
    try:
        neg_q = not (len(S) % p == 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime dividing the order of G",
    "H_3: S is the set of all Sylow p-subgroups of G",
    "H_4: P acts on S by conjugation",
    "¬Q: The number of Sylow p-subgroups of G (the cardinality of S) is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4