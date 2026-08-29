import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
# V4 is the Klein four-group, a normal subgroup of S4
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    "H_1: N is a normal subgroup of S_n",
    "¬Q: N is not the trivial subgroup, not A_n, and not S_n"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness can be a tuple (n, N) or just N (where n is inferred from N.degree)
        if isinstance(witness, tuple):
            n, N_obj = witness
        else:
            n, N_obj = None, witness
            
        # Allow N to be passed as a list of permutations
        if isinstance(N_obj, list):
            N = PermutationGroup(*N_obj)
        else:
            N = N_obj
            
        if n is None:
            n = getattr(N, 'degree', None)
            
        if not isinstance(n, int) or n < 1:
            return [False, False]
            
        if not isinstance(N, PermutationGroup):
            return [False, False]
    except Exception:
        return [False, False]
        
    # H1: N is a normal subgroup of S_n
    try:
        Sn = SymmetricGroup(n)
        
        # Check if N is a subgroup of Sn
        is_subgroup = True
        for h in N.generators:
            if h not in Sn:
                is_subgroup = False
                break
                
        # Check normality: g * h * g^-1 in N for all generators g of Sn and h of N
        is_normal = True
        if is_subgroup:
            for g in Sn.generators:
                for h in N.generators:
                    if (g * h * ~g) not in N:
                        is_normal = False
                        break
                if not is_normal:
                    break
        else:
            is_normal = False
            
        h1_ok = is_subgroup and is_normal
    except Exception:
        h1_ok = False
        
    # Neg_Q: N is not trivial, not A_n, not S_n
    try:
        Sn = SymmetricGroup(n)
        is_trivial = (N.order() == 1)
        is_Sn = (N.order() == Sn.order())
        
        if n < 2:
            is_An = False
        else:
            An = AlternatingGroup(n)
            is_An = (N.order() == An.order())
            if is_An:
                for h in N.generators:
                    if h not in An:
                        is_An = False
                        break
                        
        neg_q_ok = not (is_trivial or is_An or is_Sn)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]