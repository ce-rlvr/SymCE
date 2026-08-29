import sympy
from sympy import Expr, Poly, minpoly, sqrt
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_poly(witness):
    """Convert the witness into a SymPy Poly object over Q."""
    if isinstance(witness, Poly):
        return witness
    if isinstance(witness, Expr):
        free = witness.free_symbols
        if len(free) == 1:
            var = list(free)[0]
            return Poly(witness, var)
        elif len(free) == 0:
            return Poly(minpoly(witness, x), x)
    return Poly(witness, x)

def conditions(witness) -> list[bool]:
    # H_1: K is a field extension of Q
    try:
        poly = get_poly(witness)
        # The polynomial must be defined over Q (or Z) and be irreducible.
        h1_ok = bool((poly.domain.is_QQ or poly.domain.is_ZZ) and poly.is_irreducible)
    except Exception:
        h1_ok = False

    # ¬Q: K is NOT contained in any cyclotomic field
    try:
        poly = get_poly(witness)
        deg = poly.degree()
        
        # By the Kronecker-Weber theorem, a finite extension of Q is contained in a 
        # cyclotomic field if and only if it is an abelian extension of Q.
        if deg == 1 or deg == 2:
            # Degree 1 and 2 extensions are always abelian, hence contained in a cyclotomic field.
            neg_q_ok = False
        elif deg == 3:
            # A degree 3 irreducible polynomial generates an abelian extension (Galois group A3)
            # if and only if its discriminant is a perfect square in Q.
            # Otherwise, the Galois group is S3 (non-abelian), so it's NOT in a cyclotomic field.
            disc = poly.discriminant()
            neg_q_ok = not sqrt(disc).is_rational
        else:
            # For higher degrees, we conservatively return False to avoid false positives,
            # meaning the verifier will safely reject unverified higher-degree counterexamples.
            # A degree 3 polynomial like x**3 - 2 is a sufficient and standard counterexample.
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field extension of Q",
    "¬Q: K is not contained in any cyclotomic field"
]

N_HYP = 1
NEG_Q_INDEX = 1