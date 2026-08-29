import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The order of the quotient group N_G(P) / P is not coprime to p"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            P = witness.get('P')
        else:
            G, p, P = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime number
    try:
        if not isinstance(p, (int, sympy.Integer)):
            h1 = False
        else:
            h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: P is a Sylow p-subgroup of G
    try:
        if hasattr(G, 'is_sylow_p_subgroup'):
            h2 = bool(G.is_sylow_p_subgroup(P, p))
        elif hasattr(G, 'is_sylow'):
            h2 = bool(G.is_sylow(P, p))
        else:
            if not P.is_subgroup(G):
                h2 = False
            else:
                order_P = P.order()
                order_G = G.order()
                if order_G == sympy.oo:
                    h2 = False
                else:
                    temp = order_P
                    is_p_group = True
                    if temp == 1:
                        is_p_group = True
                    else:
                        while temp % p == 0 and temp > 1:
                            temp //= p
                        if temp != 1:
                            is_p_group = False
                    
                    if not is_p_group:
                        h2 = False
                    else:
                        h2 = (math.gcd(int(order_G // order_P), int(p)) == 1)
    except Exception:
        h2 = False

    # ¬Q: The order of the quotient group N_G(P) / P is not coprime to p
    try:
        if hasattr(G, 'normalizer_quotient_order'):
            q_order = G.normalizer_quotient_order(P)
        elif hasattr(G, 'normalizer'):
            N = G.normalizer(P)
            q_order = N.order() // P.order()
        else:
            # Fallback for SymPy PermutationGroup
            P_elements = set(P.elements)
            norm_elems = []
            for g in G.elements:
                is_norm = True
                g_inv = ~g
                for p_elem in P_elements:
                    if (g * p_elem * g_inv) not in P_elements:
                        is_norm = False
                        break
                if is_norm:
                    norm_elems.append(g)
            q_order = len(norm_elems) // P.order()

        if q_order == sympy.oo:
            neg_q = True
        else:
            neg_q = (math.gcd(int(q_order), int(p)) != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]