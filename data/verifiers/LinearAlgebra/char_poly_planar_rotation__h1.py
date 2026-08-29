import sympy as sp
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The dropped hypothesis from the true theorem is that x is a scalar.
    If x is a matrix, the constant term 1 in the conclusion causes a type mismatch
    or evaluates incorrectly, making the conclusion mathematically false.
    """
    try:
        R = witness['R']
        p = witness['p']
        theta = witness['theta']
        x = witness['x']
    except Exception:
        return [False, False, False]
        
    # H1: R is the 2x2 real rotation matrix by angle theta
    try:
        expected_R = sp.Matrix([
            [sp.cos(theta), -sp.sin(theta)],
            [sp.sin(theta),  sp.cos(theta)]
        ])
        if hasattr(R, 'shape') and R.shape == (2, 2):
            h1 = sp.simplify(R - expected_R) == sp.zeros(2, 2)
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H2: p(x) is the characteristic polynomial of R
    try:
        lam = sp.Symbol('lam')
        poly = R.charpoly(lam)
        
        p_val = p.as_expr() if hasattr(p, 'as_expr') else p
        
        if hasattr(x, 'shape'):
            # If x is a matrix, evaluate the characteristic polynomial as a matrix polynomial
            coeffs = poly.all_coeffs()
            expected_p = coeffs[0]*x**2 + coeffs[1]*x + coeffs[2]*sp.eye(x.shape[0])
            h2 = sp.simplify(p_val - expected_p) == sp.zeros(*x.shape)
        else:
            # If x is a scalar, evaluate normally
            expected_p = poly.as_expr().subs(lam, x)
            h2 = sp.simplify(p_val - expected_p) == 0
    except Exception:
        h2 = False
        
    # Conclusion: p(x) = x^2 - 2*cos(theta)*x + 1
    try:
        rhs = x**2 - 2*sp.cos(theta)*x + 1
        p_val = p.as_expr() if hasattr(p, 'as_expr') else p
        
        if hasattr(x, 'shape'):
            neg_q = sp.simplify(p_val - rhs) != sp.zeros(*x.shape)
        else:
            neg_q = sp.simplify(p_val - rhs) != 0
    except Exception:
        # If rhs raises an exception (e.g., adding scalar 1 to a matrix x), the conclusion fails.
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is the 2x2 real rotation matrix by angle theta",
    "H_2: p(x) is the characteristic polynomial of R",
    "¬Q: p(x) != x^2 - 2*cos(theta)*x + 1"
]

N_HYP = 2
NEG_Q_INDEX = 2