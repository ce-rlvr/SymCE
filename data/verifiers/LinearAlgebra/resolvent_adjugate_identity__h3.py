import sympy as sp

# Top-level setup for standard named objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that (tI - A)adj(tI - A) = p(t)I_n for any t.
    While this is true for any scalar t (or any matrix t that commutes with A),
    it fails when t is a matrix that does not commute with A.
    
    Expected witness: (A, t) or (A, p, t)
    where A is an n x n matrix, p is the characteristic polynomial, and t is the evaluation point.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                A, p, t = witness
                has_p = True
            elif len(witness) == 2:
                A, t = witness
                has_p = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        # H_1: A is an n x n matrix over a commutative ring R
        h1 = isinstance(A, sp.MatrixBase) and A.shape[0] == A.shape[1]
        if h1:
            # Check that all entries in A belong to a commutative ring
            h1 = all(getattr(x, 'is_commutative', True) for x in A)
            
        n = A.shape[0] if h1 else 0
        
        # H_2: p(t) = det(tI - A) is the characteristic polynomial of A
        x = sp.Symbol('x')
        if h1:
            I = sp.eye(n)
            char_poly = (x * I - A).det()
        else:
            char_poly = sp.S.Zero
            
        if has_p:
            free_syms = p.free_symbols
            if len(free_syms) == 1:
                var = list(free_syms)[0]
                p_expr = p.subs(var, x)
            else:
                p_expr = p
            h2 = sp.simplify(p_expr - char_poly) == 0
        else:
            h2 = True
            p_expr = char_poly

        # ¬Q: (tI - A)adj(tI - A) != p(t)I_n
        neg_Q = False
        if h1 and h2:
            is_matrix_t = getattr(t, 'is_Matrix', False)
            
            if is_matrix_t:
                # Evaluate p(t) as a matrix polynomial
                poly = sp.Poly(p_expr, x)
                coeffs = poly.all_coeffs()
                p_t = sp.zeros(n)
                for i, c in enumerate(coeffs):
                    power = len(coeffs) - 1 - i
                    if power == 0:
                        p_t += c * sp.eye(n)
                    else:
                        p_t += c * (t ** power)
                
                tI_A = t - A
                adj_tI_A = tI_A.adjugate()
                LHS = tI_A * adj_tI_A
                RHS = p_t
            else:
                # Evaluate p(t) as a scalar polynomial
                p_t = p_expr.subs(x, t)
                tI_A = t * I - A
                adj_tI_A = tI_A.adjugate()
                LHS = tI_A * adj_tI_A
                RHS = p_t * I
                
            diff = sp.simplify(LHS - RHS)
            if getattr(diff, 'is_Matrix', False):
                neg_Q = not diff.is_zero_matrix
            else:
                neg_Q = diff != 0

        return [bool(h1), bool(h2), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a commutative ring R",
    "H_2: p(t) is the characteristic polynomial of A",
    "¬Q: (tI - A)adj(tI - A) != p(t)I_n"
]

N_HYP = 2
NEG_Q_INDEX = 2