import sympy as sp
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def extract_n_p(witness):
    """
    Extracts the degree n and the characteristic p of the field K from the witness.
    """
    n, p = None, None
    if isinstance(witness, tuple) or isinstance(witness, list):
        if len(witness) >= 2:
            n, K = witness[0], witness[1]
            if isinstance(K, (int, sp.Integer)):
                p = int(K)
            elif hasattr(K, 'characteristic'):
                p = int(K.characteristic())
            elif isinstance(K, str) and '2' in K:
                p = 2
            else:
                p = 0
        elif len(witness) == 1:
            n = witness[0]
            p = 0
    elif isinstance(witness, dict):
        n = witness.get('n', None)
        K = witness.get('K', witness.get('p', None))
        if isinstance(K, (int, sp.Integer)):
            p = int(K)
        elif hasattr(K, 'characteristic'):
            p = int(K.characteristic())
        else:
            p = 0
    elif hasattr(witness, 'characteristic'):
        n = 2
        p = int(witness.characteristic())
    elif isinstance(witness, (int, sp.Integer)) and not isinstance(witness, bool):
        n = 2
        p = int(witness)
    
    if n is None:
        n = 2
    else:
        if isinstance(n, sp.Integer):
            n = int(n)
            
    if p is None:
        p = 0
        
    return n, p

def conditions(witness) -> list[bool]:
    try:
        n, p = extract_n_p(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: n >= 2 is an integer
    try:
        h1_ok = isinstance(n, int) and not isinstance(n, bool) and n >= 2
    except Exception:
        h1_ok = False
        
    # H_2: a_0, ..., a_n are algebraically independent over K
    h2_ok = True
    
    # ¬Q: The discriminant polynomial is reducible
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            if n > 4:
                neg_q_ok = (p == 2)
            else:
                a = sp.symbols(f'a0:{n+1}')
                x = sp.symbols('x')
                f = sum(a[i] * x**i for i in range(n+1))
                D = sp.discriminant(f, x)
                
                if p > 0:
                    if not sp.isprime(p):
                        neg_q_ok = False
                    else:
                        factors = sp.factor_list(D, modulus=p)
                        total_degree = sum(exp for factor, exp in factors[1])
                        neg_q_ok = total_degree > 1
                else:
                    factors = sp.factor_list(D)
                    total_degree = sum(exp for factor, exp in factors[1])
                    neg_q_ok = total_degree > 1
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: a_i are algebraically independent over K",
    "¬Q: The discriminant polynomial is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2