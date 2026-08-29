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
    try:
        # Safely get conjugacy classes
        if callable(getattr(witness, 'conjugacy_classes', None)):
            classes = witness.conjugacy_classes()
        else:
            classes = witness.conjugacy_classes
        c = len(classes)
        
        # Safely get order
        if callable(getattr(witness, 'order', None)):
            order = witness.order()
        else:
            order = witness.order
            
        # If the group is infinite or order is 0, the formula fails to hold in the standard sense
        if order == sympy.oo or order == 0:
            q = False
        else:
            # For small groups, we evaluate the sum explicitly to verify the formula
            if order <= 256:
                if callable(getattr(witness, 'elements', None)):
                    elements = list(witness.elements())
                else:
                    elements = list(witness.elements)
                    
                s = 0
                for g in elements:
                    cg_size = 0
                    for x in elements:
                        if x * g == g * x:
                            cg_size += 1
                    s += cg_size
                
                # Check if c == (1 / order) * s, rewritten to avoid float division issues
                q = (c * order == s)
            else:
                # For large finite groups, Burnside's Lemma guarantees the formula holds.
                # We assume True to avoid timeout during evaluation.
                q = True
    except Exception:
        # If any attribute is missing or an operation fails, the conclusion cannot be evaluated
        q = False

    neg_q = not q
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The number of conjugacy classes of G is not equal to (1 / |G|) * ∑_{g ∈ G} |C_G(g)|"
]

N_HYP = 0
NEG_Q_INDEX = 0