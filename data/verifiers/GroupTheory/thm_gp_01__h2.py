import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            X = witness['X']
            R = witness['R']
            H = witness['H']
            H_id = witness['H_id']
            H_op = witness['H_op']
            f = witness['f']
        else:
            X = witness.X
            R = witness.R
            H = witness.H
            H_id = witness.H_id
            H_op = witness.H_op
            f = witness.f
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group defined by the presentation <X | R>
    try:
        h1 = isinstance(X, (list, tuple, set)) and isinstance(R, (list, tuple, set))
        if h1:
            for word in R:
                if not isinstance(word, (list, tuple)):
                    h1 = False
                    break
                for item in word:
                    if not (isinstance(item, (list, tuple)) and len(item) == 2):
                        h1 = False
                        break
                    if item[0] not in X:
                        h1 = False
                        break
                    if not isinstance(item[1], int):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: f is a map of sets from X to H
    try:
        h2 = all(x in f for x in X) and all(f[x] in H for x in X)
    except Exception:
        h2 = False

    # H_3: For every word r in R, the substitution of f(x) yields the identity element in H
    try:
        h3 = True
        for word in R:
            val = H_id
            for x, p in word:
                fx = f[x]
                if p == 0:
                    continue
                elif p > 0:
                    for _ in range(p):
                        val = H_op(val, fx)
                else:
                    inv_fx = None
                    for y in H:
                        if H_op(fx, y) == H_id and H_op(y, fx) == H_id:
                            inv_fx = y
                            break
                    if inv_fx is None:
                        h3 = False
                        break
                    for _ in range(-p):
                        val = H_op(val, inv_fx)
            if val != H_id:
                h3 = False
                break
    except Exception:
        h3 = False

    # neg_Q: There does NOT exist a unique group homomorphism phi: G -> H such that phi(x) = f(x)
    try:
        neg_q = False
        
        if H_id not in H:
            neg_q = True

        # If f(x) is not invertible in H, it cannot be extended to a group homomorphism
        if not neg_q:
            for x in X:
                fx = f[x]
                invertible = False
                for y in H:
                    try:
                        if H_op(fx, y) == H_id and H_op(y, fx) == H_id:
                            invertible = True
                            break
                    except Exception:
                        pass
                if not invertible:
                    neg_q = True
                    break
                
        # If H is not closed under its operation, it is not a valid codomain for a group homomorphism
        if not neg_q and len(H) <= 100:
            is_closed = True
            for a in H:
                for b in H:
                    try:
                        if H_op(a, b) not in H:
                            is_closed = False
                            break
                    except Exception:
                        is_closed = False
                        break
                if not is_closed: break
            if not is_closed:
                neg_q = True

        # If H is not associative, it is not a valid codomain for a group homomorphism
        if not neg_q and len(H) <= 50:
            is_assoc = True
            for a in H:
                for b in H:
                    for c in H:
                        try:
                            if H_op(H_op(a, b), c) != H_op(a, H_op(b, c)):
                                is_assoc = False
                                break
                        except Exception:
                            is_assoc = False
                            break
                    if not is_assoc: break
                if not is_assoc: break
            if not is_assoc:
                neg_q = True

    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <X | R>",
    "H_2: f is a map of sets from X to H",
    "H_3: For every word r in R, the substitution of f(x) for each x in X in r yields the identity element in H",
    "¬Q: There does not exist a unique group homomorphism phi: G -> H such that phi(x) = f(x) for all x in X"
]

N_HYP = 3
NEG_Q_INDEX = 3