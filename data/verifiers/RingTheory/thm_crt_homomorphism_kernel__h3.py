import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I_1, I_2, ..., I_n are ideals of R",
    "¬Q: The kernel of f is not the intersection \\bigcap_{k=1}^n I_k (i.e., intersection != product)"
]

def conditions(witness):
    try:
        # Extract the list of ideals from the witness
        if isinstance(witness, tuple):
            if len(witness) == 2 and isinstance(witness[1], (list, tuple)):
                I_list = witness[1]
            elif len(witness) > 1 and all(isinstance(x, (int, sympy.Integer, sympy.Expr)) for x in witness[1:]):
                I_list = witness[1:]
            else:
                I_list = witness
        else:
            I_list = witness
            
        if not isinstance(I_list, (list, tuple)):
            return [False, False, False]
            
        h1 = True  # The ring R (e.g., ZZ or Q[x]) is implicitly valid
        
        if len(I_list) < 2:
            return [h1, False, False]
            
        is_int = all(isinstance(x, (int, sympy.Integer)) for x in I_list)
        is_expr = all(isinstance(x, (sympy.Expr, int)) for x in I_list)
        
        if is_int:
            h2 = True
            lcm_val = 1
            prod_val = 1
            for x in I_list:
                x_val = int(x)
                if x_val == 0:
                    lcm_val = 0
                    prod_val = 0
                else:
                    lcm_val = (lcm_val * x_val) // math.gcd(lcm_val, x_val)
                    prod_val = prod_val * x_val
            neg_q = abs(lcm_val) != abs(prod_val)
            
        elif is_expr:
            h2 = True
            lcm_val = sympy.S(1)
            prod_val = sympy.S(1)
            for x in I_list:
                x_sym = sympy.sympify(x)
                lcm_val = sympy.lcm(lcm_val, x_sym)
                prod_val = prod_val * x_sym
            
            if prod_val == 0:
                neg_q = (lcm_val != 0)
            else:
                ratio = sympy.cancel(lcm_val / prod_val)
                neg_q = (ratio.is_constant() is not True)
        else:
            h2 = False
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]