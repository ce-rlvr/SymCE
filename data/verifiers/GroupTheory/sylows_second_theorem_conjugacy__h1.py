import sympy
from sympy.ntheory import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "Any two Sylow p-subgroups of a group G are conjugate."
    (The dropped hypothesis is that G is a finite group).
    
    Witness is expected to be a tuple: (G, p, P, Q)
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            p = witness['p']
            P = witness['P']
            Q = witness['Q']
        else:
            G, p, P, Q = witness
    except Exception:
        return [False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if hasattr(G, 'is_sylow_p_subgroup'):
            h2 = bool(G.is_sylow_p_subgroup(P, p))
        elif hasattr(P, 'is_sylow_p_subgroup'):
            h2 = bool(P.is_sylow_p_subgroup(G, p))
        else:
            h2 = False
            if P.is_subgroup(G):
                try:
                    oG = G.order()
                except TypeError:
                    oG = G.order
                try:
                    oP = P.order()
                except TypeError:
                    oP = P.order
                
                if oG != sympy.oo and oP != sympy.oo:
                    temp = oP
                    is_p_group = True
                    while temp > 1:
                        if temp % p != 0:
                            is_p_group = False
                            break
                        temp //= p
                    if is_p_group and (oG // oP) % p != 0:
                        h2 = True
    except Exception:
        h2 = False

    # H_3: Q is a Sylow p-subgroup of G
    try:
        if hasattr(G, 'is_sylow_p_subgroup'):
            h3 = bool(G.is_sylow_p_subgroup(Q, p))
        elif hasattr(Q, 'is_sylow_p_subgroup'):
            h3 = bool(Q.is_sylow_p_subgroup(G, p))
        else:
            h3 = False
            if Q.is_subgroup(G):
                try:
                    oG = G.order()
                except TypeError:
                    oG = G.order
                try:
                    oQ = Q.order()
                except TypeError:
                    oQ = Q.order
                
                if oG != sympy.oo and oQ != sympy.oo:
                    temp = oQ
                    is_p_group = True
                    while temp > 1:
                        if temp % p != 0:
                            is_p_group = False
                            break
                        temp //= p
                    if is_p_group and (oG // oQ) % p != 0:
                        h3 = True
    except Exception:
        h3 = False

    # neg_Q: P and Q are NOT conjugate in G
    try:
        if hasattr(G, 'are_conjugate_subgroups'):
            are_conj = bool(G.are_conjugate_subgroups(P, Q))
        elif hasattr(P, 'is_conjugate'):
            are_conj = bool(P.is_conjugate(Q, G))
        else:
            are_conj = False
            try:
                oP = P.order()
            except TypeError:
                oP = P.order
            try:
                oQ = Q.order()
            except TypeError:
                oQ = Q.order
                
            if oP == oQ:
                try:
                    oG = G.order()
                except TypeError:
                    oG = G.order
                if oG == sympy.oo:
                    raise ValueError("Cannot brute force infinite group")
                
                for g in G.elements:
                    match1 = True
                    for p_gen in P.generators:
                        if (g * p_gen * (~g)) not in Q:
                            match1 = False
                            break
                    if match1:
                        are_conj = True
                        break
                    
                    match2 = True
                    for p_gen in P.generators:
                        if ((~g) * p_gen * g) not in Q:
                            match2 = False
                            break
                    if match2:
                        are_conj = True
                        break
        neg_q = not are_conj
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "H_3: Q is a Sylow p-subgroup of G",
    "¬Q: P and Q are not conjugate in G"
]

N_HYP = 3
NEG_Q_INDEX = 3