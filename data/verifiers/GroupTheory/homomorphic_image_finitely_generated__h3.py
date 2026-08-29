import sympy
from sympy import S
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(obj):
    if getattr(obj, 'is_group', False):
        return True
    # Standard infinite groups under addition
    if obj in (S.Rationals, S.Reals, S.Complexes, S.Integers):
        return True
    from sympy.combinatorics import Group
    if isinstance(obj, Group):
        return True
    return False

def is_finitely_generated(obj):
    if hasattr(obj, 'is_finitely_generated'):
        return bool(obj.is_finitely_generated)
    # Rationals, Reals, Complexes are not finitely generated under addition
    if obj in (S.Rationals, S.Reals, S.Complexes):
        return False
    if obj == S.Integers:
        return True
    from sympy.combinatorics import Group
    if isinstance(obj, Group):
        return True
    # Default to True so that neg_Q is False unless we are sure it's infinitely generated
    return True

def is_surjective_homomorphism(f, G, H):
    # Check mock objects
    if getattr(f, 'is_surjective', False) and getattr(f, 'is_homomorphism', False):
        if getattr(f, 'domain', None) == G and getattr(f, 'codomain', None) == H:
            return True
            
    # Check standard infinite groups with identity homomorphism
    if G == H and G in (S.Rationals, S.Reals, S.Complexes, S.Integers):
        try:
            if f(S.Half) == S.Half and f(S(1)) == S(1) and f(S(0)) == S(0):
                return True
        except Exception:
            pass
        try:
            if f(1) == 1 and f(0) == 0 and f(-1) == -1:
                return True
        except Exception:
            pass
            
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
            f = witness.get('f')
        elif hasattr(witness, 'G') and hasattr(witness, 'H') and hasattr(witness, 'f'):
            G = witness.G
            H = witness.H
            f = witness.f
        else:
            G, H, f = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(is_group(G) and is_group(H))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(is_surjective_homomorphism(f, G, H))
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not is_finitely_generated(H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: f is a surjective group homomorphism from G to H",
    "¬Q: H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2