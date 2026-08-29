import sympy
from sympy import Matrix, Poly, eye, zeros
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness can be just the matrix A, or a tuple (A, m(x))
        if isinstance(witness, tuple) and len(witness) == 2:
            A, m = witness
        else:
            A = witness
            m = None
            
        if isinstance(A, list):
            A = Matrix(A)
            
        # H_1: m(x) is the minimal polynomial of A
        try:
            m_expected = A.minimal_polynomial(x)
            if m is None:
                m = m_expected
            h1 = bool((m - m_expected).simplify() == 0)
        except Exception:
            h1 = False
            
        # ¬Q: A is invertible if and only if the constant term of m(x) is not equal to zero (fails)
        try:
            if m is None:
                neg_q = False
            else:
                if not getattr(A, 'is_square', False):
                    is_inv = False
                else:
                    # Determine if the matrix is over the integers Z
                    is_int_matrix = True
                    for val in A:
                        if isinstance(val, int):
                            continue
                        if hasattr(val, 'is_Float') and val.is_Float:
                            is_int_matrix = False
                            break
                        if hasattr(val, 'is_integer') and val.is_integer is True:
                            continue
                        is_int_matrix = False
                        break
                        
                    # A matrix over Z is invertible iff its determinant is 1 or -1
                    # A matrix over a field is invertible iff its determinant is non-zero
                    if is_int_matrix:
                        is_inv = abs(A.det()) == 1
                    else:
                        is_inv = A.det() != 0
                        
                # Extract the constant term of m(x)
                m_poly = Poly(m, x)
                const_term = m_poly.nth(0)
                const_not_zero = (const_term != 0)
                
                # The conclusion Q is that invertibility is equivalent to a non-zero constant term
                q = (bool(is_inv) == bool(const_not_zero))
                neg_q = not q
        except Exception:
            neg_q = False
            
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: m(x) is the minimal polynomial of A",
    "¬Q: A is invertible if and only if the constant term of m(x) is not equal to zero (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1