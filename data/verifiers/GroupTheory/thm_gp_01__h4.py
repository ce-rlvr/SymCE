import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup for witness expressions
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

def conditions(witness):
    try:
        G, H, f = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group defined by a presentation
    try:
        h1 = False
        parsed_X = []
        parsed_R = []
        if type(G).__name__ == 'FpGroup':
            h1 = True
            parsed_X = list(G.generators)
            for r in G.relators:
                parsed_R.append(r.array_form)
        elif isinstance(G, (list, tuple)) and len(G) == 2:
            X, R = G
            if isinstance(X, (list, tuple, set)) and isinstance(R, (list, tuple)):
                h1 = True
                parsed_X = list(X)
                for r in R:
                    if not isinstance(r, (list, tuple)):
                        h1 = False
                        break
                    parsed_r = []
                    for term in r:
                        if not (isinstance(term, (list, tuple)) and len(term) == 2 and term[0] in X and isinstance(term[1], int)):
                            h1 = False
                            break
                        parsed_r.append((term[0], term[1]))
                    parsed_R.append(parsed_r)
    except Exception:
        h1 = False

    # H_2: H is a group
    try:
        h2 = isinstance(H, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: f is a map of sets from the generators of G to H
    try:
        h3 = False
        if h1 and h2 and isinstance(f, dict):
            h3 = True
            for x in parsed_X:
                if x not in f:
                    h3 = False
                    break
            if h3:
                for val in f.values():
                    if val not in H:
                        h3 = False
                        break
    except Exception:
        h3 = False

    # ¬Q: f does not extend to a unique group homomorphism from G to H
    # This happens if and only if there is some relator r in G.relators
    # such that f(r) != identity in H.
    try:
        neg_q = False
        if h1 and h2 and h3:
            if hasattr(H, 'identity'):
                H_id = H.identity
            elif list(H.generators):
                H_id = list(H.generators)[0] ** 0
            else:
                H_id = Permutation()
                
            for r in parsed_R:
                res = H_id
                for x, p in r:
                    res = res * (f[x] ** p)
                if res != H_id:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group defined by a presentation",
    "H_2: H is a group",
    "H_3: f is a map of sets from the generators of G to H",
    "¬Q: f does not extend to a unique group homomorphism from G to H"
]

N_HYP = 3
NEG_Q_INDEX = 3