import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (q, n) or an object/dict with attributes q and n.
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
        elif hasattr(witness, 'q') and hasattr(witness, 'n'):
            q = witness.q
            n = witness.n
        else:
            q, n = witness
    except Exception:
        return [False, False, False]

    # H_1: F_q is a finite field with q elements
    try:
        if isinstance(q, int):
            q_int = q
        elif hasattr(q, 'order'):
            q_int = int(q.order)
        else:
            q_int = int(q)
            
        if q_int < 2:
            h1 = False
        else:
            factors = factorint(q_int)
            h1 = (len(factors) == 1)
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        n_int = int(n)
        h2 = (n_int >= 1) and (n_int == n)
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails at the witness
    # Conclusion: F_q contains a primitive n-th root of unity iff n divides q-1
    # Note: In characteristic p, the primitive n-th roots of unity are the primitive m-th roots 
    # of unity, where n = p^k * m and p does not divide m. Thus, F_q contains a primitive n-th 
    # root of unity iff m divides q-1.
    try:
        if h1 and h2:
            factors = factorint(q_int)
            p = list(factors.keys())[0]
            
            m = n_int
            while m % p == 0:
                m //= p
            
            # Left side of iff: F_q contains a primitive n-th root of unity
            left = ((q_int - 1) % m == 0)
            
            # Right side of iff: n divides q-1
            right = ((q_int - 1) % n_int == 0)
            
            # The conclusion is (left == right). We want its negation.
            neg_q = (left != right)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: n is a positive integer",
    "¬Q: F_q contains a primitive n-th root of unity iff n divides q-1 is false"
]

N_HYP = 2
NEG_Q_INDEX = 2