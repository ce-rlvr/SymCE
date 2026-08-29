import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
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
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple (G, N) where G is a group and N is a subgroup.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(N, PermutationGroup) and 
              N.is_subgroup(G) and 
              G.is_normal(N))
    except Exception:
        h1 = False
        
    # neg_Q: The conclusion fails
    # Conclusion: The map H ↦ H/N is a bijection between the set of subgroups of G containing N 
    # and the set of subgroups of G/N, and H is normal in G if and only if H/N is normal in G/N.
    try:
        subgroups_G = G.subgroups()
        subgroups_containing_N = [H for H in subgroups_G if N.is_subgroup(H)]
        
        Q = G.quotient_group(N)
        subgroups_Q = Q.subgroups()
        
        # Check if it is a bijection (sizes of finite sets must match)
        bijection_ok = (len(subgroups_containing_N) == len(subgroups_Q))
        
        # Check if normality is preserved both ways (sizes of normal subgroup sets must match)
        normal_subgroups_containing_N = [H for H in subgroups_containing_N if G.is_normal(H)]
        normal_subgroups_Q = [K for K in subgroups_Q if Q.is_normal(K)]
        
        normality_ok = (len(normal_subgroups_containing_N) == len(normal_subgroups_Q))
        
        conclusion_holds = bijection_ok and normality_ok
        neg_q = not conclusion_holds
    except Exception:
        # If quotient group or subgroups cannot be computed, the conclusion fails to hold
        neg_q = True
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The map H ↦ H/N is not a bijection or does not preserve normality"
]

N_HYP = 1
NEG_Q_INDEX = 1