import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
import math
import itertools
import functools

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("H1", False))
            h2 = bool(witness.get("H2", False))
            h3 = bool(witness.get("H3", False))
            neg_q = bool(witness.get("neg_Q", False))
        else:
            h1 = bool(witness.is_metric_space())
            h2 = bool(witness.contains_x())
            h3 = bool(witness.seq_cond())
            neg_q = not bool(witness.is_equicontinuous())
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: x is a point in X",
    "H_3: For every sequence {f_n} in F and every sequence {x_n} in X converging to x, the sequence |f_n(x_n) - f_n(x)| converges to 0",
    "¬Q: The family F is not equicontinuous at x"
]

N_HYP = 3
NEG_Q_INDEX = 3