import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either a tuple (G, p, q) or just a group G (in which case
    p and q will be inferred from the prime factors of the group's order).
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            G, p, q = witness
        else:
            G = witness
            order = G.order()
            factors = sympy.ntheory.factorint(order)
            primes = []
            for prime, mult in factors.items():
                primes.extend([prime] * mult)
            
            if len(primes) == 2:
                p1, p2 = primes
                if p1 != p2:
                    # Try to assign p and q such that p does not divide q - 1
                    if (p2 - 1) % p1 != 0:
                        p, q = p1, p2
                    else:
                        p, q = p2, p1
                else:
                    p, q = p1, p2
            else:
                p, q = 0, 0
    except Exception:
        G, p, q = None, 0, 0

    # H_1: p and q are prime numbers
    try:
        h1 = bool(isprime(p) and isprime(q))
    except Exception:
        h1 = False

    # H_2: G is a group of order pq
    try:
        h2 = bool(hasattr(G, 'order') and G.order() == p * q)
    except Exception:
        h2 = False

    # H_3: p does not divide q - 1
    try:
        h3 = bool((q - 1) % p != 0)
    except Exception:
        h3 = False

    # ¬Q: G is not a cyclic group
    try:
        neg_q = bool(not G.is_cyclic)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are prime numbers",
    "H_2: G is a group of order pq",
    "H_3: p does not divide q - 1",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3