import sympy
from sympy.combinatorics.named_groups import CyclicGroup, SymmetricGroup, AlternatingGroup, DihedralGroup
from sympy.ntheory import factorint, n_order
from sympy.matrices import eye, zeros
from math import gcd

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    q, n, alpha, m, k = None, None, None, None, None
    if isinstance(witness, dict):
        q = witness.get('q', witness.get('F_q'))
        n = witness.get('n', witness.get('F_qn'))
        alpha = witness.get('alpha')
        m = witness.get('m')
        k = witness.get('k')
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 4:
            q, n, alpha, m = witness[:4]
        if len(witness) >= 5:
            k = witness[4]
    else:
        q = getattr(witness, 'q', getattr(witness, 'F_q', None))
        n = getattr(witness, 'n', getattr(witness, 'F_qn', None))
        alpha = getattr(witness, 'alpha', None)
        m = getattr(witness, 'm', None)
        k = getattr(witness, 'k', None)
            
    return q, n, alpha, m, k

def is_prime_power(q):
    try:
        q = int(q)
        if q < 2:
            return False
        return len(factorint(q)) == 1
    except Exception:
        return False

def is_positive_integer(n):
    try:
        n = int(n)
        return n >= 1
    except Exception:
        return False

def find_k(q, n, alpha, k_from_witness):
    if k_from_witness is not None:
        try:
            return int(k_from_witness)
        except Exception:
            pass
            
    if alpha is None:
        return None
        
    try:
        k = 1
        val = alpha ** q
        limit = max(int(n), 100) if n is not None else 100
        while val != alpha and k <= limit:
            val = val ** q
            k += 1
        if val == alpha:
            return k
    except Exception:
        pass
        
    return None

def get_order(q, m):
    try:
        q = int(q)
        m = int(m)
        if m < 1:
            return None
        if m == 1:
            return 1
        if gcd(q, m) != 1:
            return None
        return n_order(q, m)
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    try:
        q, n, alpha, m, k_from_witness = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    h1 = is_prime_power(q)
    h2 = is_positive_integer(n)
    
    try:
        k = find_k(q, n, alpha, k_from_witness)
        if k is None:
            neg_q = False
        else:
            order = get_order(q, m)
            if order is None:
                neg_q = True
            else:
                neg_q = (k != order)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: F_{q^n} is an extension field of degree n over F_q",
    "¬Q: The smallest positive integer k such that alpha^{q^k} = alpha is NOT equal to the multiplicative order of q modulo m"
]

N_HYP = 2
NEG_Q_INDEX = 2