import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup as requested
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

def conditions(witness):
    """
    Given a witness (G, M), checks if it is a valid counterexample to the conjecture.
    """
    try:
        G, M = witness
        
        # Ensure the witness components are groups
        if not (hasattr(G, 'order') and hasattr(M, 'order')):
            return [False, False]
            
        # H_1: M is a proper normal subgroup of G
        h1 = M.is_subgroup(G) and M.is_normal(G) and M.order() < G.order()
        
        # Conclusion: M is a maximal normal subgroup of G if and only if the quotient group G/M is simple.
        
        # LHS: M is a maximal normal subgroup of G
        # This means there is no normal subgroup N of G such that M < N < G.
        lhs = True
        for N in G.normal_subgroups():
            if N.order() > M.order() and N.order() < G.order():
                if M.is_subgroup(N):
                    lhs = False
                    break
                    
        # RHS: G/M is simple
        # By the correspondence theorem, normal subgroups of the quotient G/M correspond 
        # exactly to normal subgroups of G that contain M. 
        # A group is simple if and only if it has exactly two normal subgroups.
        count = sum(1 for N in G.normal_subgroups() if M.is_subgroup(N))
        rhs = (count == 2)
        
        # The negated conclusion holds if the equivalence fails
        neg_q = not (lhs == rhs)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: M is a proper normal subgroup of G",
    "¬Q: It is NOT the case that (M is a maximal normal subgroup of G iff G/M is simple)"
]

N_HYP = 1
NEG_Q_INDEX = 1