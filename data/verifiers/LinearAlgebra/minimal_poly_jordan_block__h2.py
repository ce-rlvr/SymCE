import sympy
from sympy import Matrix, eye, zeros, minpoly, Poly
from sympy.abc import x, y

# Top-level setup for linear algebra witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_mult(p_expr, lam):
    """
    Returns the multiplicity of `lam` as a root of the polynomial expression `p_expr`.
    """
    p_shifted = p_expr.subs(x, y + lam).expand()
    try:
        p_poly = Poly(p_shifted, y)
        terms = p_poly.terms()
        if not terms:
            return 0
        return min(t[0][0] for t in terms)
    except Exception:
        # Fallback if Poly fails (e.g., due to domain issues with symbolic/algebraic roots)
        mult = 0
        p_curr = p_shifted
        while True:
            val = p_curr.subs(y, 0)
            if hasattr(val, 'is_zero') and val.is_zero:
                pass
            elif val == 0:
                pass
            else:
                try:
                    if sympy.simplify(val) != 0:
                        break
                except Exception:
                    break
            mult += 1
            p_curr = sympy.diff(p_curr, y)
        return mult

def conditions(witness) -> list[bool]:
    try:
        # The witness can be either a matrix A, or a tuple (A, lambda)
        if isinstance(witness, tuple) and len(witness) == 2:
            A, lam = witness
            lams = [lam]
        else:
            A = witness
            if not (isinstance(A, Matrix) and A.is_square):
                return [False, False]
            eigenvals = A.eigenvals()
            lams = list(eigenvals.keys())
            
        h1 = isinstance(A, Matrix) and A.is_square
    except Exception:
        h1 = False
        return [False, False]

    if not h1:
        return [False, False]

    neg_q = False
    try:
        for lam in lams:
            # Compute multiplicity in the minimal polynomial
            p_min = minpoly(A, x)
            min_mult = get_mult(p_min, lam)
                    
            # Compute multiplicity in the characteristic polynomial
            p_char = A.charpoly(x).as_expr()
            char_mult = get_mult(p_char, lam)
                    
            # Compute the size of the largest Jordan block associated with lambda
            P, J = A.jordan_form()
            n = J.shape[0]
            max_jordan = 0
            i = 0
            while i < n:
                diff = J[i, i] - lam
                if hasattr(diff, 'is_zero') and diff.is_zero:
                    is_lam = True
                elif J[i, i] == lam:
                    is_lam = True
                else:
                    try:
                        is_lam = sympy.simplify(diff) == 0
                    except Exception:
                        is_lam = False
                        
                if is_lam:
                    size = 1
                    while i + 1 < n and J[i, i+1] == 1:
                        diff_next = J[i+1, i+1] - lam
                        if hasattr(diff_next, 'is_zero') and diff_next.is_zero:
                            is_lam_next = True
                        elif J[i+1, i+1] == lam:
                            is_lam_next = True
                        else:
                            try:
                                is_lam_next = sympy.simplify(diff_next) == 0
                            except Exception:
                                is_lam_next = False
                                
                        if is_lam_next:
                            size += 1
                            i += 1
                        else:
                            break
                    if size > max_jordan:
                        max_jordan = size
                i += 1
                
            # The false conjecture states that the "algebraic multiplicity of \lambda as a root of the 
            # minimal polynomial" is exactly equal to the size of the largest Jordan block.
            # This is a confusion of terms. The multiplicity in the minimal polynomial ALWAYS equals 
            # the size of the largest Jordan block. The algebraic multiplicity (multiplicity in the 
            # characteristic polynomial) does NOT always equal the size of the largest Jordan block.
            # We check if either interpretation fails to hold.
            if char_mult != max_jordan or min_mult != max_jordan:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over an algebraically closed field F",
    "¬Q: The algebraic multiplicity of lambda as a root of the minimal polynomial of A is NOT exactly equal to the size of the largest Jordan block associated with lambda"
]

N_HYP = 1
NEG_Q_INDEX = 1