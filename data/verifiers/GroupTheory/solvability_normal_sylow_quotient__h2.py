import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.ntheory import factorint, isprime

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

def is_quotient_solvable(G, P):
    curr = G
    while True:
        derived = curr.derived_subgroup()
        gens = list(derived.generators) + list(P.generators)
        if not gens:
            gens = [Permutation()]
        next_D = PermutationGroup(gens)
        if next_D.order() == curr.order():
            break
        curr = next_D
    return curr.order() == P.order()

def conditions(witness):
    G, P, p = None, None, None
    if isinstance(witness, tuple):
        if len(witness) == 3:
            G, P, p = witness
        elif len(witness) == 2:
            G, P = witness
        elif len(witness) > 0:
            G = witness[0]
    else:
        G = witness

    try:
        h1 = getattr(G, 'is_group', False) or isinstance(G, PermutationGroup)
        if h1:
            ord_G = G.order()
            h1 = (ord_G != sympy.oo)
    except Exception:
        h1 = False

    if P is None and h1:
        try:
            ord_G = G.order()
            factors = factorint(ord_G)
            for prime in factors:
                P_cand = G.sylow_subgroup(prime)
                if P_cand.is_normal(G):
                    if is_quotient_solvable(G, P_cand):
                        P = P_cand
                        p = prime
                        break
            if P is None:
                P_cand = PermutationGroup([Permutation()])
                if is_quotient_solvable(G, P_cand):
                    P = P_cand
                    p = 2
                    while p in factors:
                        p = sympy.nextprime(p)
        except Exception:
            pass

    try:
        h2 = False
        if P is not None and (getattr(P, 'is_group', False) or isinstance(P, PermutationGroup)):
            if P.is_subgroup(G) and P.is_normal(G):
                ord_P = P.order()
                ord_G = G.order()
                if p is not None:
                    if isprime(p):
                        if ord_P == 1:
                            if ord_G % p != 0:
                                h2 = True
                        else:
                            factors = factorint(ord_P)
                            if len(factors) == 1 and p in factors:
                                if (ord_G // ord_P) % p != 0:
                                    h2 = True
                else:
                    if ord_P == 1:
                        h2 = True
                    else:
                        factors = factorint(ord_P)
                        if len(factors) == 1:
                            p_cand = list(factors.keys())[0]
                            if (ord_G // ord_P) % p_cand != 0:
                                h2 = True
    except Exception:
        h2 = False

    try:
        h3 = False
        if P is not None:
            h3 = is_quotient_solvable(G, P)
    except Exception:
        h3 = False

    try:
        neg_q = not G.is_solvable
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a normal Sylow p-subgroup of G",
    "H_3: The quotient group G/P is solvable",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3