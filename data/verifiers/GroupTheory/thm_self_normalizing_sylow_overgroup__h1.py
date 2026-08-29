import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 4:
            return witness
        elif len(witness) == 3:
            return witness[0], witness[1], witness[2], None
    else:
        G = getattr(witness, 'G', None)
        P = getattr(witness, 'P', None)
        H = getattr(witness, 'H', None)
        p = getattr(witness, 'p', None)
        if G is not None and P is not None and H is not None:
            return G, P, H, p
    return None, None, None, None

def is_subgroup(H, G):
    if hasattr(H, 'is_subgroup'):
        try:
            return H.is_subgroup(G)
        except Exception:
            pass
    if hasattr(G, 'has_subgroup'):
        try:
            return G.has_subgroup(H)
        except Exception:
            pass
    if hasattr(H, 'generators') and hasattr(G, '__contains__'):
        return all(h in G for h in H.generators)
    if hasattr(H, 'elements') and hasattr(G, '__contains__'):
        return all(h in G for h in H.elements)
    raise AttributeError("Cannot check subgroup property")

def check_sylow(G, P, p):
    if hasattr(P, 'is_sylow'):
        try:
            return P.is_sylow(G, p)
        except Exception:
            pass
    if hasattr(G, 'is_sylow'):
        try:
            return G.is_sylow(P, p)
        except Exception:
            pass
    if hasattr(P, 'is_sylow_p_subgroup'):
        try:
            return P.is_sylow_p_subgroup(G, p)
        except Exception:
            pass
    
    if not is_subgroup(P, G):
        return False
    if hasattr(P, 'order') and hasattr(G, 'order'):
        oP = P.order()
        oG = G.order()
        if oP == 1:
            return oG % p != 0
        factors = sympy.ntheory.factorint(oP)
        if list(factors.keys()) != [p]:
            return False
        return (oG // oP) % p != 0
    raise AttributeError("Cannot check Sylow property")

def check_normalizer_in(G, A, H):
    if hasattr(G, 'normalizer'):
        try:
            N = G.normalizer(A)
            return is_subgroup(N, H)
        except Exception:
            pass
    if hasattr(A, 'normalizer_in'):
        try:
            N = A.normalizer_in(G)
            return is_subgroup(N, H)
        except Exception:
            pass
    if hasattr(G, 'elements') and hasattr(A, 'generators') and hasattr(H, '__contains__'):
        for g in G.elements:
            try:
                g_inv = g**-1
            except Exception:
                g_inv = ~g
            is_norm = True
            for a in A.generators:
                if (g * a * g_inv) not in A:
                    is_norm = False
                    break
            if is_norm:
                if g not in H:
                    return False
        return True
    raise AttributeError("Cannot compute normalizer")

def check_normalizer_equals(G, H):
    if hasattr(G, 'normalizer'):
        try:
            N = G.normalizer(H)
            if N == H: return True
            if hasattr(N, 'order') and hasattr(H, 'order') and N.order() == H.order(): return True
            return is_subgroup(N, H) and is_subgroup(H, N)
        except Exception:
            pass
    if hasattr(H, 'normalizer_in'):
        try:
            N = H.normalizer_in(G)
            if N == H: return True
            if hasattr(N, 'order') and hasattr(H, 'order') and N.order() == H.order(): return True
            return is_subgroup(N, H) and is_subgroup(H, N)
        except Exception:
            pass
    if hasattr(G, 'elements') and hasattr(H, 'generators') and hasattr(H, '__contains__'):
        for g in G.elements:
            if g not in H:
                try:
                    g_inv = g**-1
                except Exception:
                    g_inv = ~g
                is_norm = True
                for h in H.generators:
                    if (g * h * g_inv) not in H:
                        is_norm = False
                        break
                if is_norm:
                    return False
        return True
    raise AttributeError("Cannot check normalizer equality")

def conditions(witness) -> list[bool]:
    G, P, H, p = extract_witness(witness)
    if G is None:
        return [False, False, False]

    h1_ok = False
    try:
        if p is not None:
            h1_ok = bool(check_sylow(G, P, p))
        else:
            if hasattr(P, 'order'):
                oP = P.order()
                if oP > 1:
                    factors = sympy.ntheory.factorint(oP)
                    if len(factors) == 1:
                        p = list(factors.keys())[0]
                        h1_ok = bool(check_sylow(G, P, p))
            if not h1_ok and hasattr(G, 'order'):
                oG = G.order()
                for prime in sympy.ntheory.factorint(oG):
                    if check_sylow(G, P, prime):
                        p = prime
                        h1_ok = True
                        break
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if is_subgroup(H, G):
            h2_ok = bool(check_normalizer_in(G, P, H))
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        neg_q_ok = not bool(check_normalizer_equals(G, H))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "H_2: H is a subgroup of G such that N_G(P) is a subgroup of H",
    "¬Q: N_G(H) != H"
]

N_HYP = 2
NEG_Q_INDEX = 2