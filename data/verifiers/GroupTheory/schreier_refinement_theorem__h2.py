import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: The normal series A and B do not have equivalent refinements"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, A, B = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            A, B = witness
            G = A[0]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: G is a group
    try:
        h1 = hasattr(G, 'generators') and hasattr(G, 'order')
    except Exception:
        h1 = False

    # ¬Q: The normal series A and B DO NOT have equivalent refinements.
    # By Schreier's Refinement Theorem, any two valid subnormal series have equivalent refinements.
    # Thus, they fail to have equivalent refinements if and only if they are not valid subnormal series.
    def is_subnormal(grp, seq):
        try:
            if not isinstance(seq, list): 
                return False
            if len(seq) < 2: 
                return False
            
            # Must start with G
            if seq[0] != grp:
                if seq[0].order() != grp.order() or not seq[0].is_subgroup(grp):
                    return False
                    
            # Must end with the trivial group
            if seq[-1].order() != 1: 
                return False
            
            # Each step must be a normal subgroup of the previous
            for i in range(len(seq)-1):
                H = seq[i]
                K = seq[i+1]
                
                if K.order() == 1:
                    continue  # The trivial group is always a normal subgroup
                    
                if not hasattr(H, 'is_subgroup') or not hasattr(K, 'is_subgroup'):
                    return False
                if not K.is_subgroup(H): 
                    return False
                    
                # Check normality: for all h in H, h * K * h^-1 == K
                for h in H.generators:
                    for k in K.generators:
                        if (h * k * ~h) not in K:
                            return False
            return True
        except Exception:
            return False

    try:
        a_sub = is_subnormal(G, A)
        b_sub = is_subnormal(G, B)
        # The conclusion fails if at least one is not a valid subnormal series
        neg_q = not (a_sub and b_sub)
    except Exception:
        neg_q = False

    return [h1, neg_q]