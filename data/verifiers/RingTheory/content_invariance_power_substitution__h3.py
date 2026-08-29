import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy import Poly
from sympy.abc import x

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample.
    The witness should be a tuple (f, k) where:
      - f is a sympy expression representing a polynomial in x
      - k is an integer exponent
    """
    try:
        f, k = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain
    try:
        p1 = Poly(f, x)
        h1 = bool(p1.domain.is_UFD)
    except Exception:
        h1 = False

    # H_2: f(x) is a non-zero polynomial
    try:
        p1 = Poly(f, x)
        h2 = not p1.is_zero
    except Exception:
        h2 = False

    # ¬Q: The content of f(x^k) is not associate to the content of f(x) in R
    try:
        p1 = Poly(f, x)
        domain = p1.domain
        
        # Substitute x with x**k
        f_sub = sympy.sympify(f).subs(x, x**k)
        p2 = Poly(f_sub, x, domain=domain)
        
        c1 = p1.content()
        c2 = p2.content()
        
        # Check if c1 and c2 are associate in the domain
        if c1 == c2:
            is_assoc = True
        elif c1 == domain.zero or c2 == domain.zero:
            is_assoc = False
        else:
            try:
                # In a UFD, elements are associate if they divide each other exactly
                domain.exquo(c1, c2)
                domain.exquo(c2, c1)
                is_assoc = True
            except Exception:
                is_assoc = False
                
        neg_q = not is_assoc
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f(x) is a non-zero polynomial",
    "¬Q: The content of f(x^k) is not associate to the content of f(x) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2