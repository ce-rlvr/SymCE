import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness is expected to be the integer parameter `n` in the group presentation.
    """
    try:
        val = witness
        # Handle cases where the witness might be wrapped in a dict or tuple
        if isinstance(val, dict) and 'n' in val:
            val = val['n']
        elif isinstance(val, (list, tuple)) and len(val) == 1:
            val = val[0]
            
        # H_1: n is an integer
        if isinstance(val, int) or isinstance(val, sympy.Integer):
            n = int(val)
            h1 = True
        elif hasattr(val, 'is_integer') and val.is_integer:
            n = int(val)
            h1 = True
        else:
            h1 = False
            n = None
    except Exception:
        h1 = False
        n = None

    if not h1:
        return [False, False]

    try:
        # ¬Q: G is not isomorphic to the dihedral group D_{2n} of order 2n.
        # The true theorem requires n >= 3. 
        # For n < 3, the conclusion fails because:
        # - If n <= 0, the order of G is not 2n (it is infinite for n=0, and 2|n| != 2n for n < 0).
        # - If n = 1 or 2, G is abelian (Z_2 and V_4 respectively), whereas D_{2n} is 
        #   typically defined as the non-abelian symmetry group of a regular n-gon (n >= 3).
        neg_q = (n < 3)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: G is not isomorphic to the dihedral group D_{2n} of order 2n"
]

N_HYP = 1
NEG_Q_INDEX = 1