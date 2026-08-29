import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import sympy.ntheory

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

def is_subgroup(P, G):
    try:
        for gen in P.generators:
            if gen not in G:
                return False
        return True
    except Exception:
        return False

def is_sylow_p_subgroup(G, P):
    if not is_subgroup(P, G):
        return False
    order_P = P.order()
    order_G = G.order()
    if order_G % order_P != 0:
        return False
    if order_P == 1:
        return True
    factors = sympy.ntheory.factorint(order_P)
    if len(factors) != 1:
        return False
    p = list(factors.keys())[0]
    if (order_G // order_P) % p == 0:
        return False
    return True

def in_center(z, P):
    if z not in P:
        return False
    for gen in P.generators:
        if z * gen != gen * z:
            return False
    return True

def in_normalizer(n, P):
    for gen in P.generators:
        if (n * gen * ~n) not in P:
            return False
    return True

def conditions(witness):
    try:
        if len(witness) == 4:
            G, P, x, y = witness
            g_given = None
        elif len(witness) == 5:
            G, P, x, y, g_given = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = is_sylow_p_subgroup(G, P)
    except Exception:
        h2 = False

    try:
        h3 = in_center(x, P) and in_center(y, P)
    except Exception:
        h3 = False

    h4 = False
    q_holds = False
    try:
        if h1 and h2 and h3:
            if g_given is not None:
                if g_given in G and g_given * x * ~g_given == y:
                    h4 = True
            
            if G.order() <= 10000:
                for g in G.elements:
                    if g * x * ~g == y:
                        h4 = True
                        if in_normalizer(g, P):
                            q_holds = True
                            break
            else:
                # If G is too large, we cannot exhaustively check Q within time limits.
                # To avoid false positives for neg_Q, we assume Q holds.
                q_holds = True 
    except Exception:
        pass

    try:
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: x and y are elements in the center Z(P) of P",
    "H_4: There exists an element g in G such that g x g^{-1} = y",
    "¬Q: There is no element n in N_G(P) such that n x n^{-1} = y"
]

N_HYP = 4
NEG_Q_INDEX = 4