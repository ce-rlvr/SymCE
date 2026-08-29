import sympy as sp
from sympy.matrices import Matrix, eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_F_type_from_A(A):
    """
    Infers the commutative ring F over which the matrix A is defined.
    Returns 'Z' for integers, 'Q' for rationals/floats, 'Poly' for polynomials, or 'Unknown'.
    """
    elements = list(A)
    if not elements:
        return 'Z'
    
    if any(getattr(e, 'has', lambda x: False)(sp.Symbol) for e in elements):
        return 'Poly'
        
    if all(getattr(e, 'is_Integer', False) for e in elements):
        return 'Z'
        
    if all(getattr(e, 'is_Rational', False) or getattr(e, 'is_Float', False) for e in elements):
        return 'Q'
        
    return 'Unknown'

def check_H1(A):
    """
    Hypothesis 1: Let A be an n \times n matrix over F.
    """
    try:
        return isinstance(A, sp.MatrixBase) and A.is_square
    except Exception:
        return False

def check_H2(A):
    """
    Hypothesis 2: The matrix A has n distinct eigenvalues in F.
    """
    try:
        if not (isinstance(A, sp.MatrixBase) and A.is_square):
            return False
        n = A.shape[0]
        evals = A.eigenvals()
        
        # Check for exactly n distinct eigenvalues
        if len(evals) != n:
            return False
            
        F_type = get_F_type_from_A(A)
        if F_type == 'Unknown':
            return False
            
        # Check if all eigenvalues belong to the ring F
        for e in evals.keys():
            if F_type == 'Z':
                if not getattr(e, 'is_Integer', False):
                    return False
            elif F_type == 'Q':
                if not (getattr(e, 'is_Rational', False) or getattr(e, 'is_Float', False)):
                    return False
            elif F_type == 'Poly':
                symbols = e.free_symbols
                if symbols:
                    if not e.is_polynomial(*symbols):
                        return False
                else:
                    if not (getattr(e, 'is_Rational', False) or getattr(e, 'is_Float', False) or getattr(e, 'is_Integer', False)):
                        return False
        return True
    except Exception:
        return False

def check_neg_Q(A):
    """
    Negated Conclusion: The matrix A is NOT diagonalizable over F.
    (i.e., there does not exist an invertible matrix P over F such that P^{-1}AP is diagonal).
    """
    try:
        if not (isinstance(A, sp.MatrixBase) and A.is_square):
            return False
        F_type = get_F_type_from_A(A)
        if F_type == 'Unknown':
            return False
            
        n = A.shape[0]
        
        P_cols = []
        for evalue, mult, evecs in A.eigenvects():
            for vec in evecs:
                elements = list(vec)
                
                # Clear denominators to find a vector in F^n
                lcm_val = 1
                for e in elements:
                    if getattr(e, 'is_Rational', False):
                        lcm_val = sp.lcm(lcm_val, e.q)
                    elif hasattr(e, 'as_numer_denom'):
                        num, den = e.as_numer_denom()
                        if getattr(den, 'is_Integer', False):
                            lcm_val = sp.lcm(lcm_val, den)
                        elif getattr(den, 'has', lambda x: False)(sp.Symbol):
                            lcm_val = lcm_val * den
                
                vec = vec * lcm_val
                vec = vec.applyfunc(sp.cancel)
                
                # Divide by the greatest common divisor to make the vector primitive in F^n
                gcd_val = 0
                for e in vec:
                    if F_type == 'Z':
                        gcd_val = sp.gcd(gcd_val, e)
                    elif F_type == 'Poly':
                        gcd_val = sp.gcd(gcd_val, e)
                        
                if gcd_val != 0 and gcd_val != 1 and gcd_val != -1:
                    vec = vec / gcd_val
                    vec = vec.applyfunc(sp.cancel)
                    
                P_cols.append(vec)
                
        # If we couldn't find n eigenvectors, it's definitely not diagonalizable
        if len(P_cols) != n:
            return True
            
        P = sp.Matrix.hstack(*P_cols)
        det_P = sp.cancel(P.det())
        
        # Check if the determinant of the eigenvector matrix is a unit in F
        if F_type == 'Z':
            is_unit = getattr(det_P, 'is_Integer', False) and abs(det_P) == 1
        elif F_type == 'Poly':
            is_unit = not getattr(det_P, 'has', lambda x: False)(sp.Symbol) and det_P != 0
        else:
            is_unit = det_P != 0
            
        return not is_unit
    except Exception:
        return False

def conditions(witness):
    return [check_H1(witness), check_H2(witness), check_neg_Q(witness)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over F",
    "H_2: A has n distinct eigenvalues in F",
    "¬Q: A is not diagonalizable over F"
]

N_HYP = 2
NEG_Q_INDEX = 2