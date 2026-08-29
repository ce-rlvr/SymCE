import sympy
from sympy.combinatorics import Permutation, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import sympy.ntheory

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

def conditions(witness) -> list[bool]:
    # Extract G, p, q from the witness
    G = None
    p = None
    q = None
    
    if isinstance(witness, tuple):
        for item in witness:
            if hasattr(item, 'order'):
                G = item
            elif isinstance(item, int):
                if p is None:
                    p = item
                elif q is None:
                    q = item
        if G is None and len(witness) > 0:
            G = witness[0]
    else:
        G = witness

    # If p and q were not explicitly provided, infer them from the order of G
    if p is None or q is None:
        try:
            order = G.order()
            factors = sympy.ntheory.factorint(order)
            primes = list(factors.keys())
            if len(primes) == 0:
                p, q = 2, 3
            elif len(primes) == 1:
                p = primes[0]
                q = 2 if p != 2 else 3
            else:
                p, q = primes[0], primes[1]
        except Exception:
            p, q = 2, 3

    # H_1: Let p and q be prime numbers
    try:
        h1_ok = bool(sympy.ntheory.isprime(p) and sympy.ntheory.isprime(q))
    except Exception:
        h1_ok = False

    # H_2: The order of G is of the form p^a q^b for some non-negative integers a and b
    try:
        order = G.order()
        if order < 1:
            h2_ok = False
        else:
            temp = order
            if p > 1:
                while temp % p == 0:
                    temp //= p
            if q > 1:
                while temp % q == 0:
                    temp //= q
            h2_ok = (temp == 1)
    except Exception:
        h2_ok = False

    # Conclusion: G is a solvable group
    try:
        # A solvable group must be a group and have the solvable property
        if hasattr(G, 'is_solvable'):
            solvable = G.is_solvable
            if callable(solvable):
                q_ok = bool(solvable())
            else:
                q_ok = bool(solvable)
        else:
            q_ok = False
    except Exception:
        q_ok = False

    neg_q_ok = not q_ok

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers",
    "H_2: The order of G is of the form p^a q^b for some non-negative integers a and b",
    "¬Q: G is not a solvable group"
]

N_HYP = 2
NEG_Q_INDEX = 2