import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.polys.domains.ring import Ring
from sympy.polys.domains.field import Field

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

def is_ring(R):
    try:
        if hasattr(R, 'is_Ring') and R.is_Ring:
            return True
        if isinstance(R, (Ring, Field)):
            return True
        if R in [ZZ, QQ, RR, CC]:
            return True
        if isinstance(R, sympy.Expr):
            return True
    except Exception:
        pass
    return False

def is_valid_module(M):
    try:
        if is_ring(M):
            return True
        if isinstance(M, list):
            if all(isinstance(s, (set, frozenset)) for s in M):
                return True
        try:
            from sympy.polys.agca.modules import Module
            if isinstance(M, Module):
                return True
        except Exception:
            pass
        if hasattr(M, 'is_Module') and M.is_Module:
            return True
        if type(M).__name__ in ['MatrixSpace', 'VectorSpace', 'ComplexSpace']:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = witness
            M = witness
    except Exception:
        R = witness
        M = witness

    # H_1: R is a ring
    try:
        h1_ok = bool(is_ring(R))
    except Exception:
        h1_ok = False

    # ¬Q: M satisfies DCC iff every non-empty collection of submodules has a minimal element
    # This equivalence is a tautology for any valid module (poset of submodules).
    # It fails (is undefined/meaningless) if M is not a valid module, which is the dropped hypothesis.
    try:
        if M is None:
            q_ok = False
        else:
            q_ok = bool(is_valid_module(M))
    except Exception:
        q_ok = False

    neg_q = not q_ok

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: M does not satisfy the equivalence (e.g., M is not a valid module)"
]

N_HYP = 1
NEG_Q_INDEX = 1