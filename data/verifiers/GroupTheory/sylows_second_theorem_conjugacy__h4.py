import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_group(X):
    if isinstance(X, PermutationGroup):
        return X
    if isinstance(X, Permutation):
        return PermutationGroup([X])
    return PermutationGroup(X)

def conditions(witness):
    try:
        G, p, P, Q = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    # H3: P is a Sylow p-subgroup of G
    try:
        if not (h1 and h2):
            h3 = False
        else:
            n = G.order()
            k = 0
            while n % p == 0:
                n //= p
                k += 1
            expected_order = p**k

            P_grp = get_group(P)

            if P_grp.order() != expected_order:
                h3 = False
            else:
                h3 = True
                for g in P_grp.generators:
                    if g not in G:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # neg_Q: There is no element g in G such that gPg^{-1} = Q
    try:
        if not h1:
            neg_q = False
        else:
            try:
                P_grp = get_group(P)
            except Exception:
                # If P is not a valid group, gPg^{-1} = Q is false, so its negation is True
                return [h1, h2, h3, True]

            try:
                Q_grp = get_group(Q)
                q_is_group = True
            except Exception:
                q_is_group = False

            neg_q = True
            
            try:
                elements = list(G.generate())
            except Exception:
                elements = list(G.elements)
                
            for g in elements:
                conj_gens = [g * x * ~g for x in P_grp.generators]
                conj_P = PermutationGroup(conj_gens)

                same = True
                if not q_is_group:
                    same = False
                elif conj_P.order() != Q_grp.order():
                    same = False
                else:
                    for cg in conj_P.generators:
                        try:
                            if cg not in Q_grp:
                                same = False
                                break
                        except Exception:
                            same = False
                            break
                if same:
                    neg_q = False
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: There is no element g in G such that gPg^{-1} = Q"
]

N_HYP = 3
NEG_Q_INDEX = 3