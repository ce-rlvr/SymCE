import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, "normal_subgroups"):
            return [False]
        
        normal_sgs = witness.normal_subgroups()
        ns_sets = [set(H.elements) for H in normal_sgs]
        ns_sets.sort(key=len)
        
        bottom = ns_sets[0]
        top = ns_sets[-1]
        
        def join(X, Y):
            for H in ns_sets:
                if X.issubset(H) and Y.issubset(H):
                    return H
            return top
            
        is_boolean = True
        
        # Check if the lattice is complemented
        for A in ns_sets:
            has_complement = False
            for B in ns_sets:
                if len(A.intersection(B)) == len(bottom):
                    if len(A) * len(B) == len(top):
                        has_complement = True
                        break
            if not has_complement:
                is_boolean = False
                break
                
        # Check if the lattice is distributive
        if is_boolean:
            for A in ns_sets:
                for B in ns_sets:
                    for C in ns_sets:
                        B_join_C = join(B, C)
                        left = A.intersection(B_join_C)
                        
                        A_meet_B = A.intersection(B)
                        A_meet_C = A.intersection(C)
                        right = join(A_meet_B, A_meet_C)
                        
                        if left != right:
                            is_boolean = False
                            break
                    if not is_boolean: break
                if not is_boolean: break
                
        neg_q = not is_boolean
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: The set of all normal subgroups of G does not form a Boolean lattice"]
N_HYP = 0
NEG_Q_INDEX = 0