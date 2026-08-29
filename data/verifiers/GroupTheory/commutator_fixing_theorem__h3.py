import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
    Given a witness, checks the hypotheses and the negated conclusion.
    The witness can be a tuple (G, g, h, x) or (G, X, g, h, x), or a dict.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            g = witness.get('g')
            h = witness.get('h')
            x = witness.get('x')
        elif len(witness) == 4:
            G, g, h, x = witness
        elif len(witness) == 5:
            G, X, g, h, x = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    def check_fixed(elem, pt):
        # Try function application (e.g., Permutation acting on an integer)
        try:
            if elem(pt) == pt:
                return True
        except Exception:
            pass
        
        # Try multiplication (e.g., Matrix acting on a vector)
        try:
            if elem * pt == pt:
                return True
        except Exception:
            pass

        # Try set-wise action if pt is a collection
        if isinstance(pt, (set, frozenset, list, tuple)):
            try:
                if type(pt)(elem(i) for i in pt) == pt:
                    return True
            except Exception:
                pass
            try:
                if type(pt)(elem * i for i in pt) == pt:
                    return True
            except Exception:
                pass

        return False

    # H1: G is a group acting on a set X
    try:
        h1 = hasattr(G, 'is_group') or hasattr(G, '__contains__') or isinstance(G, (list, set, tuple))
    except Exception:
        h1 = False

    # H2: g and h are elements of G
    try:
        h2 = bool(g in G and h in G)
    except Exception:
        h2 = False

    # H3: x is fixed by g
    try:
        h3 = bool(check_fixed(g, x))
    except Exception:
        h3 = False

    # H4: x is fixed by h
    try:
        h4 = bool(check_fixed(h, x))
    except Exception:
        h4 = False

    # neg_Q: x is not fixed by the commutator [g, h] = g^{-1}h^{-1}gh
    try:
        comm = (g**-1) * (h**-1) * g * h
        neg_q = not bool(check_fixed(comm, x))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = ["H_1: G is a group acting on a set X", "H_2: g and h are elements of G", "H_3: x is fixed by g", "H_4: x is fixed by h", "¬Q: x is not fixed by the commutator of g and h"]

N_HYP = 4
NEG_Q_INDEX = 4