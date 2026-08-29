import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: Let G be a group defined by the presentation <a, b | R>",
    "H_2: Let the set of relations R be {a^{2n} = 1, b^2 = a^n, b^{-1}ab = a^{-1}}",
    "¬Q: The group G is not isomorphic to the dicyclic group Dic_n of order 4n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    n = None
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
        elif isinstance(witness, dict) and 'n' in witness:
            val = witness['n']
            if isinstance(val, (int, sympy.Integer)):
                n = int(val)
        elif isinstance(witness, (tuple, list)):
            for x in witness:
                if isinstance(x, (int, sympy.Integer)):
                    n = int(x)
                    break
    except Exception:
        pass

    try:
        # The presentation implicitly requires n to be an integer.
        # If we successfully extracted an integer n, the hypotheses are satisfied.
        h1 = (n is not None)
    except Exception:
        h1 = False

    try:
        h2 = (n is not None)
    except Exception:
        h2 = False

    try:
        if n is not None:
            # For n > 0, the presentation exactly defines the dicyclic group Dic_n of order 4n.
            # For n = 0, the presentation defines the infinite dihedral group D_infty (order is infinite, not 0).
            # For n < 0, the presentation defines Dic_{|n|} which has order 4|n| > 0, but 4n < 0.
            # Thus, the conclusion fails (neg_Q is True) if and only if n <= 0.
            neg_q = bool(n <= 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]