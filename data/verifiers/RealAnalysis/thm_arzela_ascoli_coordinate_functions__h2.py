import math
import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: X is a metric space
    h1 = True
    try:
        X = witness.X_sample + [witness.x0]
        d_X = witness.d_X
        for x in X:
            if abs(d_X(x, x)) > 1e-9:
                h1 = False
        for x, y in itertools.product(X, X):
            if x != y and d_X(x, y) <= 1e-9:
                h1 = False
            if abs(d_X(x, y) - d_X(y, x)) > 1e-9:
                h1 = False
            for z in X:
                if d_X(x, z) > d_X(x, y) + d_X(y, z) + 1e-9:
                    h1 = False
    except Exception:
        h1 = False

    # H_2: For each f \in \mathcal{F} and 1 \le i \le n, f_i(x) denotes the i-th coordinate function
    h2 = True
    try:
        n = witness.n
        if n < 1:
            h2 = False
        for f in witness.F:
            for x in X:
                fx = f(x)
                if len(fx) != n:
                    h2 = False
    except Exception:
        h2 = False

    # H_3: The family \mathcal{F} is equicontinuous at a point x_0 \in X
    h3 = True
    try:
        x0 = witness.x0
        d_Y = witness.d_Y
        for eps in witness.epsilons_H3:
            delta = witness.get_delta_H3(eps)
            for x in X:
                if d_X(x, x0) < delta:
                    for f in witness.F:
                        if d_Y(f(x), f(x0)) >= eps:
                            h3 = False
    except Exception:
        h3 = False

    # ¬Q: For some 1 \le i \le n, the family of coordinate functions \mathcal{F}_i is not equicontinuous at x_0
    neg_q = True
    try:
        eps_q = witness.epsilon_negQ
        i_q = witness.i_negQ
        x0 = witness.x0
        d_X = witness.d_X
        
        for delta in witness.deltas_negQ:
            x, f = witness.get_violating_x_and_f(delta)
            if d_X(x, x0) >= delta:
                neg_q = False
            if abs(f(x)[i_q - 1] - f(x0)[i_q - 1]) < eps_q:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: For each f in F and 1 <= i <= n, f_i(x) denotes the i-th coordinate function",
    "H_3: The family F is equicontinuous at x_0",
    "¬Q: For some i, the family of coordinate functions F_i is not equicontinuous at x_0"
]

N_HYP = 3
NEG_Q_INDEX = 3