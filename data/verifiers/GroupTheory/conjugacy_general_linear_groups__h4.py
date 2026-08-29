import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def is_over_F(M, F):
    """Check if all elements of matrix M belong to the field F."""
    for val in M:
        in_F = False
        # Try conversion using SymPy domain method
        if hasattr(F, 'from_sympy'):
            try:
                F.from_sympy(val)
                in_F = True
            except Exception:
                pass
        # Try using Python's 'in' operator for SymPy Sets
        if not in_F and hasattr(F, '__contains__'):
            try:
                if val in F:
                    in_F = True
            except Exception:
                pass
        # Fallbacks for common SymPy fields
        if not in_F:
            if F == sympy.QQ or F == sympy.S.Rationals:
                if hasattr(val, 'is_Rational') and val.is_Rational:
                    in_F = True
            elif F == sympy.RR or F == sympy.S.Reals:
                if hasattr(val, 'is_real') and val.is_real:
                    in_F = True
            elif F == sympy.CC or F == sympy.S.Complexes:
                if hasattr(val, 'is_complex') and val.is_complex:
                    in_F = True
        if not in_F:
            return False
    return True

def are_similar(A, B):
    """
    Check if matrices A and B are similar over the field containing their entries.
    Two matrices have the same rational canonical form iff they are similar.
    """
    if A.shape != B.shape or A.shape[0] != A.shape[1]:
        return False
    n = A.shape[0]
    
    # Quick necessary conditions
    if sympy.expand(A.trace() - B.trace()) != 0:
        return False
    if sympy.expand(A.det() - B.det()) != 0:
        return False
        
    # Set up the linear system P * A = B * P
    P_syms = sympy.symbols(f'p0:{n*n}')
    P = sympy.Matrix(n, n, P_syms)
    eqs = (P * A - B * P).vec()
    
    # Solve for the entries of P
    sol = sympy.solve(eqs, P_syms, dict=True)
    if not sol:
        return False
        
    # Substitute the parameterized solution back into P
    P_sol = P.subs(sol[0])
    
    # If the determinant of the parameterized matrix P is identically zero,
    # no invertible matrix P exists, meaning they are not similar.
    detP = sympy.expand(P_sol.det())
    if detP == 0:
        return False
        
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            n = witness.get('n')
            A = witness.get('A')
            B = witness.get('B')
        else:
            F, n, A, B = witness
    except Exception:
        return [False, False, False, False]

    # Ensure A and B are SymPy matrices
    try:
        if not isinstance(A, sympy.MatrixBase):
            A = sympy.Matrix(A)
    except Exception:
        pass

    try:
        if not isinstance(B, sympy.MatrixBase):
            B = sympy.Matrix(B)
    except Exception:
        pass

    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
        if not h1:
            if F in (sympy.QQ, sympy.S.Rationals, sympy.RR, sympy.S.Reals, sympy.CC, sympy.S.Complexes):
                h1 = True
            elif hasattr(F, 'is_field'):
                h1 = F.is_field
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    # H_3: A is a matrix in the general linear group GL_n(F)
    try:
        h3 = False
        if isinstance(A, sympy.MatrixBase) and A.shape == (n, n):
            if sympy.expand(A.det()) != 0:
                if is_over_F(A, F):
                    h3 = True
    except Exception:
        h3 = False

    # ¬Q: The biconditional "A and B are conjugate in GL_n(F) iff they have the same RCF" fails.
    try:
        neg_q = False
        if isinstance(B, sympy.MatrixBase) and B.shape == (n, n):
            same_rcf = are_similar(A, B)
            b_over_f = is_over_F(B, F)
            
            # A and B are conjugate in GL_n(F) iff B is a matrix over F and they are similar over F.
            # Since A is over F, if B is over F and they are similar, they are similar over F.
            conjugate_in_F = b_over_f and same_rcf
            
            # The conclusion fails if the truth values of the two statements differ
            neg_q = (conjugate_in_F != same_rcf)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n is a positive integer",
    "H_3: A is a matrix in GL_n(F)",
    "¬Q: The biconditional between conjugacy in GL_n(F) and having the same rational canonical form fails"
]

N_HYP = 3
NEG_Q_INDEX = 3