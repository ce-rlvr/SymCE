import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: PN/N is not a Sylow p-subgroup of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        G, N, p, P = witness
    except Exception:
        return [False, False, False, False]

    # 1. Integer representation (representing subgroups of the infinite group Z)
    # In Z, a subgroup is nZ, represented by the integer n >= 0.
    # N <= G iff G divides N.
    if type(G) is int and type(N) is int and type(p) is int and type(P) is int:
        try:
            # H1: N is a normal subgroup of G (all subgroups of Z are normal)
            if G == 0:
                h1 = (N == 0)
            else:
                h1 = (N % G == 0)
                
            # H2: p is a prime number
            h2 = bool(sympy.isprime(p))
            
            # H3: P is a Sylow p-subgroup of G
            # In Z, the only elements of finite order are 0, so the unique p-subgroup is {0} (n=0).
            h3 = (P == 0) and (G >= 0)
            
            # neg_Q: PN/N is NOT a Sylow p-subgroup of G/N
            # PN = gcd(P, N) = gcd(0, N) = N. So PN/N is the trivial group (order 1).
            # G/N has order N/G (if N > 0).
            # The trivial group is a Sylow p-subgroup of G/N iff p does not divide |G/N|.
            # Thus, it is NOT a Sylow p-subgroup iff p divides |G/N|.
            if N == 0:
                neg_q = False
            else:
                neg_q = ((N // G) % p == 0)
                
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Duck-typing for Sympy PermutationGroup or similar finite group objects
    h1 = False
    try:
        if hasattr(N, 'is_normal'):
            h1 = bool(N.is_subgroup(G) and N.is_normal(G))
        elif hasattr(N, 'is_normal_subgroup'):
            h1 = bool(N.is_normal_subgroup(G))
    except Exception:
        pass

    h2 = False
    try:
        h2 = bool(sympy.isprime(p))
    except Exception:
        pass

    h3 = False
    try:
        if hasattr(P, 'is_sylow_p_subgroup'):
            h3 = bool(P.is_sylow_p_subgroup(G, p))
        else:
            if P.is_subgroup(G):
                order_P = P.order()
                order_G = G.order()
                if order_P == 1:
                    is_p_grp = True
                else:
                    factors = sympy.factorint(order_P)
                    is_p_grp = (list(factors.keys()) == [p])
                idx = order_G // order_P
                h3 = bool(is_p_grp and (idx % p != 0))
    except Exception:
        pass

    neg_q = False
    try:
        if hasattr(G, 'quotient'):
            # Custom class with quotient method
            PN = P.join(N) if hasattr(P, 'join') else P * N
            G_N = G.quotient(N)
            PN_N = PN.quotient(N)
            if hasattr(PN_N, 'is_sylow_p_subgroup'):
                neg_q = not bool(PN_N.is_sylow_p_subgroup(G_N, p))
            else:
                idx = G_N.order() // PN_N.order()
                neg_q = bool(idx % p == 0)
        else:
            # Sympy PermutationGroup
            gens = list(P.generators) + list(N.generators)
            PN = PermutationGroup(gens)
            order_PN = PN.order()
            order_G = G.order()
            if order_G % order_PN == 0:
                idx = order_G // order_PN
                neg_q = bool(idx % p == 0)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]