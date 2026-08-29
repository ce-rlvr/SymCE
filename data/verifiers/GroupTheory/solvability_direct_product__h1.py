import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
    "H_1: H is a group",
    "¬Q: The conclusion 'G x H is solvable iff both G and H are solvable' fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            H = witness.get('H')
        else:
            G, H = witness
    except Exception:
        return [False, False]
        
    # H_1: H is a group
    try:
        h1 = isinstance(H, PermutationGroup)
    except Exception:
        h1 = False
        
    # Conclusion: G x H is solvable iff G and H are solvable
    try:
        left = (G * H).is_solvable
        right = G.is_solvable and H.is_solvable
        q = bool(left == right)
    except Exception:
        # If G is not a group, operations like G * H or G.is_solvable will raise an exception.
        # This means the mathematical statement is undefined/nonsensical, so the conclusion fails.
        q = False
        
    neg_q = not q
    
    return [h1, neg_q]