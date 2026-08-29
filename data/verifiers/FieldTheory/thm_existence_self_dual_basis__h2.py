import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup for standard algebra objects
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

def conditions(witness):
    """
    The dropped hypothesis disconnected the degree of E from n.
    witness is expected to be a tuple (p, q, n, m) where:
    - p: characteristic of F (prime)
    - q: order of F (power of p)
    - n: integer n mentioned in the hypothesis
    - m: actual degree of the extension E over F
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            q = witness.get('q')
            n = witness.get('n')
            m = witness.get('m')
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 4:
                p, q, n, m = witness[:4]
            elif len(witness) == 3:
                p, q, n = witness[:3]
                m = n
            else:
                return [False, False, False]
        else:
            p = getattr(witness, 'p', None)
            q = getattr(witness, 'q', None)
            n = getattr(witness, 'n', None)
            m = getattr(witness, 'm', None)
            
        if p is None or q is None or n is None or m is None:
            return [False, False, False]
            
        try:
            p = int(p)
            q = int(q)
            n = int(n)
            m = int(m)
        except (TypeError, ValueError):
            if hasattr(m, 'degree'):
                m = int(m.degree)
            else:
                return [False, False, False]
        
        # H_1: F is a finite field of characteristic p with q elements
        h1 = sympy.isprime(p)
        if h1:
            d = 0
            temp = q
            while temp > 1 and temp % p == 0:
                temp //= p
                d += 1
            if temp != 1 or d < 1:
                h1 = False
        
        # H_2: Either p = 2, or both q and n are odd integers
        h2 = (p == 2) or (q % 2 == 1 and n % 2 == 1)
        
        # ¬Q: E over F does not have a self-dual basis
        # A finite field extension of degree m over a field of characteristic p
        # has a self-dual basis iff p == 2 or m is odd.
        # Therefore, it fails to have a self-dual basis iff p != 2 and m is even.
        neg_q = (p != 2) and (m % 2 == 0)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a finite field of characteristic p with q elements",
    "H_2: Either p = 2, or both q and n are odd integers",
    "¬Q: E over F does not have a self-dual basis"
]

N_HYP = 2
NEG_Q_INDEX = 2