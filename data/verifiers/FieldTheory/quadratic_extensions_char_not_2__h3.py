import sympy
from sympy import Poly, RootOf, factor_list, degree, sympify
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The characteristic of F is not equal to 2",
    "¬Q: E is not a Galois extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    The witness is expected to be an irreducible polynomial P(x) over a field F,
    representing the field extension E = F[x]/(P(x)).
    """
    try:
        if isinstance(witness, str):
            witness = sympify(witness)
        if isinstance(witness, tuple):
            P = Poly(*witness)
        else:
            P = Poly(witness)
            
        if len(P.gens) != 1:
            return [False, False, False]
        gen = P.gens[0]
        
        # If the domain is not a field (e.g., ZZ), move to its fraction field (e.g., QQ)
        if not P.domain.is_Field:
            P = P.set_domain(P.domain.get_field())
    except Exception:
        return [False, False, False]

    # H1: F is a field (and E is a valid field extension, so P must be irreducible)
    try:
        h1 = P.domain.is_Field and P.is_irreducible
    except Exception:
        h1 = False

    # H2: The characteristic of F is not equal to 2
    try:
        h2 = (P.domain.characteristic != 2)
    except Exception:
        h2 = False

    # neg_Q: E is NOT a Galois extension of F
    try:
        if P.degree() <= 1:
            is_galois = True
        elif P.domain.is_FiniteField:
            # Any finite extension of a finite field is Galois
            is_galois = True
        else:
            try:
                # Quick check for extensions of QQ:
                # If a normal extension has a real root, it must be totally real.
                # Thus, if it has both real and non-real roots, it cannot be Galois.
                real_roots = P.real_roots()
                if 0 < len(real_roots) < P.degree():
                    is_galois = False
                else:
                    raise ValueError("Fallback to full factorization")
            except Exception:
                # General check: E is Galois iff P splits completely in E.
                # We adjoin one root of P and check if P factors into linear terms.
                expr = P.as_expr()
                r = RootOf(expr, 0)
                factors = factor_list(expr, extension=r)[1]
                is_galois = all(degree(f, gen) == 1 for f, mult in factors)
                
        neg_q = not is_galois
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]