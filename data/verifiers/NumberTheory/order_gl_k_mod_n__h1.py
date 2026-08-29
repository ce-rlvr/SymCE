import math
from sympy.ntheory import factorint
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory and linear algebra objects
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
    # H_1: k is a positive integer
    try:
        if hasattr(witness, 'k'):
            k = witness.k
        elif isinstance(witness, dict):
            k = witness['k']
        else:
            k = witness[0]
        h1 = (int(k) == k) and (k > 0)
    except Exception:
        h1 = False

    # neg_Q: The order of the group GL_k(Z/nZ) is not given by the formula
    try:
        if hasattr(witness, 'k') and hasattr(witness, 'n'):
            k = witness.k
            n = witness.n
        elif isinstance(witness, dict):
            k = witness['k']
            n = witness['n']
        else:
            k, n = witness
            
        k = int(k)
        
        # Compute actual order of GL_k(Z/nZ)
        if n == 0:
            actual = 2 if k == 1 else math.inf
        else:
            n_abs = abs(n)
            if int(n_abs) != n_abs:
                raise ValueError("n must be an integer")
            factors = factorint(int(n_abs))
            actual = 1
            for p, a in factors.items():
                term1 = p**(k**2 * (a - 1))
                term2 = 1
                for j in range(k):
                    term2 *= (p**k - p**j)
                actual *= term1 * term2
                
        # Compute formula order
        try:
            if int(n) != n:
                raise ValueError("n must be an integer")
            factors_form = factorint(int(n))
            form_val = 1
            for p, a in factors_form.items():
                term1 = p**(k**2 * (a - 1))
                term2 = 1
                for j in range(k):
                    term2 *= (p**k - p**j)
                form_val *= term1 * term2
            neg_q = (actual != form_val)
        except Exception:
            # Formula is undefined or raises an error, so the equality is false
            neg_q = True
            
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: The order of the group GL_k(Z/nZ) is not given by the formula"
]

N_HYP = 1
NEG_Q_INDEX = 1