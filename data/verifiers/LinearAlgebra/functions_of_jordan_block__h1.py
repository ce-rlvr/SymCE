import sympy
import math

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        # The witness should provide the matrix J, the function f (as a sympy expression),
        # the scalar lambda, and the variable z used in f.
        J, f, lam, z = witness
    except Exception:
        return [False, False]
    
    # H_1: f(z) is a function that is analytic in a neighborhood of lambda
    try:
        v1 = f.subs(z, lam)
        v2 = sympy.diff(f, z).subs(z, lam)
        # If the function and its first derivative evaluate to finite values at lambda,
        # it is analytic in a neighborhood of lambda (for standard expressions).
        h1 = (v1.is_finite == True) and (v2.is_finite == True)
    except Exception:
        h1 = False
        
    # neg_Q: f(J) is NOT the specified upper triangular matrix
    try:
        if not isinstance(J, sympy.Matrix):
            return [False, False]
        if J.shape[0] != J.shape[1]:
            return [False, False]
            
        n = J.shape[0]
        
        # Evaluate f(J)
        try:
            poly = sympy.Poly(f, z)
            coeffs = poly.all_coeffs()
            f_J = sympy.zeros(n, n)
            for i, c in enumerate(coeffs):
                power = len(coeffs) - 1 - i
                f_J += c * (J ** power)
        except Exception:
            # Fallback for exponential function if polynomial evaluation fails
            if f == sympy.exp(z):
                f_J = J.exp()
            else:
                f_J = None
                
        if f_J is None:
            neg_q = False
        else:
            # Construct the expected upper triangular matrix M
            M = sympy.zeros(n, n)
            for i in range(n):
                for j in range(i, n):
                    k = j - i
                    deriv = sympy.diff(f, z, k).subs(z, lam)
                    M[i, j] = deriv / math.factorial(k)
            
            # The conclusion fails if f(J) is not exactly the matrix M
            neg_q = (f_J != M)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f(z) is a function that is analytic in a neighborhood of lambda",
    "¬Q: f(J) is not the specified upper triangular matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1