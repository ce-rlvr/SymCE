import sympy
from sympy import Matrix, MatrixBase, Poly, Symbol, zeros, eye, sympify
from sympy.abc import x

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either:
      - A tuple (T, p_list) where T is a matrix and p_list is a list of tuples (p_i(x), m_i)
      - Just a matrix T (in which case we test if it decomposes into generalized eigenspaces over its base field)
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            T, p_list = witness
            if isinstance(p_list, dict):
                p_list = list(p_list.items())
        else:
            T = witness
            p_list = None
            
        # H_1: V is a finite-dimensional vector space over a field F
        # Represented by T being a square matrix
        h1 = isinstance(T, MatrixBase) and T.is_square
        
        # H_2: T is a linear operator on V
        h2 = h1
        
        if not (h1 and h2):
            return [False, False, False]
            
        n = T.shape[0]
        
        if p_list is not None:
            x_sym = Symbol('x')
            basis_vectors = []
            for item in p_list:
                if isinstance(item, tuple):
                    p_expr, m = item
                else:
                    p_expr = item
                    m = 1
                
                if isinstance(p_expr, Poly):
                    poly = p_expr
                else:
                    p_expr = sympify(p_expr)
                    free_syms = p_expr.free_symbols
                    gen = list(free_syms)[0] if len(free_syms) == 1 else x_sym
                    poly = Poly(p_expr, gen)
                    
                coeffs = poly.all_coeffs()
                p_T = zeros(n, n)
                deg = len(coeffs) - 1
                for i, c in enumerate(coeffs):
                    p_T += c * (T ** (deg - i))
                    
                p_T_m = p_T ** m
                nullspace = p_T_m.nullspace()
                basis_vectors.extend(nullspace)
                
            # Check if the sum of the subspaces is direct and equals V
            if len(basis_vectors) == n:
                if n == 0:
                    q = True
                else:
                    M = Matrix.hstack(*basis_vectors)
                    q = (M.rank() == n)
            else:
                q = False
        else:
            # Fallback: if no polynomials are provided, check if T decomposes 
            # into generalized eigenspaces over its base field.
            is_rational_matrix = True
            for val in T:
                if not getattr(val, 'is_Rational', False):
                    is_rational_matrix = False
                    break
                    
            eigenvals = T.eigenvals()
            sum_mult = 0
            for val, mult in eigenvals.items():
                if is_rational_matrix:
                    if getattr(val, 'is_Rational', False):
                        sum_mult += mult
                else:
                    if getattr(val, 'is_real', False):
                        sum_mult += mult
            q = (sum_mult == n)
            
        neg_q = not q
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is a linear operator on V",
    "¬Q: V does not decompose into a direct sum of T-invariant subspaces V_i = ker(p_i(T)^{m_i})"
]

N_HYP = 2
NEG_Q_INDEX = 2