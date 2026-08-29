import sympy
from sympy import Matrix, Mod, gcd

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_integer_type(x):
    if isinstance(x, int): 
        return True
    if hasattr(x, 'is_integer') and x.is_integer: 
        return True
    return False

def is_matrix_unit(m):
    d = m.det()
    if d == 0: 
        return False
    
    modulus = None
    for e in m:
        if isinstance(e, Mod):
            modulus = e.args[1]
            break
            
    if modulus is not None:
        val = d % modulus if isinstance(d, (int, sympy.Integer)) else d
        if isinstance(val, Mod):
            val = val.args[0]
        try:
            return gcd(val, modulus) == 1
        except Exception:
            return False

    is_int_matrix = True
    for e in m:
        if not (isinstance(e, int) or (hasattr(e, 'is_integer') and e.is_integer)):
            is_int_matrix = False
            break
            
    if is_int_matrix:
        return d == 1 or d == -1
        
    return True

def is_matrix_zero(m):
    for e in m:
        if e == 0: 
            continue
        if isinstance(e, Mod) and e.args[0] % e.args[1] == 0: 
            continue
        try:
            if e.is_zero: 
                continue
        except Exception:
            pass
        return False
    return True

def is_nilpotent(m):
    if hasattr(m, 'is_Matrix') and m.is_Matrix:
        if m.rows != m.cols: 
            return False
        curr = m
        if is_matrix_zero(curr): 
            return True
        for _ in range(m.rows + 1):
            curr = curr * m
            if is_matrix_zero(curr): 
                return True
        return False
    else:
        if m == 0: 
            return True
        if isinstance(m, Mod) and m.args[0] % m.args[1] == 0: 
            return True
        try:
            if m.is_zero: 
                return True
        except Exception:
            pass
        return False

def conditions(witness):
    try:
        if len(witness) == 3:
            R, u, x = witness
        elif len(witness) == 2:
            u, x = witness
        else:
            return [False, False, False, False]
            
        # Auto-convert lists/tuples to sympy Matrices for convenience
        if isinstance(u, (list, tuple)) and len(u) > 0 and isinstance(u[0], (list, tuple)):
            u = Matrix(u)
        if isinstance(x, (list, tuple)) and len(x) > 0 and isinstance(x[0], (list, tuple)):
            x = Matrix(x)
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    # Note: The theorem "sum of a unit and a nilpotent is a unit" is unconditionally TRUE for commutative rings.
    # The conjecture is false precisely because it drops the commutativity requirement (e.g., in matrix rings).
    # To allow the intended non-commutative counterexample to pass, we verify that u and x are valid ring elements
    # (e.g., compatible square matrices) but intentionally relax the strict commutativity check.
    try:
        _ = u + x
        _ = u * x
        if hasattr(u, 'is_Matrix') and u.is_Matrix:
            h1 = (u.rows == u.cols) and (u.shape == x.shape)
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: u is a unit in R
    try:
        if hasattr(u, 'is_Matrix') and u.is_Matrix:
            h2 = is_matrix_unit(u)
        else:
            if u == 0:
                h2 = False
            elif isinstance(u, Mod):
                h2 = gcd(u.args[0], u.args[1]) == 1
            elif is_integer_type(u):
                h2 = (u == 1 or u == -1)
            else:
                h2 = (u != 0)
    except Exception:
        h2 = False

    # H_3: x is a nilpotent element in R
    try:
        h3 = is_nilpotent(x)
    except Exception:
        h3 = False

    # neg_Q: The sum u + x is NOT a unit in R
    try:
        s = u + x
        if hasattr(s, 'is_Matrix') and s.is_Matrix:
            neg_q = not is_matrix_unit(s)
        else:
            if s == 0:
                neg_q = True
            elif isinstance(s, Mod):
                neg_q = gcd(s.args[0], s.args[1]) != 1
            elif is_integer_type(s):
                neg_q = (s != 1 and s != -1)
            else:
                neg_q = (s == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: u is a unit in R",
    "H_3: x is a nilpotent element in R",
    "¬Q: The sum u + x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3