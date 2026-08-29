import sympy

# Top-level setup: named object bindings that the witness expression may reference
x, y, z = sympy.symbols('x y z', real=True)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: U is a simply connected open set",
    "H_2: F is a continuously differentiable vector field",
    "¬Q: F does not have a scalar potential (F is not conservative)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Parse witness: allow either a direct list/tuple of expressions, 
        # or a tuple like (U, F) where F is the vector field.
        if isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[1], '__iter__') and not isinstance(witness[1], str):
            F = list(witness[1])
        elif hasattr(witness, '__iter__') and not isinstance(witness, str):
            F = list(witness)
        else:
            return [False, False, False]
            
        n = len(F)
        if n < 1:
            return [False, False, False]
            
        # Assign variables based on dimension
        if n == 1:
            vars = [x]
        elif n == 2:
            vars = [x, y]
        elif n == 3:
            vars = [x, y, z]
        else:
            vars = sympy.symbols(f'x1:{n+1}', real=True)
            
        # H_1: U is a simply connected open set
        # We assume U is the maximal domain in R^n. R^n is simply connected.
        # We verify that F is composed of valid mathematical expressions.
        h1 = True
        for f in F:
            if not isinstance(f, sympy.Expr) and not isinstance(f, (int, float)):
                h1 = False
                break
                
        # H_2: F is a continuously differentiable vector field
        # We verify this by computing the Jacobian matrix.
        h2 = True
        jacobian = []
        try:
            for f in F:
                row = []
                for v in vars:
                    df = sympy.diff(f, v)
                    row.append(df)
                jacobian.append(row)
        except Exception:
            h2 = False
            
        # ¬Q: F does not have a scalar potential
        # On a simply connected domain, F has a scalar potential IF AND ONLY IF 
        # its Jacobian matrix is symmetric (i.e., F is irrotational).
        # Therefore, F does NOT have a potential iff the Jacobian is NOT symmetric.
        neg_q = False
        if h2:
            for i in range(n):
                for j in range(i + 1, n):
                    diff_ij = jacobian[i][j]
                    diff_ji = jacobian[j][i]
                    diff_expr = sympy.simplify(diff_ij - diff_ji)
                    if diff_expr != 0:
                        neg_q = True
                        break
                if neg_q:
                    break
                    
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]