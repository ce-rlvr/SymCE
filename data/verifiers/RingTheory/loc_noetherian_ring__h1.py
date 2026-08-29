import sympy
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
    "H_1: R is a Noetherian ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False

    # Dictionary-based witness with direct boolean flags
    if isinstance(witness, dict):
        try:
            if 'R_is_noetherian' in witness:
                h1 = bool(witness['R_is_noetherian'])
            if 'S_is_multiplicatively_closed' in witness:
                h2 = bool(witness['S_is_multiplicatively_closed'])
            if 'localized_is_noetherian' in witness:
                neg_q = not bool(witness['localized_is_noetherian'])
            
            # If it was a direct dict with these keys, we can return early
            if 'R_is_noetherian' in witness:
                return [h1, h2, neg_q]
        except Exception:
            pass

    R, S, S_inv_R = None, None, None

    # Try to unpack if it's a tuple/list
    if isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            R, S, S_inv_R = witness
        elif len(witness) == 2:
            R, S = witness
            try:
                S_inv_R = R.localize(S)
            except Exception:
                pass
    else:
        try:
            R = getattr(witness, 'R', witness.get('R') if isinstance(witness, dict) else None)
            S = getattr(witness, 'S', witness.get('S') if isinstance(witness, dict) else None)
            S_inv_R = getattr(witness, 'S_inv_R', witness.get('S_inv_R') if isinstance(witness, dict) else None)
            if S_inv_R is None and hasattr(witness, 'localized_ring'):
                S_inv_R = witness.localized_ring
            if S_inv_R is None and R is not None and S is not None and hasattr(R, 'localize'):
                S_inv_R = R.localize(S)
        except Exception:
            pass

    # Evaluate H1
    try:
        if R is not None:
            if hasattr(R, 'is_noetherian'):
                h1 = bool(R.is_noetherian() if callable(R.is_noetherian) else R.is_noetherian)
            elif hasattr(R, 'is_Noetherian'):
                h1 = bool(R.is_Noetherian() if callable(R.is_Noetherian) else R.is_Noetherian)
        elif hasattr(witness, 'is_noetherian'):
            h1 = bool(witness.is_noetherian() if callable(witness.is_noetherian) else witness.is_noetherian)
    except Exception:
        pass

    # Evaluate H2
    try:
        if S is not None:
            if hasattr(S, 'is_multiplicatively_closed'):
                h2 = bool(S.is_multiplicatively_closed() if callable(S.is_multiplicatively_closed) else S.is_multiplicatively_closed)
        elif hasattr(witness, 'is_multiplicatively_closed'):
            h2 = bool(witness.is_multiplicatively_closed() if callable(witness.is_multiplicatively_closed) else witness.is_multiplicatively_closed)
    except Exception:
        pass

    # Evaluate neg_Q
    try:
        if S_inv_R is not None:
            if hasattr(S_inv_R, 'is_noetherian'):
                neg_q = not bool(S_inv_R.is_noetherian() if callable(S_inv_R.is_noetherian) else S_inv_R.is_noetherian)
            elif hasattr(S_inv_R, 'is_Noetherian'):
                neg_q = not bool(S_inv_R.is_Noetherian() if callable(S_inv_R.is_Noetherian) else S_inv_R.is_Noetherian)
        elif hasattr(witness, 'localized_is_noetherian'):
            neg_q = not bool(witness.localized_is_noetherian() if callable(witness.localized_is_noetherian) else witness.localized_is_noetherian)
    except Exception:
        pass

    return [h1, h2, neg_q]