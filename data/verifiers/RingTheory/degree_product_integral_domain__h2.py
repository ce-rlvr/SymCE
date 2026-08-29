import sympy as sp
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness elements
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is an integral domain, then deg(f(x)g(x)) = deg(f(x)) + deg(g(x))."
    (The dropped hypothesis is that f(x) and g(x) are non-zero polynomials).
    """
    try:
        f, g = witness
    except Exception:
        return [False, False]
    
    # H_1: R is an integral domain
    # We verify that f and g are valid polynomials over an integral domain.
    # Standard SymPy expressions are over C (or subrings like ZZ, QQ), which are integral domains.
    # If explicit Poly objects with finite ring domains are provided, we ensure the modulus is prime.
    try:
        h1_ok = True
        for p in (f, g):
            if isinstance(p, sp.Poly):
                dom = p.domain
                if hasattr(dom, 'is_Field') and not dom.is_Field:
                    if hasattr(dom, 'mod'):
                        if not sp.isprime(dom.mod):
                            h1_ok = False
            else:
                # Try to convert to Poly to ensure it's a valid polynomial expression in x
                sp.Poly(p, x)
    except Exception:
        h1_ok = False

    # neg_Q: deg(f(x)g(x)) != deg(f(x)) + deg(g(x))
    # The conclusion fails if the degree of the product does not equal the sum of the degrees.
    # Mathematically, the degree of the zero polynomial is undefined (or -oo, which breaks standard addition).
    # We raise an exception for the zero polynomial to correctly evaluate the equation as failing.
    try:
        def deg(p):
            if isinstance(p, sp.Poly):
                if p.is_zero:
                    raise ValueError("Degree of zero polynomial is undefined")
                return p.degree()
            else:
                p_expr = sp.expand(sp.sympify(p))
                if p_expr.is_zero:
                    raise ValueError("Degree of zero polynomial is undefined")
                return sp.degree(p_expr, x)
        
        q_ok = (deg(f * g) == deg(f) + deg(g))
    except Exception:
        # If deg(0) is encountered, it raises ValueError, meaning the equation deg(fg) = deg(f) + deg(g) is invalid.
        q_ok = False
        
    neg_q = not q_ok
    
    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: deg(f(x)g(x)) != deg(f(x)) + deg(g(x))"
]

N_HYP = 1
NEG_Q_INDEX = 1