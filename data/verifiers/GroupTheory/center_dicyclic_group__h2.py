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
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be an integer n.
    """
    # H_1: Let n be an integer such that n >= 2
    try:
        h1 = isinstance(witness, int) and witness >= 2
    except Exception:
        h1 = False

    # ¬Q: The center Z(Dic_n) is NOT a cyclic subgroup of order 2
    try:
        if not h1:
            neg_q = False
        else:
            n = witness
            
            # Construct the Dicyclic group Dic_n of order 4n using a faithful permutation representation.
            # Presentation: < a, x | a^{2n} = 1, x^2 = a^n, x^{-1} a x = a^{-1} >
            # We use a representation on 4n points.
            a_list = [(i + 1) % (2 * n) for i in range(2 * n)] + [2 * n + (i + 1) % (2 * n) for i in range(2 * n)]
            x_list = [2 * n + (-i) % (2 * n) for i in range(2 * n)] + [(n - i) % (2 * n) for i in range(2 * n)]
            
            A = Permutation(a_list)
            X = Permutation(x_list)
            Dic_n = PermutationGroup(A, X)
            
            # Compute the center of Dic_n
            C = Dic_n.center()
            
            # Check if the center is a cyclic subgroup of order 2
            # Note: Any group of order 2 is trivially cyclic.
            is_cyclic_order_2 = (C.order() == 2)
            
            neg_q = not is_cyclic_order_2
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let n be an integer such that n >= 2",
    "¬Q: The center Z(Dic_n) is not a cyclic subgroup of order 2"
]

N_HYP = 1
NEG_Q_INDEX = 1