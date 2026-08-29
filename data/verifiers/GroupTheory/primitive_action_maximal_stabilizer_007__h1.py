import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: X is a set with at least two elements",
    "H_2: G acts transitively on X",
    "H_3: x is an element of X",
    "¬Q: The action of G on X is primitive XOR the stabilizer subgroup G_x is a maximal subgroup of G"
]

def conditions(witness):
    # Default extraction
    G = None
    X = None
    x = None

    if isinstance(witness, dict):
        G = witness.get('G')
        X = witness.get('X')
        x = witness.get('x')
    elif hasattr(witness, 'G') and hasattr(witness, 'X') and hasattr(witness, 'x'):
        G = witness.G
        X = witness.X
        x = witness.x
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            G, X, x = witness
        elif len(witness) == 2:
            G, x = witness
            try:
                X = list(range(G.degree))
            except Exception:
                pass
    else:
        G = witness
        try:
            X = list(range(G.degree))
            x = 0
        except Exception:
            pass

    # H1: X has at least two elements
    try:
        h1 = len(X) >= 2
    except Exception:
        h1 = False

    # H2: G acts transitively on X
    try:
        if isinstance(witness, dict) and 'acts_transitively' in witness:
            h2 = bool(witness['acts_transitively'])
        elif hasattr(witness, 'acts_transitively'):
            attr = witness.acts_transitively
            h2 = bool(attr() if callable(attr) else attr)
        elif hasattr(G, 'is_transitive'):
            attr = G.is_transitive
            h2 = bool(attr() if callable(attr) else attr)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = x in X
    except Exception:
        h3 = False

    # Conclusion: primitive iff G_x is maximal
    try:
        if isinstance(witness, dict) and 'is_primitive' in witness:
            prim = bool(witness['is_primitive'])
        elif hasattr(witness, 'is_primitive'):
            attr = witness.is_primitive
            prim = bool(attr() if callable(attr) else attr)
        elif hasattr(G, 'is_primitive'):
            attr = G.is_primitive
            prim = bool(attr() if callable(attr) else attr)
        else:
            prim = False

        if isinstance(witness, dict) and 'stabilizer_is_maximal' in witness:
            max_sub = bool(witness['stabilizer_is_maximal'])
        elif hasattr(witness, 'stabilizer_is_maximal'):
            attr = witness.stabilizer_is_maximal
            max_sub = bool(attr() if callable(attr) else attr)
        else:
            stab = G.stabilizer(x)
            if stab.order() == G.order():
                max_sub = False
            else:
                max_sub = True
                for g in G.generate():
                    if g not in stab:
                        K = type(G)(*(list(stab.generators) + [g]))
                        if K.order() != G.order():
                            max_sub = False
                            break
        
        q = (prim == max_sub)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]