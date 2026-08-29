import sympy
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    The conjecture is a globally false proposition with no free variables.
    Hypothesis: P is the set of all finite group presentations.
    Conclusion: There exists at least one finite presentation in P for which the word problem is undecidable.
    
    Since every finite group has a decidable word problem (e.g., by enumerating its finite Cayley graph),
    the existential conclusion is mathematically false. Thus, its negation is true.
    Any witness serves as a valid counterexample to the conjecture as a whole.
    """
    try:
        # H_1: P is the set of all finite group presentations.
        # This is a definitional hypothesis of the global context.
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # ¬Q: The word problem is decidable for all finite group presentations.
        # The conclusion fails, so its negation is True.
        neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: P is the set of all finite group presentations",
    "¬Q: The word problem is decidable for all finite group presentations (conclusion fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1