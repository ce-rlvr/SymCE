import sympy
from sympy import Matrix, Expr, Poly, Integer, Float, eye, zeros, symbols

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
x, y, z = symbols('x y z')

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # The witness might be provided as a tuple (Ring, element) or just the element
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, a = witness
        else:
            a = witness

        # Convert Poly to Expr for uniform handling
        if isinstance(a, Poly):
            a = a.as_expr()

        if isinstance(a, (int, Integer)):
            h1 = True
            h2 = (a != 0)
            neg_q = (abs(a) != 1)
            
        elif isinstance(a, (float, Float)):
            h1 = True
            h2 = (a != 0)
            neg_q = (a == 0)
            
        elif isinstance(a, Matrix):
            if a.is_square:
                h1 = True
                det = a.det()
                
                # Check regularity (det != 0)
                if hasattr(det, 'is_zero'):
                    is_z = det.is_zero
                    if is_z is None:
                        is_z = (sympy.simplify(det) == 0)
                    h2 = not is_z
                else:
                    h2 = (det != 0)
                
                # Determine if it's a matrix over Z
                is_int_matrix = True
                for val in a:
                    if isinstance(val, (float, Float)):
                        is_int_matrix = False
                        break
                    if isinstance(val, (int, Integer)):
                        continue
                    elif hasattr(val, 'is_integer') and val.is_integer:
                        continue
                    else:
                        is_int_matrix = False
                        break
                
                # Check if it is NOT a unit
                if is_int_matrix:
                    neg_q = (abs(det) != 1)
                else:
                    if isinstance(det, Expr):
                        if det.is_constant():
                            is_z = det.is_zero
                            if is_z is None:
                                is_z = (sympy.simplify(det) == 0)
                            neg_q = is_z
                        else:
                            neg_q = True
                    else:
                        neg_q = (det == 0)
                        
        elif isinstance(a, Expr):
            h1 = True
            is_z = a.is_zero
            if is_z is None:
                is_z = (sympy.simplify(a) == 0)
            h2 = not is_z
            
            if a.is_constant():
                if a.is_integer and not isinstance(a, Float):
                    neg_q = (abs(a) != 1)
                else:
                    neg_q = is_z
            else:
                neg_q = True
                
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is an element of a ring R",
    "H_2: a is a regular element in R",
    "¬Q: a is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2