import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Given a witness object, checks whether it is a valid counterexample to the false conjecture.
    The theorem is true for finite groups, so a valid counterexample must be an infinite group.
    """
    # Extract G, N, p, P
    try:
        if isinstance(witness, tuple) or isinstance(witness, list):
            G, N, p, P = witness[:4]
        else:
            G = witness.G
            N = witness.N
            p = witness.p
            P = witness.P
    except Exception:
        return [False, False, False, False]

    # H_1: N is a normal subgroup of G
    h1 = False
    try:
        if hasattr(N, 'is_normal'):
            h1 = bool(N.is_normal(G))
        elif hasattr(G, 'is_normal_subgroup'):
            h1 = bool(G.is_normal_subgroup(N))
        else:
            h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        pass

    # H_2: p is a prime number
    h2 = False
    try:
        h2 = bool(isprime(p))
    except Exception:
        pass

    # H_3: P is a Sylow p-subgroup of G
    h3 = False
    try:
        if hasattr(P, 'is_sylow'):
            h3 = bool(P.is_sylow(G, p))
        elif hasattr(G, 'is_sylow_subgroup'):
            h3 = bool(G.is_sylow_subgroup(P, p))
        else:
            if P.is_subgroup(G):
                order_P = P.order()
                order_G = G.order()
                if order_P == 1 and order_G % p != 0:
                    h3 = True
                else:
                    temp = order_P
                    while temp % p == 0 and temp > 1:
                        temp //= p
                    if temp == 1 and (order_G // order_P) % p != 0:
                        h3 = True
    except Exception:
        pass

    # ¬Q: PN/N is NOT a Sylow p-subgroup of G/N
    neg_q = False
    try:
        if hasattr(witness, 'neg_Q'):
            neg_q = bool(witness.neg_Q() if callable(witness.neg_Q) else witness.neg_Q)
        elif hasattr(G, 'is_sylow_quotient'):
            neg_q = not bool(G.is_sylow_quotient(N, P, p))
        elif hasattr(G, 'quotient') and hasattr(P, 'join'):
            Q_group = G.quotient(N)
            PN = P.join(N)
            PN_mod_N = PN.quotient(N)
            neg_q = not bool(PN_mod_N.is_sylow(Q_group, p))
        else:
            # Try to compute for SymPy finite groups (will correctly yield False for finite groups)
            if hasattr(P, 'join'):
                PN = P.join(N)
            elif hasattr(P, '__mul__'):
                try:
                    PN = P * N
                except Exception:
                    PN = PermutationGroup(list(P.generators) + list(N.generators))
            else:
                PN = PermutationGroup(list(P.generators) + list(N.generators))
            
            order_PN = PN.order()
            order_N = N.order()
            order_G = G.order()
            
            order_quotient = order_PN // order_N
            temp = order_quotient
            is_p_group = True
            if temp != 1:
                while temp % p == 0 and temp > 1:
                    temp //= p
                if temp != 1:
                    is_p_group = False
            
            if not is_p_group:
                neg_q = True
            else:
                index = (order_G // order_N) // order_quotient
                if index % p == 0:
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: p is a prime number",
    "H_3: P is a Sylow p-subgroup of G",
    "¬Q: PN/N is not a Sylow p-subgroup of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3