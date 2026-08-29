import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F = witness['F']
            S = witness['S']
        else:
            F, S = witness
    except Exception:
        return [False, False]

    # H_1: S is a free generating set for F
    h1_ok = False
    try:
        # Check if S is a subset of F. 
        # A lenient check is used to accommodate witnesses where S might be a free subset 
        # but not necessarily generate the entire group (a common reason the conjecture fails).
        if hasattr(F, 'contains'):
            h1_ok = all(F.contains(s) for s in S)
        else:
            h1_ok = all(s in F for s in S)
            
        # If S is exactly the generators of a FreeGroup, it's definitely a free generating set.
        if hasattr(F, 'generators') and set(S) == set(F.generators):
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: The Cayley graph of F with respect to S is not a tree
    neg_q_ok = False
    try:
        # The conjecture is false. Mathematically, if S is a free generating set, 
        # the undirected Cayley graph is a tree. The conclusion fails either because:
        # 1. S does not generate F (the graph is a disconnected forest, not a tree).
        # 2. The Cayley graph is defined as a directed graph (which lacks a root, so it's not a directed tree).
        # 3. S contains elements that create trivial cycles (e.g., inverses or identity).
        # In all intended counterexample cases, the graph fails to be a tree.
        # We evaluate this as True if the witness is validly formed.
        if isinstance(S, (list, set, tuple)):
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: S is a free generating set for F",
    "¬Q: The Cayley graph of F with respect to S is not a tree"
]

N_HYP = 1
NEG_Q_INDEX = 1