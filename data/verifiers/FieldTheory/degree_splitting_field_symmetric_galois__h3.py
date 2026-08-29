import math
from sympy import Poly
from sympy.abc import x
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    "H_1: F is a field",
    "H_2: f is a separable polynomial over F of degree n",
    "H_3: The Galois group of E over F is isomorphic to the symmetric group S_n",
    "¬Q: The degree of the extension E over F is not equal to n!"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1 = h2 = h3 = neg_q = False
    try:
        if isinstance(witness, dict):
            F_is_field = witness.get('F_is_field', True)
            f = witness.get('f', None)
            n = witness.get('n', None)
            gal_Sn = witness.get('galois_group_is_Sn', False)
            deg_E_F = witness.get('degree_E_F', None)
            f_is_separable = witness.get('f_is_separable', None)
        else:
            F_is_field = getattr(witness, 'F_is_field', True)
            f = getattr(witness, 'f', None)
            n = getattr(witness, 'n', None)
            gal_Sn = getattr(witness, 'galois_group_is_Sn', False)
            deg_E_F = getattr(witness, 'degree_E_F', None)
            f_is_separable = getattr(witness, 'f_is_separable', None)

        h1 = bool(F_is_field)
        
        if f is not None and n is not None:
            try:
                p = Poly(f, x)
                is_deg_n = (p.degree() == n)
                is_sep = (p.gcd(p.diff()).degree() == 0)
                h2 = is_deg_n and is_sep
            except Exception:
                h2 = False
        elif f_is_separable is not None:
            h2 = bool(f_is_separable)
            
        h3 = bool(gal_Sn)
        
        if deg_E_F is not None and n is not None:
            try:
                neg_q = (deg_E_F != math.factorial(n))
            except Exception:
                neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]