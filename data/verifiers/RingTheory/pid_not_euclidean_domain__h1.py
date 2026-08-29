import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        # Check if the witness is a Principal Ideal Domain (PID)
        is_pid = getattr(witness, 'is_PID', False)
        
        # Check if the witness is a Euclidean Domain (ED)
        # In SymPy, fields, ZZ, and univariate polynomial rings over fields are Euclidean Domains.
        is_ed = False
        if getattr(witness, 'is_Field', False):
            is_ed = True
        elif witness == ZZ:
            is_ed = True
        elif hasattr(witness, 'domain') and getattr(witness.domain, 'is_Field', False):
            if hasattr(witness, 'gens') and len(witness.gens) == 1:
                is_ed = True
                
        # The conclusion states that R is a PID AND R is not a Euclidean Domain.
        conclusion = is_pid and (not is_ed)
        
        # The negated conclusion is True when the conclusion fails.
        neg_q = not conclusion
        
        return [bool(neg_q)]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: R is not a principal ideal domain or R is a Euclidean domain"
]

N_HYP = 0
NEG_Q_INDEX = 0