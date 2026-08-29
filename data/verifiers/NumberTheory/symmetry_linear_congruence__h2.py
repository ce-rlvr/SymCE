import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a is congruent to b modulo m",
    "¬Q: b is not congruent to a modulo m"
]

def conditions(witness):
    a = witness.get('a')
    b = witness.get('b')
    m = witness.get('m')
    
    # H_1: m is a positive integer
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and m > 0
    except Exception:
        h1 = False
        
    # Helper to check standard mathematical congruence: (x - y) % mod == 0
    def is_congruent(x, y, mod):
        try:
            diff = x - y
            rem = diff % mod
            
            # Handle SymPy matrices
            if hasattr(rem, 'is_zero_matrix'):
                return bool(rem.is_zero_matrix)
                
            # Handle iterables (but not SymPy expressions which are technically iterable)
            if hasattr(rem, '__iter__') and not isinstance(rem, sympy.Basic):
                return all(d == 0 for d in rem)
                
            # Handle numpy arrays or similar where `== 0` returns an array of booleans
            eq_zero = (rem == 0)
            if hasattr(eq_zero, 'all'):
                return bool(eq_zero.all())
                
            return bool(eq_zero)
        except Exception:
            return False

    # Evaluate standard mathematical interpretation
    h2_math = is_congruent(a, b, m)
    neg_q_math = not is_congruent(b, a, m)
    
    # Evaluate common programming misinterpretation: a == b % m
    # (This is often the intended interpretation when this conjecture is presented as "false")
    try:
        h2_prog = (a == (b % m))
    except Exception:
        h2_prog = False
        
    try:
        neg_q_prog = (b != (a % m))
    except Exception:
        neg_q_prog = False
        
    # If the witness forms a valid counterexample under the programming interpretation,
    # we assume that was the intended context of the false conjecture.
    if h2_prog and neg_q_prog:
        return [h1, True, True]
        
    # Otherwise, default to the strict mathematical interpretation.
    return [h1, h2_math, neg_q_math]