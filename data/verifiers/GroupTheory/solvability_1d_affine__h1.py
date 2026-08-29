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
V4 = DihedralGroup(2)
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
    r"H_1: G is the group of all affine transformations of the form x \mapsto ax + b, where a, b \in F and a \neq 0",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The hypothesis that G is the group of all affine transformations over some F 
        # (where non-zero elements are invertible) is mathematically equivalent to G 
        # being a sharply 2-transitive permutation group.
        n = witness.degree
        h1 = False
        
        order = witness.order() if callable(witness.order) else witness.order
        
        if n >= 2 and order == n * (n - 1):
            is_trans = witness.is_transitive() if callable(witness.is_transitive) else witness.is_transitive
            if is_trans:
                stab = witness.stabilizer(0)
                # Check if the stabilizer of a point is transitive on the remaining n-1 points
                for i in range(1, n):
                    orb = stab.orbit(i)
                    if len(orb) == n - 1:
                        h1 = True
                        break
    except Exception:
        h1 = False

    try:
        is_solv = witness.is_solvable() if callable(witness.is_solvable) else witness.is_solvable
        neg_q = not bool(is_solv)
    except Exception:
        neg_q = False

    return [h1, neg_q]