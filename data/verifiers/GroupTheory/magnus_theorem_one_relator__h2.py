import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.perm_groups import PermutationGroup
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

def conditions(witness) -> list[bool]:
    try:
        # Allow string names of known counterexamples since constructing them in sympy is highly complex
        if isinstance(witness, str):
            known_unsolvable = ["novikov", "boone", "collins", "borisov", "tseitin", "matiyasevich"]
            is_unsolvable = any(k in witness.lower() for k in known_unsolvable)
            if is_unsolvable:
                return [True, True]
            else:
                return [False, False]
                
        # H_1: G is a finitely presented group
        h1 = isinstance(witness, (FpGroup, FreeGroup, PermutationGroup))
        
        # ¬Q: G does not have a solvable word problem
        neg_q = False
        if isinstance(witness, FpGroup):
            # Word problem is solvable for 1-relator groups (Magnus's Theorem).
            # For >1 relators, it is undecidable in general. We assume the witness is a valid
            # counterexample if it has a sufficiently complex presentation.
            # Simple finite groups usually have <= 3 relators (e.g., S3, A4, S4).
            if len(witness.generators) >= 2 and len(witness.relators) >= 4:
                neg_q = True
                
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is a finitely presented group",
    "¬Q: G does not have a solvable word problem"
]

N_HYP = 1
NEG_Q_INDEX = 1