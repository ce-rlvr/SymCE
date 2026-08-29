import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, DihedralGroup, AlternatingGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    G = None
    p = None
    q = None
    
    # Unpack witness if it's a tuple (G, p, q), otherwise try to infer p and q
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            if hasattr(G, "order"):
                order = G.order()
                factors = sympy.ntheory.factorint(order)
                primes = []
                for prime, mult in factors.items():
                    primes.extend([prime] * mult)
                
                # If order is exactly the product of two primes, assign p and q
                # to satisfy p does not divide q - 1 if possible.
                if len(primes) == 2:
                    if (primes[1] - 1) % primes[0] != 0:
                        p, q = primes[0], primes[1]
                    elif (primes[0] - 1) % primes[1] != 0:
                        p, q = primes[1], primes[0]
                    else:
                        p, q = primes[0], primes[1]
    except Exception:
        pass

    # H_1: G is a finite group
    h1 = False
    try:
        if hasattr(G, "is_group") and getattr(G, "is_group"):
            h1 = True
        elif hasattr(G, "elements") and hasattr(G, "order"):
            h1 = True
        if h1:
            h1 = G.order() < float('inf')
    except Exception:
        h1 = False

    # H_2: The order of G is pq, where p and q are prime numbers
    h2 = False
    try:
        if h1 and p is not None and q is not None:
            if sympy.isprime(p) and sympy.isprime(q) and G.order() == p * q:
                h2 = True
    except Exception:
        h2 = False

    # H_3: p does not divide q - 1
    h3 = False
    try:
        if h2 and p is not None and q is not None:
            if (q - 1) % p != 0:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: G is not a cyclic group
    neg_q = False
    try:
        order = G.order()
        is_cyclic = False
        if hasattr(G, "is_cyclic") and getattr(G, "is_cyclic") is not None:
            val = getattr(G, "is_cyclic")
            is_cyclic = val() if callable(val) else val
        else:
            # Fallback: check if there is an element of order equal to the group's order
            for g in G.elements:
                if g.order() == order:
                    is_cyclic = True
                    break
        neg_q = not bool(is_cyclic)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is pq, where p and q are prime numbers",
    "H_3: p does not divide q - 1",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3