import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, factorint

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)  # V4 is isomorphic to the Sylow 2-subgroup of A4
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_normal(G, H):
    """Check if subgroup H is normal in G."""
    try:
        if hasattr(G, 'is_normal'):
            return G.is_normal(H)
    except Exception:
        pass
    
    # Fallback: H is normal in G iff g * h * ~g in H for all g in G.generators and h in H.generators
    for g in G.generators:
        g_inv = ~g
        for h in H.generators:
            if (g * h * g_inv) not in H:
                return False
    return True

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            order = G.order()
            factors = factorint(order)
            if len(factors) != 2:
                return [False, False, False]
            p, q = None, None
            for prime, exp in factors.items():
                if exp == 2:
                    p = prime
                elif exp == 1:
                    q = prime
            if p is None or q is None:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: p and q are distinct prime numbers
    try:
        h1_ok = bool(isprime(p) and isprime(q) and p != q)
    except Exception:
        h1_ok = False

    # H_2: The order of G is p^2 q
    try:
        h2_ok = bool(G.order() == (p**2) * q)
    except Exception:
        h2_ok = False

    # neg_Q: Neither the Sylow p-subgroup of G is normal in G, nor the Sylow q-subgroup of G is normal in G
    try:
        P = G.sylow_subgroup(p)
        Q = G.sylow_subgroup(q)
        
        p_normal = is_normal(G, P)
        q_normal = is_normal(G, Q)
        
        neg_q_ok = not (p_normal or q_normal)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: The order of G is p^2 q",
    "¬Q: Neither the Sylow p-subgroup nor the Sylow q-subgroup is normal in G"
]

N_HYP = 2
NEG_Q_INDEX = 2