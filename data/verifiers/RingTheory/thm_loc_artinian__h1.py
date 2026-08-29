import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol

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
    "H_1: R is an Artinian ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized ring S^{-1}R is not an Artinian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    try:
        # Dictionary-based witness
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_artinian", False))
            h2 = bool(witness.get("is_multiplicatively_closed", False))
            neg_q = not bool(witness.get("localized_is_artinian", True))
            return [h1, h2, neg_q]

        # Determine R and S if provided as tuple or attributes
        R = None
        S = None
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'S'):
            R = witness.R
            S = witness.S

        if R is not None and S is not None:
            try:
                h1_val = R.is_artinian() if callable(getattr(R, 'is_artinian', None)) else R.is_artinian
                h1 = bool(h1_val)
            except Exception:
                h1 = False
                
            try:
                h2_val = S.is_multiplicatively_closed() if callable(getattr(S, 'is_multiplicatively_closed', None)) else S.is_multiplicatively_closed
                h2 = bool(h2_val)
            except Exception:
                h2 = False
                
            try:
                if hasattr(R, 'localize'):
                    loc = R.localize(S)
                    q_val = loc.is_artinian() if callable(getattr(loc, 'is_artinian', None)) else loc.is_artinian
                    neg_q = not bool(q_val)
                elif hasattr(witness, 'localized_is_artinian'):
                    q_val = witness.localized_is_artinian() if callable(getattr(witness, 'localized_is_artinian', None)) else witness.localized_is_artinian
                    neg_q = not bool(q_val)
            except Exception:
                neg_q = False
                
            return [h1, h2, neg_q]

        # Fallback to single object witness
        try:
            h1_val = witness.is_artinian() if callable(getattr(witness, 'is_artinian', None)) else witness.is_artinian
            h1 = bool(h1_val)
        except Exception:
            h1 = False
            
        try:
            h2_val = witness.is_multiplicatively_closed() if callable(getattr(witness, 'is_multiplicatively_closed', None)) else witness.is_multiplicatively_closed
            h2 = bool(h2_val)
        except Exception:
            h2 = False
            
        try:
            if hasattr(witness, 'localized_is_artinian'):
                q_val = witness.localized_is_artinian() if callable(getattr(witness, 'localized_is_artinian', None)) else witness.localized_is_artinian
                neg_q = not bool(q_val)
            elif hasattr(witness, 'localize'):
                loc = witness.localize()
                q_val = loc.is_artinian() if callable(getattr(loc, 'is_artinian', None)) else loc.is_artinian
                neg_q = not bool(q_val)
        except Exception:
            neg_q = False

    except Exception:
        pass

    return [h1, h2, neg_q]