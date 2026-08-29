import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to be a tuple (G, P, p) or (G, P).
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                G, P, p = witness
            elif len(witness) == 2:
                G, P = witness
                order_P = P.order()
                if order_P > 1:
                    factors = sympy.ntheory.factorint(int(order_P))
                    p = list(factors.keys())[0]
                else:
                    p = 2
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if not isinstance(P, PermutationGroup):
            h2 = False
        else:
            all_in_G = True
            for g in P.generators:
                try:
                    if not G.contains(g):
                        all_in_G = False
                        break
                except Exception:
                    all_in_G = False
                    break
            if not all_in_G:
                h2 = False
            elif not sympy.ntheory.isprime(int(p)):
                h2 = False
            else:
                order_G = G.order()
                order_P = P.order()
                k = 0
                temp = order_G
                p_int = int(p)
                while temp > 0 and temp % p_int == 0:
                    k += 1
                    temp //= p_int
                h2 = (order_P == p_int**k)
    except Exception:
        h2 = False

    # H_3: P is contained in the center of its normalizer N_G(P)
    try:
        h3 = True
        if h1 and isinstance(P, PermutationGroup):
            P_gens = P.generators
            for g in G.generate():
                normalizes = True
                for x in P_gens:
                    try:
                        conj = g * x * (~g)
                        in_P = P.contains(conj)
                    except Exception:
                        in_P = False
                    if not in_P:
                        normalizes = False
                        break
                if normalizes:
                    centralizes = True
                    for x in P_gens:
                        try:
                            conj = g * x * (~g)
                            is_eq = (conj == x)
                        except Exception:
                            is_eq = False
                        if not is_eq:
                            centralizes = False
                            break
                    if not centralizes:
                        h3 = False
                        break
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: G does not have a normal p-complement
    try:
        neg_q = False
        if h1 and isinstance(P, PermutationGroup):
            p_int = int(p)
            p_prime_elements = []
            for g in G.generate():
                try:
                    if math.gcd(int(g.order()), p_int) == 1:
                        p_prime_elements.append(g)
                except Exception:
                    pass
            
            if not p_prime_elements:
                N_order = 1
                def N_contains(x): return x.is_Identity
            else:
                N = PermutationGroup(p_prime_elements)
                N_order = N.order()
                N_contains = N.contains
            
            intersection_trivial = True
            for x in P.generate():
                if not x.is_Identity:
                    try:
                        in_N = N_contains(x)
                    except Exception:
                        in_N = False
                    if in_N:
                        intersection_trivial = False
                        break
            
            has_normal_p_complement = (N_order * P.order() == G.order()) and intersection_trivial
            neg_q = not has_normal_p_complement
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: P is contained in the center of its normalizer N_G(P)",
    "¬Q: G does not have a normal p-complement"
]

N_HYP = 3
NEG_Q_INDEX = 3