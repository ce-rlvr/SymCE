import sympy
from sympy.polys.domains import Domain, FractionField, PolynomialRing
from sympy.abc import x, y, z

# Top-level setup
QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness):
    try:
        k, R, I = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: k is a field
    try:
        h1 = isinstance(k, Domain) and k.is_Field
    except Exception:
        h1 = False
        
    # H2: R is a commutative k-algebra
    try:
        # In SymPy, Domain objects represent commutative rings.
        # We check if k is a subring of R by verifying that unifying R and k yields R.
        h2 = isinstance(R, Domain) and R.unify(k) == R
    except Exception:
        h2 = False
        
    # H3: I is an ideal of R
    try:
        # We represent the ideal I as a list or tuple of its generators in R.
        h3 = isinstance(I, (list, tuple))
        if h3:
            for elem in I:
                try:
                    # Verify that the element can be coerced into R
                    R(elem)
                except Exception:
                    h3 = False
                    break
    except Exception:
        h3 = False
        
    # neg_Q: R/I is NOT finitely generated as a k-algebra
    try:
        neg_q = False
        # A standard counterexample is R = k(x1, ..., xn) (a fraction field) and I = (0).
        # A fraction field over k is not finitely generated as a k-algebra unless it has 0 generators.
        if isinstance(R, FractionField) and R.domain == k:
            is_zero_ideal = all(R(elem) == R.zero for elem in I)
            if is_zero_ideal:
                neg_q = len(R.gens) > 0
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: R is a commutative k-algebra",
    "H_3: I is an ideal of R",
    "¬Q: R/I is not finitely generated as a k-algebra"
]

N_HYP = 3
NEG_Q_INDEX = 3