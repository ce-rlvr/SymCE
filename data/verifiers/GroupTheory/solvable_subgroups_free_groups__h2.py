import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # Extract F and H from the witness
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            H = witness.get('H')
        elif hasattr(witness, 'F') and hasattr(witness, 'H'):
            F = witness.F
            H = witness.H
        else:
            F, H = witness
    except Exception:
        return [False, False]

    # H_1: F is a free group
    try:
        if type(F).__name__ == 'FreeGroup':
            h1_ok = True
        elif type(F).__name__ == 'FpGroup' and len(F.relators) == 0:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: H is not a cyclic group
    try:
        is_cyclic = False
        if hasattr(H, 'is_cyclic') and H.is_cyclic is not None:
            is_cyclic = bool(H.is_cyclic)
        elif type(H).__name__ == 'FreeGroup':
            is_cyclic = (len(H.generators) <= 1)
        else:
            # If H is a subgroup or a list of elements in a free group,
            # it is cyclic iff its generators commute.
            gens = None
            if isinstance(H, (list, tuple)):
                gens = H
            elif hasattr(H, 'generators'):
                gens = H.generators
            
            if gens is not None:
                is_cyclic = True
                for i in range(len(gens)):
                    for j in range(i+1, len(gens)):
                        if gens[i]*gens[j] != gens[j]*gens[i]:
                            is_cyclic = False
                            break
                    if not is_cyclic:
                        break
            else:
                is_cyclic = False
                
        neg_q_ok = not is_cyclic
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: H is not a cyclic group"
]

N_HYP = 1
NEG_Q_INDEX = 1