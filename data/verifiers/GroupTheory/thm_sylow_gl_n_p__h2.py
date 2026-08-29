import sympy
import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_infinite(n):
    if n == sympy.oo or n == math.inf:
        return True
    if isinstance(n, str) and n.lower() in ['oo', 'inf', 'infinity']:
        return True
    return False

def conditions(witness):
    p = n = G = U = None
    
    # Extract variables from the witness
    if isinstance(witness, dict):
        p = witness.get('p')
        n = witness.get('n')
        G = witness.get('G')
        U = witness.get('U')
    elif hasattr(witness, 'p') and hasattr(witness, 'n'):
        p = witness.p
        n = witness.n
        G = getattr(witness, 'G', None)
        U = getattr(witness, 'U', None)
    elif isinstance(witness, tuple):
        if len(witness) == 4:
            p, n, G, U = witness
        elif len(witness) == 2:
            p, n = witness
        elif len(witness) == 3:
            p, G, U = witness
            if is_infinite(G) or is_infinite(U):
                n = sympy.oo

    # H_1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # H_2: G is the general linear group GL_n(F_p)
    try:
        if G is None or isinstance(G, str):
            h2 = True
        elif hasattr(G, 'order') and isinstance(n, int) and n >= 0:
            expected_order = (p**(n*(n-1)//2)) * math.prod(p**n - p**i for i in range(n))
            h2 = (G.order() == expected_order)
        else:
            h2 = True
    except Exception:
        h2 = False

    # H_3: U is the subgroup of G consisting of all upper unitriangular matrices
    try:
        if U is None or isinstance(U, str):
            h3 = True
        elif hasattr(U, 'order') and isinstance(n, int) and n >= 0:
            expected_order = p**(n*(n-1)//2)
            h3 = (U.order() == expected_order)
        else:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: U is not a Sylow p-subgroup of G
    # (The conclusion fails iff n is infinite, as U is always a Sylow p-subgroup for finite n)
    try:
        if is_infinite(n):
            neg_q = True
        elif hasattr(G, 'order') and hasattr(U, 'order'):
            order_G = G.order()
            order_U = U.order()
            if is_infinite(order_G) or is_infinite(order_U):
                neg_q = True
            elif order_U == 1:
                neg_q = (order_G % p == 0)
            else:
                k = sympy.factorint(order_U)
                if list(k.keys()) != [p]:
                    neg_q = True
                else:
                    index = order_G // order_U
                    neg_q = (index % p == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: G is the general linear group GL_n(F_p)",
    "H_3: U is the subgroup of G consisting of all upper unitriangular matrices",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3