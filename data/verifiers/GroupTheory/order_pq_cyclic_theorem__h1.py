import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import sympy.ntheory

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_pq(witness):
    """
    Helper function to extract p and q if the order of the witness is p*q for primes p, q.
    Returns (p, q) with p <= q, or (None, None) if the order is not a product of two primes.
    """
    try:
        if hasattr(witness, 'order'):
            if callable(witness.order):
                order = witness.order()
            else:
                order = witness.order
        elif hasattr(witness, '__len__'):
            order = len(witness)
        else:
            return None, None
        
        order = int(order)
        if order <= 1:
            return None, None
            
        factors = sympy.ntheory.factorint(order)
        if sum(factors.values()) == 2:
            primes = sorted(list(factors.keys()))
            if len(primes) == 2:
                return primes[0], primes[1]
            elif len(primes) == 1:
                return primes[0], primes[0]
    except Exception:
        pass
    return None, None

def conditions(witness) -> list[bool]:
    # H1: The order of G is pq, where p and q are prime numbers
    try:
        p, q = get_pq(witness)
        h1_ok = (p is not None and q is not None)
    except Exception:
        h1_ok = False

    # H2: p < q
    try:
        p, q = get_pq(witness)
        h2_ok = (p is not None and q is not None and p < q)
    except Exception:
        h2_ok = False

    # H3: p does not divide q - 1
    try:
        p, q = get_pq(witness)
        h3_ok = (p is not None and q is not None and (q - 1) % p != 0)
    except Exception:
        h3_ok = False

    # ¬Q: G is not a cyclic group
    try:
        if hasattr(witness, 'is_cyclic'):
            if callable(witness.is_cyclic):
                is_cyclic = bool(witness.is_cyclic())
            else:
                is_cyclic = bool(witness.is_cyclic)
        else:
            # If it doesn't have the property, it's not a cyclic group
            is_cyclic = False
        neg_q_ok = not is_cyclic
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The order of G is pq, where p and q are prime numbers",
    "H_2: p < q",
    "H_3: p does not divide q - 1",
    "¬Q: G is not a cyclic group"
]

N_HYP = 3
NEG_Q_INDEX = 3