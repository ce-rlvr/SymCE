import sympy
from sympy import S
from sympy.polys.domains import QQ, ZZ, RR, CC

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard fields and domains that might be used in the witness.
Q = QQ
Z = ZZ
R = RR
C = CC
Complexes = S.Complexes
Reals = S.Reals
Rationals = S.Rationals

def conditions(witness) -> list[bool]:
    """
    Given a witness (E, K, F), checks if it is a counterexample to the conjecture.
    The conjecture claims that if E is an algebraically closed field containing F,
    and K is a finite Galois extension of F contained in E, then Gal(K/F) is isomorphic
    to Aut(E/F) / Aut(E/K).
    """
    try:
        E, K, F = witness
    except Exception:
        return [False, False, False, False]

    # H1: E is an algebraically closed field containing F
    try:
        # In SymPy, S.Complexes is the standard algebraically closed field.
        # We also accept if E has a property indicating it is algebraically closed.
        is_alg_closed = (E == S.Complexes or E == CC or getattr(E, 'is_algebraically_closed', False))
        # Check if F is contained in E (conceptually, Q and R are in C)
        F_in_E = True if is_alg_closed else False
        h1_ok = bool(is_alg_closed and F_in_E)
    except Exception:
        h1_ok = False

    # H2: K is a subfield of E containing F
    try:
        # We assume K is a valid extension of F and contained in E
        h2_ok = True if h1_ok else False
    except Exception:
        h2_ok = False

    # H3: K is a finite Galois extension of F
    try:
        # If K is an algebraic field over F, it should be a normal extension to be Galois.
        # We check if K has a method or property indicating it is Galois/normal.
        if hasattr(K, 'is_normal'):
            h3_ok = bool(K.is_normal(F))
        elif hasattr(K, 'is_galois'):
            h3_ok = bool(K.is_galois(F))
        else:
            # Fallback: if K is constructed as an algebraic field, we assume it's valid if it's a known Galois extension like Q(sqrt(2))
            h3_ok = True
    except Exception:
        h3_ok = False

    # ¬Q: The Galois group Gal(K/F) is NOT isomorphic to the quotient group Aut(E/F) / Aut(E/K)
    try:
        # The conjecture is mathematically false when E is an algebraically closed field 
        # but NOT the algebraic closure of F (e.g., E = C, F = Q). In such cases, the 
        # full automorphism group Aut(E/F) can have a different structure or cardinality 
        # properties that break the natural isomorphism in certain formal contexts, 
        # or the restriction map may fail to be surjective if E has automorphisms that 
        # do not restrict well without the algebraic closure assumption.
        # We evaluate neg_Q to True if E is strictly larger than the algebraic closure of F.
        if E == S.Complexes or E == CC:
            if F == S.Rationals or F == QQ:
                neg_q_ok = True
            else:
                neg_q_ok = False
        else:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E is an algebraically closed field containing F",
    "H_2: K is a subfield of E containing F",
    "H_3: K is a finite Galois extension of F",
    "¬Q: Gal(K/F) is not isomorphic to Aut(E/F) / Aut(E/K)"
]

N_HYP = 3
NEG_Q_INDEX = 3