import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: Phi_G is the Frattini subgroup of G",
    "H_2: P is a Sylow p-subgroup of Phi_G",
    "¬Q: P is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the conjecture.
    The witness can be a tuple (G, Phi_G, P, p), a tuple (G, P, p), or a dict.
    """
    try:
        if isinstance(witness, dict):
            G = witness['G']
            P = witness['P']
            p = witness['p']
            if 'Phi_G' in witness:
                Phi_G = witness['Phi_G']
            else:
                Phi_G = G.frattini_subgroup() if callable(getattr(G, 'frattini_subgroup', None)) else G.frattini_subgroup
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                G, Phi_G, P, p = witness
            elif len(witness) == 3:
                G, P, p = witness
                Phi_G = G.frattini_subgroup() if callable(getattr(G, 'frattini_subgroup', None)) else G.frattini_subgroup
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: Phi_G is the Frattini subgroup of G
    try:
        if hasattr(G, 'is_frattini_subgroup'):
            h1 = bool(G.is_frattini_subgroup(Phi_G))
        elif hasattr(G, 'frattini_subgroup'):
            frat = G.frattini_subgroup() if callable(getattr(G, 'frattini_subgroup', None)) else G.frattini_subgroup
            h1 = bool(frat == Phi_G)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: P is a Sylow p-subgroup of Phi_G
    try:
        if hasattr(Phi_G, 'is_sylow_p_subgroup'):
            h2 = bool(Phi_G.is_sylow_p_subgroup(P, p))
        elif hasattr(Phi_G, 'is_sylow'):
            h2 = bool(Phi_G.is_sylow(P, p))
        elif hasattr(G, 'is_sylow_p_subgroup'):
            h2 = bool(G.is_sylow_p_subgroup(P, Phi_G, p))
        else:
            is_sub = False
            if hasattr(P, 'is_subgroup'):
                is_sub = P.is_subgroup(Phi_G)
            elif hasattr(Phi_G, 'has_subgroup'):
                is_sub = Phi_G.has_subgroup(P)
            elif hasattr(P, 'generators') and hasattr(Phi_G, '__contains__'):
                is_sub = all(g in Phi_G for g in P.generators)
            
            if not is_sub:
                h2 = False
            else:
                try:
                    order_Phi = Phi_G.order()
                except TypeError:
                    order_Phi = Phi_G.order
                try:
                    order_P = P.order()
                except TypeError:
                    order_P = P.order
                
                if order_P == float('inf') or order_Phi == float('inf'):
                    h2 = False
                elif p <= 1:
                    h2 = False
                else:
                    k = 0
                    temp = order_Phi
                    while temp > 0 and temp % p == 0:
                        k += 1
                        temp //= p
                    h2 = (order_P == p**k)
    except Exception:
        h2 = False

    # neg_Q: P is NOT a normal subgroup of G
    try:
        if hasattr(G, 'is_normal_subgroup'):
            neg_q = not bool(G.is_normal_subgroup(P))
        elif hasattr(P, 'is_normal_subgroup'):
            neg_q = not bool(P.is_normal_subgroup(G))
        elif hasattr(P, 'is_normal'):
            try:
                neg_q = not bool(P.is_normal(G))
            except TypeError:
                neg_q = not bool(P.is_normal)
        else:
            if hasattr(G, 'generators') and hasattr(P, 'generators') and hasattr(P, '__contains__'):
                is_normal = True
                for g in G.generators:
                    try:
                        g_inv = g**-1
                    except Exception:
                        g_inv = ~g
                    
                    # For infinite groups, we must check conjugation by both g and g^-1
                    for c, c_inv in [(g, g_inv), (g_inv, g)]:
                        for h in P.generators:
                            if (c * h * c_inv) not in P:
                                is_normal = False
                                break
                        if not is_normal:
                            break
                    if not is_normal:
                        break
                neg_q = not is_normal
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]