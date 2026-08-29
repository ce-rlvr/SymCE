import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(obj):
    """Helper to check if an object is a valid group in SymPy."""
    if isinstance(obj, PermutationGroup):
        return True
    if hasattr(obj, 'is_group') and obj.is_group:
        return True
    if hasattr(obj, 'identity') and hasattr(obj, 'generators'):
        return True
    return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (G1, G2).
    """
    try:
        G1, G2 = witness
    except Exception:
        return [False, False]
        
    # H_1: \pi: G_1 \times G_2 \to G_1 is the projection map defined by \pi(g_1, g_2) = g_1
    # This is a definitional hypothesis establishing what \pi is, so it holds for any pair (G1, G2).
    try:
        h1_ok = True
    except Exception:
        h1_ok = False
    
    # Q: \pi is a surjective group homomorphism and its kernel is {e_1} \times G_2
    # The theorem is unconditionally true if G1 and G2 are both groups.
    # The dropped hypothesis was that G1 and G2 are groups.
    # If they are not both groups, the conclusion fails (e.g., \pi is not a group homomorphism).
    try:
        if is_group(G1) and is_group(G2):
            q_ok = True
        else:
            q_ok = False
    except Exception:
        q_ok = False
        
    neg_q_ok = not q_ok
    
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: \\pi is the projection map defined by \\pi(g_1, g_2) = g_1",
    "¬Q: \\pi is not a surjective group homomorphism or its kernel is not {e_1} \\times G_2"
]

N_HYP = 1
NEG_Q_INDEX = 1