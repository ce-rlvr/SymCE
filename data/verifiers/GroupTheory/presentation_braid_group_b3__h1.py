import sympy
from sympy.combinatorics.free_groups import FreeGroup, free_group
from sympy.combinatorics.fp_groups import FpGroup
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

def conditions(witness):
    def h1(witness):
        try:
            if not hasattr(witness, 'generators') or not hasattr(witness, 'relators'):
                return False
            if len(witness.relators) != 1:
                return False
            
            gens = witness.generators
            rel = witness.relators[0]
            
            for i in range(len(gens)):
                for j in range(len(gens)):
                    if i == j:
                        continue
                    a = gens[i]
                    b = gens[j]
                    
                    # The relation is a * b * a = b * a * b
                    # As a relator, this is a * b * a * b^-1 * a^-1 * b^-1
                    expected = a * b * a * (b**-1) * (a**-1) * (b**-1)
                    
                    w_rel = rel.array_form
                    w_exp = expected.array_form
                    w_exp_inv = (expected**-1).array_form
                    
                    def get_cyclic(arr):
                        if len(arr) == 0:
                            return [()]
                        return [arr[k:] + arr[:k] for k in range(len(arr))]
                    
                    if w_rel in get_cyclic(w_exp) or w_rel in get_cyclic(w_exp_inv):
                        return True
            return False
        except Exception:
            return False

    def neg_q(witness):
        try:
            # The braid group B_3 has abelianization Z, so its abelian invariants should be [0].
            # If the invariants are not [0], the group is definitely not isomorphic to B_3.
            invs = witness.abelian_invariants
            if callable(invs):
                invs = invs()
            return list(invs) != [0]
        except Exception:
            return False

    return [h1(witness), neg_q(witness)]

CONDITION_LABELS = [
    "H_1: The set of relations R consist of the single relation σ_1 σ_2 σ_1 = σ_2 σ_1 σ_2",
    "¬Q: The group G is not isomorphic to the braid group on 3 strands, B_3"
]

N_HYP = 1
NEG_Q_INDEX = 1