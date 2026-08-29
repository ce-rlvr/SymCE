import sympy
from sympy import *
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness elements
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

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion for the false conjecture:
    'Localization commutes with symmetric powers' (missing hypothesis: M is an R-module).
    """
    try:
        R = witness['R']
        S = witness['S']
        k = witness['k']
        M = witness['M']
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    try:
        h1 = False
        if R in [sympy.ZZ, sympy.QQ]:
            h1 = True
        elif type(R).__name__.endswith('Ring') or type(R).__name__.endswith('Field'):
            h1 = True
        elif hasattr(R, 'get_ring'):
            h1 = True
        elif hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        h2 = True
        if isinstance(S, (set, list, tuple)) or (hasattr(S, 'is_FiniteSet') and S.is_FiniteSet):
            try:
                has_one = (1 in S) or (hasattr(R, 'one') and R.one in S)
            except Exception:
                has_one = False
                
            if not has_one:
                h2 = False
            else:
                for a in S:
                    for b in S:
                        try:
                            if (a * b) not in S:
                                h2 = False
                                break
                        except Exception:
                            h2 = False
                            break
                    if not h2:
                        break
        elif callable(S):
            try:
                if not S(1) and not (hasattr(R, 'one') and S(R.one)):
                    h2 = False
            except Exception:
                h2 = False
        elif hasattr(S, 'contains'):
            try:
                if not S.contains(1) and not (hasattr(R, 'one') and S.contains(R.one)):
                    h2 = False
            except Exception:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: k is a non-negative integer
    try:
        h3 = isinstance(k, int) and k >= 0
    except Exception:
        h3 = False

    # neg_Q: The conclusion fails
    # The theorem is unconditionally true for all valid R-modules.
    # The conclusion fails (or is undefined) precisely when M is not an R-module.
    try:
        is_module = False
        if hasattr(M, 'ring') and M.ring == R:
            is_module = True
        elif type(M).__name__ in ['FreeModule', 'SubModule', 'QuotientModule', 'Module']:
            is_module = True
            
        neg_q = not is_module
    except Exception:
        neg_q = True

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: k is a non-negative integer",
    "¬Q: The conclusion fails (e.g., M is not an R-module)"
]

N_HYP = 3
NEG_Q_INDEX = 3