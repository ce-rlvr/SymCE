import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    # Extract G, H, N, n from the witness
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                G, H, N, n = witness
            elif len(witness) == 3:
                G, H, N = witness
                n = G.order() // H.order()
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            N = witness.get('N')
            if 'n' in witness:
                n = witness['n']
            else:
                n = G.order() // H.order() if G and H else 0
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            try:
                h2 = H.is_subgroup(G)
            except Exception:
                h2 = all(g in G for g in H.generators)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: N is the normal core of H in G
    try:
        if not isinstance(N, PermutationGroup) or not isinstance(H, PermutationGroup) or not isinstance(G, PermutationGroup):
            h3 = False
        elif G.order() > 2000:
            h3 = False
        else:
            core_elems = set(H.elements)
            h_elems = set(H.elements)
            for g in G.elements:
                g_inv = ~g
                conj = {g * h * g_inv for h in h_elems}
                core_elems = core_elems.intersection(conj)
            h3 = (set(N.elements) == core_elems)
    except Exception:
        h3 = False

    # ¬Q: N is not a normal subgroup of G or the index of N in G does not divide n!
    try:
        n_int = int(n)
        if n_int < 0 or n_int > 1000:
            neg_q = False
        elif not isinstance(N, PermutationGroup) or not isinstance(G, PermutationGroup):
            neg_q = False
        else:
            is_normal = N.is_normal(G)
            index = G.order() // N.order()
            fact_n = math.factorial(n_int)
            divides = (fact_n % index == 0)
            neg_q = not (is_normal and divides)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: N is the normal core of H in G",
    "¬Q: N is not a normal subgroup of G or the index of N in G does not divide n!"
]

N_HYP = 3
NEG_Q_INDEX = 3