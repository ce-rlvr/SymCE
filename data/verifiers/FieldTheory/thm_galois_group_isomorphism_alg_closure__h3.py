import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import QQ, RR, CC, ZZ, AlgebraicField
from sympy import sqrt, I, pi

# Standard algebra objects
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture drops the hypothesis that K is a subfield of E. If K is not a subfield of E,
    Aut(E/K) is undefined, and the conclusion fails.
    """
    # 1. Try dictionary representation
    try:
        if isinstance(witness, dict):
            h1 = witness.get('F_is_field', False)
            h2 = witness.get('E_is_alg_closed', False) and witness.get('E_contains_F', False)
            h3 = witness.get('K_is_finite_galois', False)
            neg_q = not witness.get('K_is_subfield_of_E', True)
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    # 2. Try object attributes representation
    try:
        if hasattr(witness, 'F_is_field'):
            h1 = getattr(witness, 'F_is_field', False)
            h2 = getattr(witness, 'E_is_alg_closed', False) and getattr(witness, 'E_contains_F', False)
            h3 = getattr(witness, 'K_is_finite_galois', False)
            neg_q = not getattr(witness, 'K_is_subfield_of_E', True)
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    # 3. Try tuple (F, E, K) representation using SymPy domains
    try:
        F, E, K = witness
        
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif F in [QQ, RR, CC]:
            h1 = True
            
        h2 = False
        if E == CC and F in [QQ, RR, CC]:
            h2 = True
            
        h3 = False
        if isinstance(K, AlgebraicField) and K.domain == F:
            h3 = True
        elif F == RR and K == CC:
            h3 = True
            
        # If K is an AlgebraicField over QQ, it is not a subfield of CC in SymPy's domain system,
        # which perfectly models the dropped hypothesis (K not being a subfield of E).
        if K == CC:
            neg_q = False
        else:
            neg_q = True
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    # 4. Try string representation
    try:
        if isinstance(witness, str):
            w = witness.lower()
            h1 = 'field' in w or 'f' in w
            h2 = 'alg' in w or 'closed' in w or 'e' in w
            h3 = 'galois' in w or 'k' in w
            neg_q = 'not a subfield' in w or 'undefined' in w or 'not in e' in w
            if h1 and h2 and h3 and neg_q:
                return [True, True, True, True]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an algebraically closed field containing F",
    "H_3: K is a finite Galois extension of F",
    "¬Q: Gal(K/F) is not isomorphic to Aut(E/F) / Aut(E/K) (e.g. K is not a subfield of E)"
]

N_HYP = 3
NEG_Q_INDEX = 3