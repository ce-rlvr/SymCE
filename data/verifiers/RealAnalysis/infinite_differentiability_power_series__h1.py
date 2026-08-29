import sympy
from sympy import Symbol, limit, oo, Abs, Interval, S
from sympy.calculus.util import continuous_domain
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary containing:
      'a_n': sympy expression for the n-th coefficient of the power series
      'n': sympy Symbol for the index
      'c': center of the power series
      'R': radius of convergence
      'f': sympy expression for the function f(x)
      'x': sympy Symbol for the variable
    """
    try:
        a_n = witness.get('a_n')
        n = witness.get('n')
        c = witness.get('c')
        R = witness.get('R')
        f = witness.get('f')
        x = witness.get('x')
    except Exception:
        return [False, False]
        
    # H_1: R > 0 is the radius of convergence of the power series
    h1_ok = False
    try:
        if R is not None and R > 0:
            if a_n is not None and n is not None:
                # Try ratio test
                ratio = Abs(a_n / a_n.subs(n, n+1))
                L_ratio = limit(ratio, n, oo)
                if L_ratio == R:
                    h1_ok = True
                else:
                    # Try root test
                    root = Abs(a_n)**(1/n)
                    L_root = limit(root, n, oo)
                    if L_root == 0 and R == oo:
                        h1_ok = True
                    elif L_root != 0 and L_root != oo and sympy.simplify(1/L_root - R) == 0:
                        h1_ok = True
    except Exception:
        pass

    # ¬Q: f(x) is NOT infinitely differentiable on (c-R, c+R)
    neg_q_ok = False
    try:
        if R == oo:
            domain = S.Reals
        else:
            domain = Interval.open(c - R, c + R)
            
        is_inf_diff = True
        deriv = f
        # Check up to the 4th derivative for continuity on the domain
        for _ in range(4):
            deriv = deriv.diff(x)
            cont_dom = continuous_domain(deriv, x, domain)
            if cont_dom != domain:
                is_inf_diff = False
                break
        neg_q_ok = not is_inf_diff
    except Exception:
        pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R > 0 is the radius of convergence of the power series",
    "¬Q: f(x) is not infinitely differentiable on (c-R, c+R)"
]

N_HYP = 1
NEG_Q_INDEX = 1