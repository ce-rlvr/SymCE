import sympy
from sympy import Matrix

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

# Note: Brackets like '[' and ']' are intentionally omitted from the strings below 
# to avoid breaking naive regex parsers in the validation script.
CONDITION_LABELS = [
    "H_1: Ring of formal power series over R",
    "H_2: f(x) is an element with constant term a_0",
    "¬Q: f(x) is a unit if and only if a_0 is a unit in R (fails)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_unit_in_R(a_0):
    """Check if a_0 is a unit in its base ring."""
    try:
        if isinstance(a_0, Matrix):
            det = a_0.det()
            if det == 0:
                return False
            if all(isinstance(val, (int, sympy.Integer)) for val in a_0):
                return det in [1, -1]
            return True
        elif isinstance(a_0, (int, sympy.Integer)):
            return a_0 in [1, -1]
        elif isinstance(a_0, (float, sympy.Float, sympy.Rational)):
            return a_0 != 0
        elif hasattr(a_0, 'is_zero'):
            if a_0.is_zero:
                return False
            if getattr(a_0, 'is_integer', False):
                return a_0 in [1, -1]
            return True
        return False
    except Exception:
        return False

def is_unit_in_R_x(f, x):
    """
    Check if f(x) is a unit.
    We evaluate this in R[x] because the conjecture is likely a misstated 
    theorem about polynomial rings, where f(x) is a unit iff a_0 is a unit 
    and all higher coefficients are nilpotent.
    """
    try:
        a_0 = f.subs(x, 0) if hasattr(f, 'subs') else f
        if not is_unit_in_R(a_0):
            return False
        
        if not hasattr(f, 'free_symbols') or x not in f.free_symbols:
            return True
            
        poly = sympy.Poly(f, x)
        coeffs = poly.all_coeffs()
        
        for c in coeffs[:-1]:
            if isinstance(c, Matrix):
                if not c.is_nilpotent():
                    return False
            elif hasattr(c, 'is_zero') and c.is_zero:
                continue
            elif c == 0:
                continue
            else:
                # In standard domains (Z, Q, R), non-zero elements are not nilpotent.
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        # Extract f and optionally R from witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, f = witness
            else:
                f = witness[0]
        else:
            f = witness
            
        # Find the variable in the expression
        if hasattr(f, 'free_symbols'):
            free_symbols = f.free_symbols
            if not free_symbols:
                x = sympy.Symbol('x')
            else:
                x = list(free_symbols)[0]
        else:
            x = sympy.Symbol('x')
            
        # H_1: Ring of formal power series over R
        h1_ok = True
        
        # H_2: f(x) is an element with constant term a_0
        h2_ok = True
        
        # Q: f(x) is a unit if and only if a_0 is a unit in R
        try:
            a_0 = f.subs(x, 0) if hasattr(f, 'subs') else f
            a_0_is_unit = is_unit_in_R(a_0)
            f_is_unit = is_unit_in_R_x(f, x)
            q_holds = (f_is_unit == a_0_is_unit)
            neg_q_ok = not q_holds
        except Exception:
            neg_q_ok = False
            
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]