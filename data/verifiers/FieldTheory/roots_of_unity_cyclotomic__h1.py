import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness):
    try:
        w = sympy.sympify(witness)
        if not w.is_integer:
            return [False, False]
        n = int(w)
    except Exception:
        return [False, False]
        
    try:
        # H1: \mathbb{Q}(\zeta_n) is the n-th cyclotomic field
        # This implies n is a non-zero integer.
        h1 = (n != 0)
    except Exception:
        h1 = False
        
    try:
        # neg_Q: The group of roots of unity contained in \mathbb{Q}(\zeta_n) has order 2n if n is odd, and order n if n is even
        # We check if the actual order is DIFFERENT from the formula given in the conclusion.
        abs_n = abs(n)
        
        # The actual order of the group of roots of unity in the |n|-th cyclotomic field
        if abs_n % 2 == 1:
            actual_order = 2 * abs_n
        else:
            actual_order = abs_n
            
        # The order predicted by the false conjecture's formula
        if n % 2 == 1:
            formula_order = 2 * n
        else:
            formula_order = n
            
        neg_q = (actual_order != formula_order)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: \\mathbb{Q}(\\zeta_n) is the n-th cyclotomic field",
    "\\neg Q: The group of roots of unity contained in \\mathbb{Q}(\\zeta_n) does not have order 2n if n is odd, and order n if n is even"
]

N_HYP = 1
NEG_Q_INDEX = 1