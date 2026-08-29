import sympy
from sympy import Poly, integer_nthroot
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

CONDITION_LABELS = [
    "H_1: L/K is a Galois extension",
    "H_2: The Galois group Gal(L/K) is an abelian group",
    "¬Q: The extension M/K is not a Galois extension"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_field(expr):
    """Check if the expression defines a valid field extension over Q (i.e. is irreducible)."""
    try:
        if isinstance(expr, Poly):
            p = expr
            if p.domain != sympy.QQ:
                p = p.set_domain('QQ')
        else:
            if not hasattr(expr, 'free_symbols'):
                return False
            free = expr.free_symbols
            if len(free) != 1:
                return False
            x_var = list(free)[0]
            p = Poly(expr, x_var, domain='QQ')
        return p.is_irreducible
    except Exception:
        return False

def is_galois(expr):
    """
    Check if the polynomial defines a Galois extension over Q.
    Returns True if definitely Galois, False if definitely not, None if unknown (degree > 3).
    """
    try:
        if isinstance(expr, Poly):
            p = expr
            if p.domain != sympy.QQ:
                p = p.set_domain('QQ')
        else:
            free = expr.free_symbols
            x_var = list(free)[0]
            p = Poly(expr, x_var, domain='QQ')
            
        n = p.degree()
        if n == 1:
            return True
        if n == 2:
            return True
        if n == 3:
            disc = p.discriminant()
            if disc.is_Rational:
                num, den = disc.as_numer_denom()
                if num < 0:
                    return False
                return integer_nthroot(int(num), 2)[1] and integer_nthroot(int(den), 2)[1]
            return False
        return None
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    L_expr = None
    M_expr = None
    K_expr = None

    # Parse witness
    if isinstance(witness, dict):
        L_expr = witness.get('L')
        M_expr = witness.get('M')
        K_expr = witness.get('K', x)
    elif isinstance(witness, tuple):
        if len(witness) == 2:
            L_expr, M_expr = witness
            K_expr = x
        elif len(witness) == 3:
            L_expr, K_expr, M_expr = witness
            
    if L_expr is None or M_expr is None:
        return [False, False, False]

    # Verify K is Q (represented by a degree 1 polynomial)
    if K_expr is not None:
        try:
            if not is_field(K_expr):
                return [False, False, False]
            if isinstance(K_expr, Poly):
                pK = K_expr
            else:
                free = K_expr.free_symbols
                var = list(free)[0]
                pK = Poly(K_expr, var, domain='QQ')
            if pK.degree() != 1:
                return [False, False, False]
        except Exception:
            return [False, False, False]

    # H_1: L/K is a Galois extension
    try:
        if not is_field(L_expr):
            h1 = False
        else:
            gal_L = is_galois(L_expr)
            h1 = (gal_L is True)
    except Exception:
        h1 = False

    # H_2: Gal(L/K) is an abelian group
    try:
        # For degree <= 3, any Galois extension is abelian (groups are trivial, Z2, or Z3)
        if h1:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: M/K is NOT a Galois extension
    try:
        if not is_field(M_expr):
            neg_q = False
        else:
            gal_M = is_galois(M_expr)
            # Must be DEFINITELY not Galois to falsify the conclusion
            neg_q = (gal_M is False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]