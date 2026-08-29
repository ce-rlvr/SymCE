import sympy
from sympy import Matrix, eye, zeros, Symbol, rem, simplify
from sympy.matrices.matrixbase import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is a square matrix
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: A has complex entries
    try:
        if h1:
            h2 = all(e.is_complex for e in witness)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: A complex number \lambda is a root of c_A(x) iff it is a root of m_A(x)
    # Negation: There is a root of c_A(x) that is not a root of m_A(x), or vice versa.
    try:
        if not h1:
            neg_q = False
        else:
            x = Symbol('x')
            n = witness.rows
            
            if n == 0:
                neg_q = False
            else:
                c_A = witness.charpoly(x).as_expr()
                
                # Compute minimal polynomial m_A(x)
                vecs = []
                A_k = eye(n)
                m_A = None
                for d in range(n + 1):
                    # Flatten the matrix into a vector
                    vec = [A_k[i, j] for i in range(n) for j in range(n)]
                    vecs.append(vec)
                    
                    # Check for linear dependence
                    M = Matrix(vecs).T
                    nullspace = M.nullspace()
                    if nullspace:
                        coeffs = nullspace[0]
                        lead = coeffs[-1]
                        m_A = sum(simplify(coeffs[i] / lead) * x**i for i in range(d + 1))
                        break
                    
                    A_k = A_k * witness
                
                if m_A is None:
                    neg_q = False
                else:
                    # c_A and m_A have the exact same roots iff c_A divides m_A^n and m_A divides c_A
                    rem1 = rem(m_A**n, c_A, x)
                    rem2 = rem(c_A, m_A, x)
                    
                    def is_zero_poly(p):
                        p = simplify(p)
                        if p == 0:
                            return True
                        try:
                            poly_obj = p.as_poly(x)
                            if poly_obj is None:
                                return False
                            coeffs = poly_obj.all_coeffs()
                            for c in coeffs:
                                if abs(complex(c)) > 1e-9:
                                    return False
                            return True
                        except Exception:
                            return False
                            
                    same_roots = is_zero_poly(rem1) and is_zero_poly(rem2)
                    neg_q = not same_roots
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: A has complex entries",
    "¬Q: There is a root of c_A(x) that is not a root of m_A(x), or vice versa"
]

N_HYP = 2
NEG_Q_INDEX = 2