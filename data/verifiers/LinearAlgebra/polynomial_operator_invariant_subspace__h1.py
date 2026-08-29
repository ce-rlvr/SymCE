import sympy
from sympy.matrices import MatrixBase

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    witness is expected to be a tuple: (T, U, p)
    where:
      - T is a sympy Matrix representing the linear operator on V.
      - U is a sympy Matrix whose columns form a basis for the subspace U.
      - p is a sympy expression representing the polynomial p(x).
    """
    try:
        T, U, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: T is a linear operator on V
    try:
        h1 = isinstance(T, MatrixBase) and T.is_square
    except Exception:
        h1 = False
        
    # H2: U is a T-invariant subspace of V
    try:
        if not isinstance(U, MatrixBase) or U.shape[0] != T.shape[0]:
            h2 = False
        else:
            rk_U = U.rank()
            rk_TU = U.row_join(T * U).rank()
            h2 = (rk_U == rk_TU)
    except Exception:
        h2 = False
        
    # H3: p(x) is a polynomial with coefficients in F
    try:
        if hasattr(p, "free_symbols") and p.free_symbols:
            x = sympy.Symbol('x') if sympy.Symbol('x') in p.free_symbols else list(p.free_symbols)[0]
        else:
            x = sympy.Symbol('x')
            
        poly_p = sympy.Poly(p, x)
        h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: U is NOT invariant under the polynomial operator p(T)
    try:
        coeffs = poly_p.all_coeffs()
        n = T.shape[0]
        p_T = sympy.zeros(n, n)
        deg = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            p_T += c * (T ** (deg - i))
            
        B = p_T * U
        
        try:
            X, _ = U.gauss_jordan_solve(B)
            
            # Check if X is in the field of V.
            # We approximate this by checking if X introduces complex numbers
            # when T and U are strictly real.
            T_is_real = all(e.is_real for e in T)
            U_is_real = all(e.is_real for e in U)
            
            if T_is_real and U_is_real:
                X_is_real = all(e.is_real for e in X)
                is_inv = X_is_real
            else:
                # Fallback: check for explicit imaginary unit
                T_has_I = any(e.has(sympy.I) for e in T)
                U_has_I = any(e.has(sympy.I) for e in U)
                if not T_has_I and not U_has_I:
                    X_has_I = any(e.has(sympy.I) for e in X)
                    is_inv = not X_has_I
                else:
                    is_inv = True
        except ValueError:
            # gauss_jordan_solve raises ValueError if there is no solution
            is_inv = False
            
        neg_q = not is_inv
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: U is a T-invariant subspace of V",
    "H_3: p(x) is a polynomial with coefficients in F",
    "¬Q: U is not invariant under the polynomial operator p(T)"
]

N_HYP = 3
NEG_Q_INDEX = 3