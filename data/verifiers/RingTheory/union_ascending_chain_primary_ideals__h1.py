import sympy
from sympy import *
import sympy.combinatorics as combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    h1, h2, h3, neg_q = False, False, False, False

    # H_1: P is a prime ideal in R
    try:
        if hasattr(witness, 'P') and hasattr(witness.P, 'is_prime'):
            h1 = bool(witness.P.is_prime())
        elif hasattr(witness, 'is_prime'):
            h1 = bool(witness.is_prime(witness.P))
    except Exception:
        pass

    # H_2: Q_1 \subseteq Q_2 \subseteq \dots is an ascending chain of ideals in R
    try:
        if hasattr(witness, 'is_ascending_chain'):
            h2 = bool(witness.is_ascending_chain(witness.Q_chain))
        elif hasattr(witness, 'Q_chain'):
            h2 = True
            for i in range(len(witness.Q_chain) - 1):
                if not witness.Q_chain[i].issubset(witness.Q_chain[i+1]):
                    h2 = False
                    break
    except Exception:
        pass

    # H_3: For all i \geq 1, Q_i is a P-primary ideal
    try:
        if hasattr(witness, 'is_P_primary'):
            h3 = all(witness.is_P_primary(q, witness.P) for q in witness.Q_chain)
        elif hasattr(witness, 'Q_chain'):
            h3 = True
            for q in witness.Q_chain:
                if hasattr(q, 'is_P_primary'):
                    if not q.is_P_primary(witness.P):
                        h3 = False
                        break
                else:
                    h3 = False
                    break
    except Exception:
        pass

    # ¬Q: The union \bigcup_{i=1}^\infty Q_i is not a P-primary ideal
    try:
        if hasattr(witness, 'is_P_primary'):
            neg_q = not witness.is_P_primary(witness.union_Q, witness.P)
        elif hasattr(witness, 'union_Q') and hasattr(witness.union_Q, 'is_P_primary'):
            neg_q = not witness.union_Q.is_P_primary(witness.P)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal in R",
    "H_2: Q_1 \\subseteq Q_2 \\subseteq \\dots is an ascending chain of ideals in R",
    "H_3: For all i \\geq 1, Q_i is a P-primary ideal",
    "¬Q: The union \\bigcup_{i=1}^\\infty Q_i is not a P-primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3