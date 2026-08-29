import sympy
import sympy.ntheory
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
try:
    V4 = AbelianGroup(2, 2)
except Exception:
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

def conditions(witness) -> list[bool]:
    # The witness can be a tuple (G, p, q, n) or just the group G.
    # If it's just G, we attempt to deduce p, q, n from its order.
    if isinstance(witness, tuple) and len(witness) == 4:
        G, p, q, n = witness
    else:
        G = witness
        p, q, n = None, None, None
        try:
            order = G.order()
            factors = sympy.ntheory.factorint(order)
            if len(factors) == 2:
                p1, p2 = list(factors.keys())
                e1, e2 = factors[p1], factors[p2]
                # We need the order to be p^n * q, so q must have exponent 1.
                if e2 == 1 and p1**e1 < p2:
                    p, q, n = p1, p2, e1
                elif e1 == 1 and p2**e2 < p1:
                    p, q, n = p2, p1, e2
                elif e2 == 1:
                    p, q, n = p1, p2, e1
                elif e1 == 1:
                    p, q, n = p2, p1, e2
        except Exception:
            pass

    # H_1: p and q are distinct prime numbers
    try:
        h1 = sympy.isprime(p) and sympy.isprime(q) and p != q
    except Exception:
        h1 = False

    # H_2: n is a positive integer such that p^n < q
    try:
        h2 = (int(n) == n) and n > 0 and (p**n < q)
    except Exception:
        h2 = False

    # H_3: The order of G is p^n q
    try:
        h3 = G.order() == (p**n * q)
    except Exception:
        h3 = False

    # ¬Q: The Sylow q-subgroup of G is NOT a normal subgroup of G
    try:
        # Try using sympy's built-in methods first
        if hasattr(G, 'sylow_subgroup') and hasattr(G, 'is_normal'):
            Q_sub = G.sylow_subgroup(q)
            neg_q = not G.is_normal(Q_sub)
        else:
            raise AttributeError
    except Exception:
        # Fallback: count elements of order q.
        # If the Sylow q-subgroup has order q (which it does if |G| = p^n q),
        # it is normal if and only if there are exactly q - 1 elements of order q in G.
        try:
            order = G.order()
            if order % q == 0 and order % (q**2) != 0:
                count = 0
                for g in G.elements:
                    if g.order() == q:
                        count += 1
                neg_q = (count != q - 1)
            else:
                neg_q = False
        except Exception:
            neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "H_2: n is a positive integer such that p^n < q",
    "H_3: The order of G is p^n q",
    "¬Q: The Sylow q-subgroup of G is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3