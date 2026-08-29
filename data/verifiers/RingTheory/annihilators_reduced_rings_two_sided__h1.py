import itertools
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class Z2_Matrix:
    """A simple wrapper for 2x2 matrices over Z/2Z to be used as a finite ring."""
    def __init__(self, mat):
        self.mat = mat.applyfunc(lambda x: x % 2)
        
    def __add__(self, other):
        return Z2_Matrix(self.mat + other.mat)
        
    def __mul__(self, other):
        return Z2_Matrix(self.mat * other.mat)
        
    def __eq__(self, other):
        if not isinstance(other, Z2_Matrix):
            return False
        return self.mat == other.mat
        
    def __hash__(self):
        return hash(tuple(self.mat))
        
    def __repr__(self):
        return f"Z2_Matrix({self.mat.tolist()})"

# M2_Z2 is the ring of 2x2 matrices over Z/2Z (16 elements)
M2_Z2 = []
for entries in itertools.product([0, 1], repeat=4):
    M2_Z2.append(Z2_Matrix(Matrix(2, 2, entries)))


def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    Expected witness format: (R, x, L)
    where R is an iterable of ring elements, x is an element in R, and L is a subset of R.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        R_input, x, L_input = witness
        
        # Safely extract R and L to prevent infinite loops
        R = []
        for i, elem in enumerate(R_input):
            if i > 1000:
                return [False, False, False]
            R.append(elem)
            
        L = []
        for i, elem in enumerate(L_input):
            if i > 1000:
                return [False, False, False]
            L.append(elem)
            
    except Exception:
        return [False, False, False]
        
    # H_1: x is an element of R
    try:
        h1 = False
        for elem in R:
            if x == elem:
                h1 = True
                break
    except Exception:
        h1 = False
        
    # H_2: L is the left annihilator of x
    try:
        # Find the zero element of the ring
        zero = None
        for z in R:
            is_zero = True
            for a in R:
                if not (z + a == a):
                    is_zero = False
                    break
            if is_zero:
                zero = z
                break
                
        if zero is None:
            h2 = False
        else:
            expected_L = []
            for a in R:
                if a * x == zero:
                    expected_L.append(a)
            
            # Check set equality between L and expected_L
            h2 = True
            if len(L) != len(expected_L):
                h2 = False
            else:
                for a in expected_L:
                    if a not in L:
                        h2 = False
                for a in L:
                    if a not in expected_L:
                        h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: L is not a two-sided ideal of R
    try:
        is_ideal = True
        if zero not in L:
            is_ideal = False
            
        # Check closure under addition
        for a in L:
            for b in L:
                if (a + b) not in L:
                    is_ideal = False
                    
        # Check left and right absorption
        for a in L:
            for r in R:
                if (r * a) not in L:
                    is_ideal = False
                if (a * r) not in L:
                    is_ideal = False
                    
        neg_q = not is_ideal
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "H_2: L is the left annihilator of x",
    "¬Q: L is not a two-sided ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2