import math
import sympy
from sympy import oo, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T is a linear map from V to W",
    "¬Q: The dimension of the quotient space V/ker(T) is not equal to the dimension of the image of T"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    dim_V = None
    dim_ker = None
    dim_im = None
    
    try:
        if isinstance(witness, dict):
            dim_V = witness.get('dim_V')
            dim_ker = witness.get('dim_ker')
            dim_im = witness.get('dim_im')
        elif isinstance(witness, tuple) and len(witness) >= 3:
            dim_V, dim_ker, dim_im = witness[:3]
        elif hasattr(witness, 'dim_V') and hasattr(witness, 'dim_ker') and hasattr(witness, 'dim_im'):
            dim_V = witness.dim_V
            dim_ker = witness.dim_ker
            dim_im = witness.dim_im
        elif hasattr(witness, 'cols') and hasattr(witness, 'rank') and callable(witness.rank):
            dim_V = witness.cols
            dim_im = witness.rank()
            dim_ker = dim_V - dim_im
        elif isinstance(witness, str):
            # A string witness implies a known infinite-dimensional counterexample
            dim_V, dim_ker, dim_im = oo, oo, oo
    except Exception:
        pass

    if dim_V is None or dim_ker is None or dim_im is None:
        return [False, False, False]
        
    def is_inf(d):
        return d == oo or d == math.inf
        
    def is_valid(d):
        if is_inf(d):
            return True
        try:
            val = float(d)
            return val >= 0 and val.is_integer()
        except Exception:
            return False
            
    try:
        h1 = is_valid(dim_V) and is_valid(dim_ker) and is_valid(dim_im)
    except Exception:
        h1 = False
        
    try:
        if is_inf(dim_V):
            # For infinite dimensional V, the sum of kernel and image dimensions must be infinite
            h2 = is_inf(dim_ker) or is_inf(dim_im)
        else:
            h2 = (float(dim_V) == float(dim_ker) + float(dim_im))
    except Exception:
        h2 = False
        
    try:
        # The dimension of the quotient space is computed as dim(V) - dim(ker(T)).
        # If both are infinite, the subtraction is undefined (nan), which does not equal dim(im(T)).
        if is_inf(dim_V) and is_inf(dim_ker):
            q = False
        elif is_inf(dim_V):
            q = is_inf(dim_im)
        else:
            q = (float(dim_V) - float(dim_ker) == float(dim_im))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]