import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R and S are rings and f: R -> S is a ring homomorphism, 
    then f(x) and f(y) are orthogonal idempotents in S."
    
    The witness is expected to represent:
    - R as Z_n (integers modulo n)
    - S as Z_m (integers modulo m)
    - f as a mapping (dict, list, or callable) from Z_n to Z_m
    - x, y as elements of Z_n
    
    Format can be a tuple (n, m, f, x, y) or a dict with these keys.
    """
    # H_1: R and S are rings
    try:
        if isinstance(witness, dict):
            n = witness.get('n', witness.get('R'))
            m = witness.get('m', witness.get('S'))
            f = witness['f']
            x = witness['x']
            y = witness['y']
        else:
            n, m, f, x, y = witness
            
        if hasattr(n, 'order'):
            n = n.order()
        if hasattr(m, 'order'):
            m = m.order()
            
        n = int(n)
        m = int(m)
        h1 = (n >= 1) and (m >= 1)
    except Exception:
        h1 = False

    # H_2: f: R -> S is a ring homomorphism
    try:
        if not h1:
            h2 = False
        else:
            if callable(f):
                f_val = lambda a: int(f(a)) % m
            elif isinstance(f, (dict, list, tuple)):
                f_val = lambda a: int(f[int(a)]) % m
            else:
                raise ValueError
            
            h2 = True
            # Check preservation of multiplicative identity
            if f_val(1 % n) != 1 % m:
                h2 = False
            else:
                # Check preservation of addition and multiplication
                for a in range(n):
                    for b in range(n):
                        if f_val((a + b) % n) != (f_val(a) + f_val(b)) % m:
                            h2 = False
                            break
                        if f_val((a * b) % n) != (f_val(a) * f_val(b)) % m:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # ¬Q: f(x) and f(y) are NOT orthogonal idempotents in S
    try:
        if not h1:
            neg_q = False
        else:
            x_val = int(x) % n
            y_val = int(y) % n
            
            if callable(f):
                fx = int(f(x_val)) % m
                fy = int(f(y_val)) % m
            elif isinstance(f, (dict, list, tuple)):
                fx = int(f[x_val]) % m
                fy = int(f[y_val]) % m
            else:
                raise ValueError
            
            is_idem_fx = (fx * fx) % m == fx
            is_idem_fy = (fy * fy) % m == fy
            is_ortho = ((fx * fy) % m == 0) and ((fy * fx) % m == 0)
            
            q = is_idem_fx and is_idem_fy and is_ortho
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: f(x) and f(y) are not orthogonal idempotents in S"
]

N_HYP = 2
NEG_Q_INDEX = 2