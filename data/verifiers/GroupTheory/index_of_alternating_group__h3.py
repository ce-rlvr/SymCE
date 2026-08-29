import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    # Extract n from witness
    try:
        if isinstance(witness, (tuple, list)):
            n_val = witness[0]
        else:
            n_val = witness
            
        if float(n_val) != int(n_val):
            h1 = False
        else:
            n = int(n_val)
            h1 = (n >= 2)
    except Exception:
        h1 = False

    # H2: S_n is the symmetric group of degree n (definitional hypothesis)
    try:
        h2 = h1
    except Exception:
        h2 = False

    # Conclusion: The index of A_n in S_n is exactly 2, and A_n is a normal subgroup of S_n.
    try:
        if isinstance(witness, (tuple, list)):
            n = int(witness[0])
        else:
            n = int(witness)
            
        Sn = SymmetricGroup(n)
        An = AlternatingGroup(n)
        
        # Check index
        index = Sn.order() // An.order()
        
        # Check if An is a normal subgroup of Sn
        is_normal = True
        for g in Sn.generators:
            for h in An.generators:
                conj = g * h * (~g)
                if not An.contains(conj):
                    is_normal = False
                    break
            if not is_normal:
                break
                
        q = (index == 2) and is_normal
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "H_2: S_n is the symmetric group of degree n",
    "¬Q: The index of A_n in S_n is not exactly 2, or A_n is not a normal subgroup of S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2