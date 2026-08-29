import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the group G and the group C.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            C = witness.get('C')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, C = witness
            elif len(witness) == 3:
                _, G, C = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: X is a set
    # In SymPy, a PermutationGroup implicitly defines the set X = {0, 1, ..., degree-1}
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a subgroup of the symmetric group Sym(X)
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False

    # H_3: G acts transitively on X
    try:
        trans = G.is_transitive
        h3 = bool(trans() if callable(trans) else trans)
    except Exception:
        h3 = False

    # ¬Q: C does NOT act semi-regularly on X
    # Semi-regular means: for any c in C, if c has a fixed point in X, then c is the identity on X.
    # Negation: there exists c in C such that c has a fixed point in X AND c is not the identity on X.
    try:
        degree = G.degree
        neg_q = False
        elements = C.elements if hasattr(C, 'elements') else C
        
        for c in elements:
            is_identity_on_X = True
            has_fixed_point_on_X = False
            
            for x in range(degree):
                try:
                    cx = c(x)
                except TypeError:
                    # Fallback if calling the permutation is not supported
                    cx = c.array_form[x] if x < c.size else x
                
                if cx == x:
                    has_fixed_point_on_X = True
                else:
                    is_identity_on_X = False
            
            if has_fixed_point_on_X and not is_identity_on_X:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G is a subgroup of the symmetric group Sym(X)",
    "H_3: G acts transitively on X",
    "¬Q: C does not act semi-regularly on X"
]

N_HYP = 3
NEG_Q_INDEX = 3