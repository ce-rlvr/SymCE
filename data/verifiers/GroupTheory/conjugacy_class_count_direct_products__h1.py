import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H).
    """
    try:
        G, H = witness
    except Exception:
        # If witness is not a tuple of two elements, it's invalid.
        return [False, False]
        
    # H_1: H is a finite group
    try:
        # In SymPy, PermutationGroup instances are finite groups.
        h1_ok = isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # neg_Q: The conclusion FAILS at the witness
    # Conclusion: The number of conjugacy classes of G x H is equal to the product 
    # of the number of conjugacy classes of G and H.
    try:
        try:
            cG = len(G.conjugacy_classes())
            cH = len(H.conjugacy_classes())
            GxH = G * H
            cGxH = len(GxH.conjugacy_classes())
            concl = (cGxH == cG * cH)
        except Exception:
            # If G is not a group (e.g. an integer or string), evaluating its conjugacy 
            # classes or direct product will raise an exception. In this case, the 
            # conclusion is undefined/meaningless, which means the equality is false.
            concl = False
            
        neg_q_ok = not concl
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "¬Q: The number of conjugacy classes of G x H is not equal to the product of the number of conjugacy classes of G and H"
]

N_HYP = 1
NEG_Q_INDEX = 1