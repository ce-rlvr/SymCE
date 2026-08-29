import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x, y, z

# Standard group theory bindings
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

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    Since the counterexample requires a non-commutative ring (as the theorem 
    is unconditionally true for commutative integral domains), and SymPy does 
    not natively support non-commutative fields of fractions, the witness is 
    expected to be a custom object, dictionary, or tuple exposing the properties.
    """
    h1 = False
    h2 = False
    neg_q = False

    try:
        if callable(witness):
            witness = witness()
    except Exception:
        pass

    # Handle dictionary-based witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('K_is_field_of_fractions', witness.get('h1', False)))
        except Exception:
            pass
        try:
            h2 = bool(witness.get('M_is_torsion_free', witness.get('h2', False)))
        except Exception:
            pass
        try:
            neg_q = not bool(witness.get('is_injective', witness.get('q', True)))
        except Exception:
            pass
        return [h1, h2, neg_q]

    # Handle tuple-based witness (R, K, M)
    if isinstance(witness, tuple) and len(witness) == 3:
        R, K, M = witness
        try:
            if hasattr(K, 'is_field_of_fractions_of'):
                h1 = bool(K.is_field_of_fractions_of(R))
            elif hasattr(R, 'field_of_fractions'):
                h1 = (K == R.field_of_fractions)
        except Exception:
            pass

        try:
            if hasattr(M, 'is_torsion_free_over'):
                h2 = bool(M.is_torsion_free_over(R))
            elif hasattr(M, 'is_torsion_free'):
                h2 = bool(M.is_torsion_free)
        except Exception:
            pass

        try:
            if hasattr(M, 'canonical_map_is_injective'):
                neg_q = not bool(M.canonical_map_is_injective(K))
            elif hasattr(M, 'is_injective'):
                neg_q = not bool(M.is_injective)
        except Exception:
            pass
            
        if h1 or h2 or neg_q:
            return [h1, h2, neg_q]

    # Handle custom object witness
    try:
        if hasattr(witness, 'K_is_field_of_fractions'):
            attr = witness.K_is_field_of_fractions
            h1 = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'h1'):
            attr = witness.h1
            h1 = bool(attr() if callable(attr) else attr)
    except Exception:
        pass

    try:
        if hasattr(witness, 'M_is_torsion_free'):
            attr = witness.M_is_torsion_free
            h2 = bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'h2'):
            attr = witness.h2
            h2 = bool(attr() if callable(attr) else attr)
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_injective'):
            attr = witness.is_injective
            neg_q = not bool(attr() if callable(attr) else attr)
        elif hasattr(witness, 'q'):
            attr = witness.q
            neg_q = not bool(attr() if callable(attr) else attr)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: M is a torsion-free R-module",
    "¬Q: The canonical R-module homomorphism from M to M \\otimes_R K is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2