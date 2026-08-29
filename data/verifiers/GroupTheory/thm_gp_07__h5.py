import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The conjecture claims that the group G defined by the presentation:
      < s_1, ..., s_{n-1} | s_i^2 = 1, (s_i s_{i+1})^3 = 1 >
    is isomorphic to S_n.
    
    This is false because the relation (s_i s_j)^2 = 1 for |i - j| >= 2 is missing.
    Without it, the universal group G is an infinite Coxeter group for all n >= 4.
    Since G is uniquely determined by n, the only free variable is n.
    """
    n = None
    
    # Extract n from various possible witness formats
    if isinstance(witness, int):
        n = witness
    elif isinstance(witness, dict) and 'n' in witness:
        n = witness['n']
    elif isinstance(witness, (tuple, list)) and len(witness) > 0:
        if isinstance(witness[0], int):
            n = witness[0]
        elif hasattr(witness[0], 'generators'):
            n = len(witness[0].generators) + 1
    elif hasattr(witness, 'generators'):
        n = len(witness.generators) + 1

    try:
        n = int(n)
        h1 = (n >= 2)
    except Exception:
        h1 = False

    # H2: G is the group defined by the presentation.
    # Since G is uniquely determined by n, this is vacuously true for the universal group G_n.
    h2 = h1

    # H3: The generators satisfy s_i^2 = 1.
    # True by definition of the presentation of G_n.
    h3 = h1

    # H4: The generators satisfy (s_i s_{i+1})^3 = 1.
    # True by definition of the presentation of G_n.
    h4 = h1

    # Neg_Q: G_n is not isomorphic to S_n.
    # For n = 2, G_2 = <s1 | s1^2 = 1> = Z_2 = S_2.
    # For n = 3, G_3 = <s1, s2 | s1^2 = s2^2 = (s1 s2)^3 = 1> = S_3.
    # For n >= 4, G_n is an infinite Coxeter group (since m_{13} = \infty), 
    # while S_n is finite. Thus, G_n is not isomorphic to S_n.
    try:
        neg_q = h1 and (n >= 4)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "H_2: G is the group defined by the presentation with generators s_1, ..., s_{n-1}",
    "H_3: The generators satisfy s_i^2 = 1 for all 1 <= i <= n-1",
    "H_4: The generators satisfy (s_i s_{i+1})^3 = 1 for all 1 <= i <= n-2",
    "¬Q: The group G is not isomorphic to the symmetric group S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4