import sympy
from sympy import symbols, solve, S, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    'Isotropy of Quadratic Forms over Algebraically Closed Fields' (missing 'q is a quadratic form' hypothesis).
    
    Witness is expected to be a tuple: (K, n, q)
    where:
      - K is the field (e.g., sympy.S.Complexes)
      - n is the dimension of the vector space (int >= 2)
      - q is a callable, a SymPy expression, or a matrix representing the map V -> K
    """
    try:
        K, n, q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: K is an algebraically closed field
    try:
        # In SymPy, S.Complexes or CC represent the algebraically closed field of complex numbers
        h1 = bool(K == S.Complexes or K == sympy.CC)
    except Exception:
        h1 = False
        
    # H_2: V is a vector space over K of dimension n >= 2
    try:
        h2 = bool(isinstance(n, int) and n >= 2)
    except Exception:
        h2 = False
        
    # ¬Q: There does NOT exist a non-zero vector v in V such that q(v) = 0
    try:
        vars = symbols(f'x0:{n}')
        
        # Evaluate q at the symbolic vector
        if hasattr(q, 'is_Matrix') and q.is_Matrix:
            v = sympy.Matrix(vars)
            expr = (v.T * q * v)[0]
        elif callable(q):
            expr = q(*vars)
        else:
            expr = q
            
        expr_simp = sympy.simplify(expr)
        
        # Check if the expression is a non-zero constant
        if hasattr(expr_simp, 'is_number') and expr_simp.is_number:
            neg_q = bool(expr_simp != 0)
        elif isinstance(expr_simp, (int, float)) or expr_simp in [S.true, S.false]:
            neg_q = bool(expr_simp != 0)
        else:
            # Solve q(v) = 0
            sols = solve(expr_simp, vars, dict=True)
            
            if not sols:
                # No solutions at all -> no non-zero solutions
                neg_q = True
            else:
                has_nonzero = False
                for sol in sols:
                    # Any free variable means we can choose it to be non-zero
                    free_vars = [v for v in vars if v not in sol]
                    if free_vars:
                        has_nonzero = True
                        break
                    
                    # If no free variables, check if any assigned value is non-zero
                    if any(sympy.simplify(sol[v]) != 0 for v in vars):
                        has_nonzero = True
                        break
                
                # The conclusion fails (neg_q is True) if there are NO non-zero solutions
                neg_q = not has_nonzero
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: V is a vector space over K of dimension n >= 2",
    "¬Q: There is no non-zero vector v in V such that q(v) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2