import sympy as sp
import z3
import math
import itertools
import functools

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    # H1: A is an n by n matrix
    def check_h1(A):
        try:
            if not isinstance(A, sp.MatrixBase):
                return False
            return A.is_square
        except Exception:
            return False

    # H2: Every entry of A is a non-negative real number
    def check_h2(A):
        try:
            for i in range(A.rows):
                for j in range(A.cols):
                    val = A[i, j]
                    cval = complex(val.evalf())
                    if abs(cval.imag) > 1e-9:
                        return False
                    if cval.real < -1e-9:
                        return False
            return True
        except Exception:
            return False

    # neg_Q: Conclusion fails
    def check_neg_Q(A):
        try:
            if not A.is_square:
                return False
                
            evs = A.eigenvals(multiple=True)
            if not evs:
                return True
                
            rho = 0.0
            for ev in evs:
                cval = complex(ev.evalf())
                mag = (cval.real**2 + cval.imag**2)**0.5
                if mag > rho:
                    rho = mag
                    
            if rho <= 1e-9:
                return True
                
            rho_eigenvalue = None
            for ev in A.eigenvals().keys():
                cval = complex(ev.evalf())
                if abs(cval.imag) < 1e-9 and abs(cval.real - rho) < 1e-9:
                    rho_eigenvalue = ev
                    break
                    
            if rho_eigenvalue is None:
                return True
                
            vects = []
            for ev, mult, basis in A.eigenvects():
                cval = complex(ev.evalf())
                if abs(cval.imag) < 1e-9 and abs(cval.real - rho) < 1e-9:
                    vects.extend(basis)
                    
            if not vects:
                return True
                
            solver = z3.Solver()
            coeffs = [z3.Real(f'c_{i}') for i in range(len(vects))]
            
            n = A.shape[0]
            for i in range(n):
                row_expr = 0
                for j in range(len(vects)):
                    cval = complex(vects[j][i].evalf())
                    val = cval.real
                    if abs(val) < 1e-9:
                        val = 0.0
                    row_expr += coeffs[j] * val
                solver.add(row_expr >= 1.0)
                
            if solver.check() == z3.sat:
                return False
            else:
                return True
                
        except Exception:
            return False

    h1_ok = check_h1(witness)
    h2_ok = check_h2(witness)
    neg_q_ok = check_neg_Q(witness)
    
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an n by n matrix",
    "H_2: Every entry of A is a non-negative real number",
    "¬Q: The spectral radius is not a strictly positive eigenvalue, or no strictly positive eigenvector exists"
]

N_HYP = 2
NEG_Q_INDEX = 2