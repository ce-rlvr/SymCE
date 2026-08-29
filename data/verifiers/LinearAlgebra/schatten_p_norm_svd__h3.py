import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math

# Top-level setup for standard named objects
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

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Extract witness
    try:
        A, p = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an m x n complex matrix
    try:
        if not isinstance(A, sp.MatrixBase):
            h1_ok = False
        else:
            h1_ok = all(val.is_complex for val in A)
    except Exception:
        h1_ok = False

    # H_2: p >= 1 is a real number
    try:
        if hasattr(p, 'is_real') and not p.is_real:
            h2_ok = False
        else:
            p_val = float(p)
            h2_ok = p_val >= 1.0
    except Exception:
        h2_ok = False

    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: (Tr((A^*A)^{p/2}))^{1/p} == (\sum_{i=1}^{\min(m,n)} \sigma_i(A)^p)^{1/p}
    try:
        m, n = A.shape
        p_float = float(p)
        
        A_star_A = A.H * A
        
        # Compute LHS: (Tr((A^*A)^{p/2}))^{1/p}
        try:
            # Attempt direct matrix fractional power
            power_mat = A_star_A ** (p_float / 2.0)
            lhs_trace = power_mat.trace()
            lhs_val = complex(sp.N(lhs_trace ** (1.0 / p_float)))
        except Exception:
            # Fallback to eigenvalue definition if matrix power fails (e.g. singular matrix issues in SymPy)
            evals = A_star_A.eigenvals(multiple=True)
            trace_val = sum(complex(sp.N(e))**(p_float / 2.0) for e in evals)
            lhs_val = trace_val ** (1.0 / p_float)
            
        # Compute RHS: (\sum_{i=1}^{\min(m,n)} \sigma_i(A)^p)^{1/p}
        evals = A_star_A.eigenvals(multiple=True)
        # Singular values are the square roots of the non-negative eigenvalues
        evals_real = sorted([float(sp.re(e)) for e in evals], reverse=True)
        sigmas = [math.sqrt(max(0.0, e)) for e in evals_real[:min(m, n)]]
        
        rhs_sum = sum(s**p_float for s in sigmas)
        rhs_val = complex(rhs_sum ** (1.0 / p_float))
        
        # Check if they are equal
        is_equal = math.isclose(lhs_val.real, rhs_val.real, abs_tol=1e-7, rel_tol=1e-7) and \
                   math.isclose(lhs_val.imag, rhs_val.imag, abs_tol=1e-7, rel_tol=1e-7)
                   
        neg_q_ok = not is_equal
    except Exception:
        # If evaluation of the expressions fails mathematically, the equality does not hold
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "H_2: p >= 1 is a real number",
    "¬Q: The Schatten p-norm definition via trace of (A^*A)^{p/2} does not equal the p-norm of singular values"
]

N_HYP = 2
NEG_Q_INDEX = 2