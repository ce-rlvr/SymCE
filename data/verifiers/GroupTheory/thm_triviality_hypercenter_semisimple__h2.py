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
    try:
        # H_1: G is a semisimple finite group
        # In the context of finite groups of Lie type, a semisimple group 
        # (like SL(n, q)) is perfect (with a few small exceptions).
        # We check if G is a perfect group.
        if not isinstance(witness, PermutationGroup):
            h1 = False
        else:
            ds = witness.derived_subgroup()
            if isinstance(ds, list):
                h1 = (len(ds) == witness.order())
            else:
                h1 = (ds.order() == witness.order())
            
            # A trivial group is perfect but usually not considered a valid semisimple 
            # counterexample in this context, though its center is trivial anyway.
            if witness.order() == 1:
                h1 = False
    except Exception:
        h1 = False

    try:
        # ¬Q: Z_\infty(G) is not the trivial subgroup
        # The hypercenter of a finite group is trivial iff its center is trivial.
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            c = witness.center()
            if isinstance(c, list):
                neg_q = (len(c) > 1)
            else:
                neg_q = (c.order() > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "¬Q: Z_\\infty(G) is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1