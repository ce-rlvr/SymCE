import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

CONDITION_LABELS = [
    "H_1: \\alpha is an automorphism of G",
    "H_2: S is the set of all elements x \\in G such that \\alpha(x) = x",
    "\\neg Q: S is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def apply_alpha(alpha, x):
    if isinstance(alpha, dict):
        return alpha[x]
    return alpha(x)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                raw_elements, op, alpha, raw_S = witness
            elif len(witness) == 3:
                G, alpha, raw_S = witness
                if hasattr(G, 'generate'):
                    raw_elements = list(G.generate())
                    op = lambda x, y: x * y
                else:
                    return [False, False, False]
            else:
                return [False, False, False]
            
            elements = []
            for e in raw_elements:
                if e not in elements:
                    elements.append(e)
            
            if not elements:
                return [False, False, False]
            
            S = []
            for e in raw_S:
                if e not in S:
                    S.append(e)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: alpha is an automorphism of G
    try:
        mapped = []
        for x in elements:
            y = apply_alpha(alpha, x)
            if y not in mapped:
                mapped.append(y)
        
        is_bijection = len(mapped) == len(elements)
        if is_bijection:
            for x in elements:
                if x not in mapped:
                    is_bijection = False
                    break
        
        preserves_op = True
        if is_bijection:
            for x in elements:
                for y in elements:
                    ax = apply_alpha(alpha, x)
                    ay = apply_alpha(alpha, y)
                    xy = op(x, y)
                    axy = apply_alpha(alpha, xy)
                    if axy != op(ax, ay):
                        preserves_op = False
                        break
                if not preserves_op:
                    break
        
        h1 = is_bijection and preserves_op
    except Exception:
        h1 = False

    # H_2: S is the set of fixed points
    try:
        expected_S = []
        for x in elements:
            ax = apply_alpha(alpha, x)
            if ax == x:
                expected_S.append(x)
        
        h2 = (len(S) == len(expected_S))
        if h2:
            for x in S:
                if x not in expected_S:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: S is NOT a subgroup of G
    try:
        def is_group(subset, operation):
            if not subset:
                return False
            
            # Closure
            for x in subset:
                for y in subset:
                    try:
                        res = operation(x, y)
                        if res not in subset:
                            return False
                    except Exception:
                        return False
            
            # Associativity
            for x in subset:
                for y in subset:
                    for z in subset:
                        try:
                            if operation(x, operation(y, z)) != operation(operation(x, y), z):
                                return False
                        except Exception:
                            return False
            
            # Identity
            identity = None
            for e in subset:
                is_id = True
                for x in subset:
                    try:
                        if operation(e, x) != x or operation(x, e) != x:
                            is_id = False
                            break
                    except Exception:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
            
            if identity is None:
                return False
            
            # Inverses
            for x in subset:
                has_inv = False
                for y in subset:
                    try:
                        if operation(x, y) == identity and operation(y, x) == identity:
                            has_inv = True
                            break
                    except Exception:
                        pass
                if not has_inv:
                    return False
            
            return True

        neg_q = not is_group(S, op)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]