import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Poly
from sympy.abc import x, y, z, t

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: L is a finite Galois extension of K",
    "H_2: E is a purely inseparable extension of K",
    "¬Q: The restriction map is not a group isomorphism from Gal(LE/E) onto Gal(L/K)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness, checks the hypotheses and the negated conclusion.
    The theorem is unconditionally true (L/K Galois and E/K purely inseparable 
    implies L \\cap E = K, so the restriction map is always an isomorphism).
    Thus, no valid counterexample exists.
    """
    # 1. Try to interpret witness as a tuple of two polynomials (poly_L, poly_E) over Q
    if isinstance(witness, tuple) and len(witness) == 2:
        try:
            poly_L_expr, poly_E_expr = witness
            poly_L = Poly(poly_L_expr)
            poly_E = Poly(poly_E_expr)
            
            # H1: L is a finite Galois extension of K
            try:
                from sympy.polys.galois import galois_group
                G_L = galois_group(poly_L)[0]
                h1 = (G_L.order() == poly_L.degree()) and poly_L.is_irreducible
            except Exception:
                h1 = False
                
            # H2: E is a purely inseparable extension of K
            # Over Q (characteristic 0), purely inseparable implies degree 1
            try:
                h2 = (poly_E.degree() == 1) and poly_E.is_irreducible
            except Exception:
                h2 = False
                
            # ¬Q: The restriction map is not an isomorphism
            # Since E is degree 1 over Q, E = Q, so LE = L.
            # Gal(LE/E) = Gal(L/Q), and the restriction map is the identity (an isomorphism).
            neg_q = False
            
            return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            pass

    # 2. Fallback for abstract dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get("H_1", witness.get("H1", False)))
            h2 = bool(witness.get("H_2", witness.get("H2", False)))
            neg_q = bool(witness.get("neg_Q", witness.get("neg_q", False)))
            return [h1, h2, neg_q]
        except Exception:
            pass

    return [False, False, False]