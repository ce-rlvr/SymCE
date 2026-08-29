import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        # Compute the length of the lower central series
        lcs_len = len(witness.lower_central_series())
        
        # Compute the length of the upper central series
        elements = list(witness.generate())
        gens = witness.generators
        if not elements:
            return [False]
            
        identity = elements[0]**0
        U_elements = {identity}
        U_order = 1
        ucs_len = 1
        
        while True:
            next_U_elements = set()
            for g in elements:
                is_in_next = True
                for h in gens:
                    # Commutator [g, h] = g^-1 h^-1 g h
                    commutator = (g**-1) * (h**-1) * g * h
                    if commutator not in U_elements:
                        is_in_next = False
                        break
                if is_in_next:
                    next_U_elements.add(g)
            
            if len(next_U_elements) == U_order:
                break
            U_order = len(next_U_elements)
            U_elements = next_U_elements
            ucs_len += 1
            
        # The conclusion is that the lengths are equal.
        # The negated conclusion is that the lengths are NOT equal.
        neg_q = (lcs_len != ucs_len)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The length of the lower central series of G is not equal to the length of the upper central series of G"
]

N_HYP = 0
NEG_Q_INDEX = 0