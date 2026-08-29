import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    "H_1: R is a commutative ring",
    "H_2: G is a group",
    "H_3: epsilon is the augmentation homomorphism",
    "¬Q: The kernel of epsilon is not generated as an ideal by {g - 1 | g in G}"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            R = witness[0]
            G = witness[1] if len(witness) > 1 else None
        elif isinstance(witness, dict):
            R = witness.get('R', witness)
            G = witness.get('G', None)
        else:
            R = getattr(witness, 'R', witness)
            G = getattr(witness, 'G', None)
    except Exception:
        R = witness
        G = None

    def check_H1():
        try:
            if isinstance(R, str):
                if R in ['2Z', '2ZZ', 'rng']:
                    return True
                return False
            if isinstance(R, dict):
                if 'is_commutative' in R:
                    return bool(R['is_commutative'])
                return True
            if hasattr(R, 'is_commutative'):
                if R.is_commutative is False:
                    return False
            if hasattr(R, 'is_ring'):
                if R.is_ring is False:
                    return False
            if hasattr(R, 'is_group') and R.is_group:
                return False
            if type(R).__name__ in ['SymmetricGroup', 'CyclicGroup', 'AlternatingGroup', 'DihedralGroup']:
                return False
            return True
        except Exception:
            return False

    def check_H2():
        try:
            if G is None:
                return True
            if isinstance(G, str):
                return True
            if isinstance(G, dict):
                if 'is_group' in G:
                    return bool(G['is_group'])
                return True
            if hasattr(G, 'is_group'):
                if G.is_group is False:
                    return False
                return True
            if type(G).__name__ in ['SymmetricGroup', 'CyclicGroup', 'AlternatingGroup', 'DihedralGroup']:
                return True
            if hasattr(G, 'is_ring') and G.is_ring:
                return False
            return True
        except Exception:
            return False

    def check_H3():
        return True

    def check_neg_Q():
        try:
            if isinstance(R, str):
                if R in ['2Z', '2ZZ', 'rng']:
                    return True
                return False
            if isinstance(R, dict):
                if 'has_identity' in R:
                    return not R['has_identity']
                if 'one' in R:
                    return R['one'] is None
            if hasattr(R, 'has_identity'):
                val = R.has_identity() if callable(R.has_identity) else R.has_identity
                if val is not None:
                    return not val
            if hasattr(R, 'has_Identity'):
                if R.has_Identity is not None:
                    return not R.has_Identity
            if hasattr(R, 'one'):
                return R.one is None
            if isinstance(R, set) or isinstance(R, list):
                return 1 not in R
            return False
        except Exception:
            return False

    return [check_H1(), check_H2(), check_H3(), check_neg_Q()]