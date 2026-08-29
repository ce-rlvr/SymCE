import math
import sympy
from sympy import ZZ, QQ, RR, CC, Rational, Integer
from sympy.abc import x, y, z, t

# Top-level setup for the namespace
# (Standard rings and fields are imported above; variables x, y, z, t are available)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: J(R) is the intersection of all maximal ideals of R",
    "¬Q: There exists y in R such that 1 - xy is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness can be:
      - An integer x (implicitly in the ring Z)
      - A tuple (n, x) representing an element x in Z/nZ
      - A tuple (R, x) where R is a SymPy ring (e.g., ZZ, QQ) and x is an element
      - A SymPy expression (implicitly in a polynomial ring)
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        ring = None
        # Parse the witness format
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, x_val = witness
            R_str = str(R_obj)
            
            if isinstance(R_obj, int) and R_obj >= 2:
                ring = 'Zn'
                n = R_obj
                x_elem = int(x_val)
            elif R_str in ['ZZ', 'Z', 'Integers', 'ZZ()'] or R_obj == ZZ:
                ring = 'Z'
                x_elem = int(x_val)
            elif R_str in ['QQ', 'Q', 'Rationals', 'QQ()'] or R_obj == QQ:
                ring = 'Field'
                x_elem = Rational(x_val)
            elif R_str in ['RR', 'R', 'Reals', 'CC', 'C', 'Complexes'] or R_obj in [RR, CC]:
                ring = 'Field'
                x_elem = x_val
            elif 'x' in R_str or 't' in R_str or 'Poly' in R_str:
                ring = 'Poly'
                x_elem = sympy.sympify(x_val)
        elif isinstance(witness, int) or isinstance(witness, Integer):
            x_elem = int(witness)
            ring = 'Z'
        elif isinstance(witness, Rational):
            x_elem = witness
            ring = 'Field'
        elif isinstance(witness, float):
            x_elem = witness
            ring = 'Field'
        elif isinstance(witness, sympy.Expr):
            x_elem = witness
            ring = 'Poly'
            
        # Evaluate conditions based on the identified ring
        if ring == 'Zn':
            h1 = True
            h2 = True  # J(R) is the intersection of all maximal ideals in any commutative ring with identity
            for y_val in range(n):
                val = (1 - x_elem * y_val) % n
                if math.gcd(val, n) != 1:
                    neg_q = True
                    break
                    
        elif ring == 'Z':
            h1 = True
            h2 = True
            # In Z, the only units are 1 and -1.
            # We check a few values of y to see if 1 - x*y is a non-unit.
            for y_val in [2, 3, 4, 5]:
                val = 1 - x_elem * y_val
                if val not in [1, -1]:
                    neg_q = True
                    break
                    
        elif ring in ['Field', 'Poly']:
            h1 = True
            h2 = True
            # In a field or polynomial ring over a field, if x != 0, 
            # we can always find y such that 1 - xy is not a unit.
            # (For a field, y = 1/x gives 1 - xy = 0. For polynomials, y = x gives 1 - x^2 which is not constant).
            if x_elem != 0:
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]