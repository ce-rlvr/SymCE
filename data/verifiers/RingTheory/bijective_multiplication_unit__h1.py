import sympy
from sympy import *
import itertools

# Top-level setup
class NonAssocRing:
    """
    A finite non-associative ring over Z_2 to serve as a witness.
    Basis: e1 (identity), e2, e3.
    Multiplication rules:
    e1 * x = x * e1 = x
    e2 * e2 = e1
    e2 * e3 = e3 * e2 = 0
    e3 * e3 = 0
    """
    def __init__(self):
        self.elements = [(c1, c2, c3) for c1 in (0,1) for c2 in (0,1) for c3 in (0,1)]
        self.zero = (0,0,0)
        self.one = (1,0,0)
        
    def add(self, x, y):
        return ((x[0]+y[0])%2, (x[1]+y[1])%2, (x[2]+y[2])%2)
        
    def mul(self, x, y):
        c1, c2, c3 = x
        d1, d2, d3 = y
        return ((c1*d1 + c2*d2)%2, (c1*d2 + c2*d1)%2, (c1*d3 + c3*d1)%2)

R_nonassoc = NonAssocRing()
u_elem = (0,1,0)  # This element is a unit but its left multiplication map is not bijective

def conditions(witness):
    try:
        R, a = witness
    except Exception:
        return [False, False]
        
    # H_1: a is an element of R
    try:
        h1 = a in R.elements
    except Exception:
        h1 = False
        
    # Conclusion: a is a unit iff L_a and R_a are bijective
    try:
        # Check if a is a unit (has a two-sided inverse)
        is_unit = False
        if hasattr(R, 'one'):
            for b in R.elements:
                if R.mul(a, b) == R.one and R.mul(b, a) == R.one:
                    is_unit = True
                    break
        else:
            is_unit = False
            
        # Check if L_a is bijective
        L_a_image = []
        for x in R.elements:
            L_a_image.append(R.mul(a, x))
        L_a_unique = []
        for y in L_a_image:
            if y not in L_a_unique:
                L_a_unique.append(y)
        L_a_bijective = (len(L_a_unique) == len(R.elements))
        
        # Check if R_a is bijective
        R_a_image = []
        for x in R.elements:
            R_a_image.append(R.mul(x, a))
        R_a_unique = []
        for y in R_a_image:
            if y not in R_a_unique:
                R_a_unique.append(y)
        R_a_bijective = (len(R_a_unique) == len(R.elements))
        
        both_bijective = L_a_bijective and R_a_bijective
        
        # The conjecture claims: a is a unit iff both maps are bijective
        conclusion = (is_unit == both_bijective)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of R",
    "¬Q: It is NOT true that (a is a unit iff L_a and R_a are bijective)"
]

N_HYP = 1
NEG_Q_INDEX = 1