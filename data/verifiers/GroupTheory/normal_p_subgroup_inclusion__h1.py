import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime, factorint

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

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (G, N, P, p), checks if it is a valid counterexample to the conjecture.
    """
    try:
        G, N, P, p = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if hasattr(N, 'is_normal'):
            h2 = bool(N.is_normal(G))
        elif hasattr(N, 'is_subgroup') and N.is_subgroup(G):
            h2 = True
            for g in G.generators:
                g_inv = g**-1
                for n in N.generators:
                    if (g * n * g_inv) not in N:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # H_3: The order of N is a power of p
    try:
        h3 = False
        if h1:
            N_order = int(N.order())
            if N_order == 1:
                h3 = True
            elif N_order > 1:
                factors = factorint(N_order)
                if len(factors) == 1 and p in factors:
                    h3 = True
    except Exception:
        h3 = False

    # H_4: P is a Sylow p-subgroup of G
    try:
        h4 = False
        if h1 and hasattr(P, 'is_subgroup') and P.is_subgroup(G):
            P_order = int(P.order())
            G_order = int(G.order())
            
            is_p_group = False
            if P_order == 1:
                is_p_group = True
            elif P_order > 1:
                factors = factorint(P_order)
                if len(factors) == 1 and p in factors:
                    is_p_group = True
            
            if is_p_group:
                index = G_order // P_order
                if index % p != 0:
                    h4 = True
    except Exception:
        h4 = False

    # ¬Q: N is not a subgroup of P
    try:
        neg_q = not bool(N.is_subgroup(P))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: N is a normal subgroup of G",
    "H_3: The order of N is a power of p",
    "H_4: P is a Sylow p-subgroup of G",
    "¬Q: N is not a subgroup of P"
]

N_HYP = 4
NEG_Q_INDEX = 4