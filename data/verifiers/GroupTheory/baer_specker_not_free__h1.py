import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    Checks if the witness satisfies the remaining hypotheses and the negated conclusion.
    """
    # H_1: G is the direct product of countably infinitely many copies of Z
    h1 = False
    try:
        w_str = str(witness).lower().replace(" ", "").replace("_", "")
        baer_specker_names = [
            "z^n", "z**n", "z^omega", "z**omega", "z^infty", "z**infty",
            "baerspecker", "baerspeckergroup", "prod(z)", "z^aleph0", "z**aleph0",
            "directproductofcountablyinfinitelymanycopiesofz",
            "z^n0", "z**n0", "z**oo", "z^oo",
            "product(z,(i,1,oo))", "product(z,(i,1,infty))"
        ]
        if w_str in baer_specker_names:
            h1 = True
    except Exception:
        pass

    # neg_Q: G is a free abelian group
    neg_q = False
    try:
        w_str = str(witness).lower().replace(" ", "").replace("_", "")
        baer_specker_names = [
            "z^n", "z**n", "z^omega", "z**omega", "z^infty", "z**infty",
            "baerspecker", "baerspeckergroup", "prod(z)", "z^aleph0", "z**aleph0",
            "directproductofcountablyinfinitelymanycopiesofz",
            "z^n0", "z**n0", "z**oo", "z^oo",
            "product(z,(i,1,oo))", "product(z,(i,1,infty))"
        ]
        if w_str in baer_specker_names:
            # The Baer-Specker group is NOT a free abelian group.
            neg_q = False
        elif w_str in ["z", "z^2", "z**2", "z^3", "z**3", "z^k", "z**k", "z^m", "z**m", "integers"]:
            neg_q = True
        elif "oplus" in w_str or "directsum" in w_str:
            neg_q = True
        elif "productset" in w_str and "integers" in w_str:
            neg_q = True
        elif isinstance(witness, PermutationGroup):
            # A finite free abelian group must be the trivial group
            if witness.order() == 1:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is the direct product of countably infinitely many copies of Z",
    "¬Q: G is a free abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1