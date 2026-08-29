import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Standard group theory bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Dihedral group of order 4 is isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def homology_not_trivial(F, k):
    """
    Returns True if we can mathematically determine that the k-th group homology 
    H_k(F, Z) is NOT the trivial group. Returns False otherwise.
    """
    try:
        if not hasattr(F, 'elements') or not hasattr(F, 'order'):
            return False
            
        order = int(F.order())
        if order <= 1:
            return False
            
        if order > 1000:
            return False # Prevent timeouts for excessively large groups
            
        # Check if the group is cyclic
        cyclic = False
        for g in F.elements:
            if int(g.order()) == order:
                cyclic = True
                break
                
        if cyclic:
            # For a finite cyclic group, H_k(F, Z) is isomorphic to F if k is odd, and 0 if k is even.
            return (k % 2 == 1)
            
        if getattr(F, 'is_abelian', False):
            # A finite abelian group that is not cyclic has non-trivial homology for all k >= 1
            return True
            
        # Hardcoded checks for common small non-abelian groups
        if order == 6: 
            # S3 has periodic cohomology, H_k != 0 iff k is odd
            return (k % 2 == 1)
            
        if order == 8:
            elements_order_2 = sum(1 for g in F.elements if int(g.order()) == 2)
            if elements_order_2 == 5: 
                # D4 has non-trivial homology for all k >= 1
                return True
            elif elements_order_2 == 1: 
                # Q8 has periodic cohomology, H_k != 0 iff k is odd
                return (k % 2 == 1)
                
        # For other common groups, we can at least check the Schur multiplier (H_2)
        if k == 2:
            if order == 12: # A4
                return True
            if order == 24: # S4
                return True
            if order == 60: # A5
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample.
    The witness is expected to be a tuple (F, k) or a dict {'F': F, 'k': k}.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            k = witness.get('k')
        elif isinstance(witness, tuple) and len(witness) == 2:
            F, k = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: k is an integer such that k >= 2
    try:
        if not isinstance(k, (int, sympy.Integer)):
            h1 = False
        else:
            k_val = int(k)
            h1 = (k_val >= 2)
    except Exception:
        h1 = False
        
    # ¬Q: The k-th group homology H_k(F, Z) is NOT the trivial group
    try:
        k_val_for_q = int(k)
        neg_q = homology_not_trivial(F, k_val_for_q)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is an integer such that k >= 2",
    "¬Q: The k-th group homology H_k(F, Z) is not the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1