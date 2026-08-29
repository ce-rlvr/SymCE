import math
import functools
import itertools
from sympy.combinatorics import PermutationGroup, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings for the witness expression
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = DirectProduct(Z2, Z2)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample.
    The witness should be a tuple (G, H).
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: H is a group with finite exponent
    try:
        # In SymPy, all PermutationGroups are finite, hence have a finite exponent.
        h1_ok = isinstance(H, PermutationGroup)
    except Exception:
        h1_ok = False

    # neg_Q: The exponent of the direct product G x H is equal to lcm(exp(G), exp(H))
    try:
        def _lcm(a, b):
            return abs(a * b) // math.gcd(a, b) if a and b else 0

        def get_exp(grp):
            if isinstance(grp, PermutationGroup):
                e = 1
                for g in grp.elements:
                    e = _lcm(e, g.order())
                return e
            # If it's not a finite permutation group, its exponent is undefined/infinite
            return None

        exp_G = get_exp(G)
        exp_H = get_exp(H)

        if exp_G is None or exp_H is None:
            # If either exponent is undefined, the equation exp(G x H) == lcm(...) is False
            q = False
        else:
            try:
                GxH = DirectProduct(G, H)
                exp_GxH = get_exp(GxH)
                if exp_GxH is None:
                    q = False
                else:
                    q = (exp_GxH == _lcm(exp_G, exp_H))
            except Exception:
                q = False

        neg_q = not q
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group with finite exponent",
    "¬Q: The exponent of the direct product G x H is not equal to lcm(exp(G), exp(H))"
]

N_HYP = 1
NEG_Q_INDEX = 1