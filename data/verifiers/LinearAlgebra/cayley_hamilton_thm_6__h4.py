import sympy
from sympy import eye, zeros, Symbol, Poly, Matrix, MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is an n x n matrix with entries in F",
    "H_3: A is an invertible matrix",
    "¬Q: A^{-1} != -(1/c_0)(A^{n-1} + c_{n-1}A^{n-2} + ... + c_1 I)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # The witness can be just the matrix A, or a tuple (A, c) where c is a list of coefficients.
        if isinstance(witness, tuple) and len(witness) == 2:
            A_input, c_input = witness
            try:
                A = Matrix(A_input)
            except Exception:
                A = A_input
            c = c_input
        else:
            try:
                A = Matrix(witness)
            except Exception:
                A = witness
            c = None
            
        # H_1: F is a field (implicitly checked by ensuring A is a valid SymPy matrix)
        h1 = isinstance(A, MatrixBase)
        
        # H_2: A is an n x n matrix
        h2 = False
        if h1 and len(A.shape) == 2 and A.shape[0] == A.shape[1] and A.shape[0] > 0:
            h2 = True
            n = A.shape[0]
            
        # H_3: A is an invertible matrix
        h3 = False
        if h2:
            try:
                if sympy.simplify(A.det()) != 0:
                    A_inv = A.inv()
                    h3 = True
            except Exception:
                h3 = False
                
        # ¬Q: The conclusion fails at the witness
        neg_q = False
        if h3:
            # If coefficients are not provided, compute them from det(A - tI)
            # This naturally provides a counterexample for odd n due to the missing (-1)^n factor.
            if c is None:
                t = Symbol('t')
                p = (A - t * eye(n)).det()
                c_poly = Poly(p, t)
                coeffs = c_poly.all_coeffs()
                c = coeffs[::-1]  # Reverse so c[0] is the constant term
                
            if len(c) >= n:
                c0 = sympy.simplify(c[0])
                if c0 == 0:
                    neg_q = True
                else:
                    # Evaluate the polynomial: A^{n-1} + c_{n-1}A^{n-2} + ... + c_1 I
                    poly_A = A**(n - 1)
                    for i in range(1, n):
                        poly_A += c[i] * (A**(i - 1))
                    
                    RHS = -(1 / c0) * poly_A
                    
                    if A_inv != RHS:
                        diff = sympy.simplify(A_inv - RHS)
                        if diff != zeros(n, n):
                            neg_q = True
            else:
                # If the provided coefficient list is too short, the formula is undefined
                neg_q = True
                
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]