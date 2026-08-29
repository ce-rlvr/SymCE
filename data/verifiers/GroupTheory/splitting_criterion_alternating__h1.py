import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, Permutation
from sympy.combinatorics.named_groups import CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
        n, x = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: S_n is the symmetric group on n letters
    try:
        h1 = (int(n) == n) and (n >= 1)
    except Exception:
        h1 = False

    # H_2: A_n is the alternating group on n letters
    try:
        h2 = (int(n) == n) and (n >= 1)
    except Exception:
        h2 = False

    # H_3: x is an element of A_n
    try:
        if h2:
            An = AlternatingGroup(n)
            h3 = x in An
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: The conjugacy class of x in S_n splits into two distinct conjugacy classes 
    # of equal size in A_n if and only if the centralizer of x in S_n is a subgroup of A_n.
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            Sn = SymmetricGroup(n)
            An = AlternatingGroup(n)
            
            Sn_elements = list(Sn.elements)
            An_elements = list(An.elements)
            
            # Conjugacy class of x in Sn
            cc_Sn = set()
            for g in Sn_elements:
                cc_Sn.add(g * x * ~g)
                
            # Conjugacy class of x in An
            cc_An = set()
            for g in An_elements:
                cc_An.add(g * x * ~g)
                
            # Check if it splits into two distinct conjugacy classes of equal size in An
            lhs = (len(cc_Sn) == 2 * len(cc_An))
            
            # Centralizer of x in Sn
            cent_Sn = set()
            for g in Sn_elements:
                if g * x == x * g:
                    cent_Sn.add(g)
                    
            # Check if centralizer is a subgroup of An
            An_set = set(An_elements)
            rhs = cent_Sn.issubset(An_set)
            
            q = (lhs == rhs)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S_n is the symmetric group on n letters",
    "H_2: A_n is the alternating group on n letters",
    "H_3: x is an element of A_n",
    "¬Q: The splitting criterion iff statement fails"
]

N_HYP = 3
NEG_Q_INDEX = 3