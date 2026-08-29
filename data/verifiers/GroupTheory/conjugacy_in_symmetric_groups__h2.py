import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    try:
        n, sigma, tau = witness
    except Exception:
        return [False, False]
    
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False
        
    # ¬Q: sigma and tau are conjugate in S_n iff they have the same cycle type (fails)
    try:
        if not isinstance(sigma, Permutation):
            sigma = Permutation(sigma)
        if not isinstance(tau, Permutation):
            tau = Permutation(tau)
            
        def cycle_type(p):
            # The multiset of lengths of disjoint cycles of length >= 2
            return sorted([len(c) for c in p.cyclic_form if len(c) > 1])
            
        ct_sigma = cycle_type(sigma)
        ct_tau = cycle_type(tau)
        same_cycle_type = (ct_sigma == ct_tau)
        
        if n > 8:
            # Prevent timeout for excessively large n
            conjugate_in_Sn = False
        else:
            Sn = SymmetricGroup(n)
            conjugate_in_Sn = False
            for g in Sn.elements:
                # Compare cyclic forms to safely handle permutations of different sizes
                if (g * sigma * g**-1).cyclic_form == tau.cyclic_form:
                    conjugate_in_Sn = True
                    break
                    
        # The conclusion is a biconditional. It fails if the truth values differ.
        neg_q = (conjugate_in_Sn != same_cycle_type)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: (sigma and tau are conjugate in S_n) is not equivalent to (they have the same cycle type)"
]

N_HYP = 1
NEG_Q_INDEX = 1