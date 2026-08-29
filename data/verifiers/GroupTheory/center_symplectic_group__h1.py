import sympy
from sympy import isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (n, F) or just the field characteristic p.
    """
    try:
        n = None
        p = None
        
        if isinstance(witness, tuple) and len(witness) == 2:
            n_val, F_val = witness
            n = int(n_val)
            if hasattr(F_val, 'characteristic'):
                p = int(F_val.characteristic())
            else:
                p = int(F_val)
        elif isinstance(witness, dict):
            n = int(witness.get('n', 1))
            F_val = witness.get('F', witness.get('p', 2))
            if hasattr(F_val, 'characteristic'):
                p = int(F_val.characteristic())
            else:
                p = int(F_val)
        else:
            n = 1
            if hasattr(witness, 'characteristic'):
                p = int(witness.characteristic())
            else:
                p = int(witness)
                
        # H_1: n >= 1
        h1 = (n >= 1)
        
        # H_2: G is the symplectic group Sp(2n, F)
        # We verify that F is a valid finite field by checking if its characteristic is prime.
        h2 = isprime(p)
        
        # ¬Q: The center of G does NOT consist exactly of I and -I.
        # For a field F, the center of Sp(2n, F) is {I, -I}.
        # If the characteristic of F is 2, then I = -I, so the center is just {I},
        # which has size 1 and thus does not consist exactly of two distinct elements I and -I.
        neg_q = (p == 2)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: n >= 1",
    "H_2: G is the symplectic group Sp(2n, F)",
    "¬Q: The center of G does not consist exactly of I and -I"
]

N_HYP = 2
NEG_Q_INDEX = 2