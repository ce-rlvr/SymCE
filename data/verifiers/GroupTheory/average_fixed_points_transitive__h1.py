import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

def get_elements(G):
    elements = []
    if hasattr(G, 'generate'):
        gen = G.generate()
    else:
        gen = iter(G)
    for _ in range(100000):
        try:
            elements.append(next(gen))
        except StopIteration:
            return elements
    return None

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) != 2:
                return [False, False, False]
            G, X_iter = witness
            
            X = []
            try:
                it = iter(X_iter)
                for _ in range(10000):
                    X.append(next(it))
                else:
                    return [False, False, False]
            except StopIteration:
                pass
                
            elements = get_elements(G)
            if elements is None:
                return [False, False, False]
        else:
            G = witness
            elements = get_elements(G)
            if elements is None:
                return [False, False, False]
                
            if hasattr(G, 'degree'):
                X = list(range(G.degree))
            else:
                max_val = -1
                for p in elements:
                    if hasattr(p, 'size') and p.size > 0:
                        max_val = max(max_val, p.size - 1)
                X = list(range(max_val + 1)) if max_val >= 0 else []
    except Exception:
        return [False, False, False]

    # H1: X is a finite set
    try:
        h1 = isinstance(X, list)
    except Exception:
        h1 = False

    # H2: G acts transitively on X
    try:
        if len(X) == 0:
            h2 = True
        else:
            is_closed = True
            for x in X:
                for g in elements:
                    try:
                        nxt = g(x) if hasattr(g, '__call__') else x
                    except Exception:
                        is_closed = False
                        break
                    if nxt not in X:
                        is_closed = False
                        break
                if not is_closed:
                    break
            
            if not is_closed:
                h2 = False
            else:
                orbit = set([X[0]])
                queue = [X[0]]
                while queue:
                    curr = queue.pop(0)
                    for g in elements:
                        try:
                            nxt = g(curr) if hasattr(g, '__call__') else curr
                        except Exception:
                            nxt = curr
                        if nxt not in orbit:
                            orbit.add(nxt)
                            queue.append(nxt)
                h2 = (orbit == set(X))
    except Exception:
        h2 = False

    # neg_Q: sum_{g \in G} |X^g| != |G|
    try:
        sum_fixed = 0
        for g in elements:
            fixed_count = 0
            for x in X:
                try:
                    nxt = g(x) if hasattr(g, '__call__') else x
                except Exception:
                    nxt = None
                if nxt == x:
                    fixed_count += 1
            sum_fixed += fixed_count
            
        neg_q = (sum_fixed != len(elements))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a finite set",
    "H_2: G acts transitively on X",
    "¬Q: \\sum_{g \\in G} |X^g| != |G|"
]

N_HYP = 2
NEG_Q_INDEX = 2