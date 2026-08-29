import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Symbol

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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture:
    "f is a unit in A if and only if f(1) != 0"
    where A is the ring of arithmetic functions from the positive integers to a field K.
    
    Since the theorem is unconditionally true for all arithmetic functions over any field K,
    the only way the conclusion can fail is if the dropped hypothesis "f is an arithmetic function"
    is violated (i.e., f is not an element of A, so it cannot be a unit in A, but f(1) != 0 might still hold).
    """
    h1 = True
    h2 = True
    
    try:
        # Unpack witness if it's a tuple of (K, f)
        if isinstance(witness, tuple) and len(witness) == 2:
            K, f = witness
            if hasattr(K, 'is_Field'):
                h1 = bool(K.is_Field)
        else:
            f = witness

        # Evaluate f(1) and determine if f is an arithmetic function (i.e., in A)
        if callable(f):
            f1 = f(1)
            is_in_A = True
        elif hasattr(f, 'subs'):
            # A symbolic expression is not a function from positive integers to K
            free_vars = list(f.free_symbols)
            if free_vars:
                f1 = f.subs(free_vars[0], 1)
            else:
                f1 = f
            is_in_A = False
        elif isinstance(f, (list, tuple)):
            f1 = f[1] if len(f) > 1 else 0
            is_in_A = True
        elif isinstance(f, dict):
            f1 = f.get(1, 0)
            is_in_A = True
        else:
            f1 = f
            is_in_A = False
            
        f1_not_zero = bool(f1 != 0)
        
        # If f is an arithmetic function over a field, it is a unit iff f(1) != 0.
        # If f is not an arithmetic function, it is not in A, so it is not a unit in A.
        if is_in_A:
            is_unit = f1_not_zero
        else:
            is_unit = False
            
        # The conclusion fails if the biconditional is false
        neg_q = not (is_unit == f1_not_zero)
        
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: A is the ring of arithmetic functions from the positive integers to K, equipped with pointwise addition and Dirichlet convolution",
    "¬Q: f is a unit in A if and only if f(1) != 0 is false"
]

N_HYP = 2
NEG_Q_INDEX = 2