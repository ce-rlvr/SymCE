import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    Returns a list of booleans: [neg_Q]
    """
    # Attempt to interpret the witness as a group and check its number of Sylow 5-subgroups
    try:
        if hasattr(witness, 'sylow_subgroup'):
            order = witness.order()
            # Safeguard against extremely large groups timing out
            if order > 100000:
                return [False]
            
            if order % 5 != 0:
                num_sylow_5 = 1
            else:
                P = witness.sylow_subgroup(5)
                P_elements = set(P.elements)
                normalizer_size = 0
                for g in witness.elements:
                    # Check if g normalizes P by checking the generators
                    if all((g * gen * ~g) in P_elements for gen in P.generators):
                        normalizer_size += 1
                num_sylow_5 = order // normalizer_size
            
            neg_q = not (num_sylow_5 == 6)
            return [neg_q]
    except Exception:
        pass

    # Attempt to interpret the witness as the integer number of Sylow 5-subgroups
    try:
        if isinstance(witness, int):
            return [not (witness == 6)]
    except Exception:
        pass

    # Fallback: evaluate the literal statement about A_5
    try:
        A5 = AlternatingGroup(5)
        P = A5.sylow_subgroup(5)
        P_elements = set(P.elements)
        normalizer_size = 0
        for g in A5.elements:
            if all((g * gen * ~g) in P_elements for gen in P.generators):
                normalizer_size += 1
        num_sylow_5 = A5.order() // normalizer_size
        neg_q = not (num_sylow_5 == 6)
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The number of Sylow 5-subgroups in A_5 is not exactly 6"
]

N_HYP = 0
NEG_Q_INDEX = 0