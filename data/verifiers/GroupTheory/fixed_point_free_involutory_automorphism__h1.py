import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

CONDITION_LABELS = [
    "H_1: alpha is an automorphism of G",
    "H_2: alpha(alpha(x)) = x for all x in G",
    "H_3: For all x in G, alpha(x) = x implies x = e",
    "¬Q: G is not abelian or alpha(x) != x^-1 for some x in G"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G_obj, alpha = witness
                elements = getattr(G_obj, 'elements', G_obj)
                if callable(elements):
                    elements = elements()
                identity = getattr(G_obj, 'identity', None)
                mul = getattr(G_obj, 'mul', lambda a, b: a * b)
                inv = getattr(G_obj, 'inv', lambda a: a**-1)
            elif len(witness) == 3:
                elements, mul, alpha = witness
                if callable(elements):
                    elements = elements()
                identity = None
                inv = lambda a: a**-1
            elif len(witness) == 5:
                elements, identity, mul, inv, alpha = witness
                if callable(elements):
                    elements = elements()
            else:
                return [False, False, False, False]
        else:
            elements = witness.elements
            if callable(elements):
                elements = elements()
            alpha = witness.alpha
            mul = getattr(witness, 'mul', lambda a, b: a * b)
            inv = getattr(witness, 'inv', lambda a: a**-1)
            identity = getattr(witness, 'identity', None)
            
        elements = list(elements)
        
        if isinstance(alpha, dict):
            alpha_func = lambda x: alpha[x]
        else:
            alpha_func = alpha
            
        if identity is None:
            for e in elements:
                is_id = True
                for x in elements:
                    try:
                        if mul(e, x) != x or mul(x, e) != x:
                            is_id = False
                            break
                    except Exception:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
    except Exception:
        return [False, False, False, False]

    # H1: alpha is an automorphism of G
    h1 = False
    try:
        is_homo = True
        mapped = []
        for x in elements:
            mapped.append(alpha_func(x))
            for y in elements:
                xy = mul(x, y)
                if alpha_func(xy) != mul(alpha_func(x), alpha_func(y)):
                    is_homo = False
                    break
            if not is_homo:
                break
        if is_homo:
            is_inj = True
            for i in range(len(mapped)):
                for j in range(i + 1, len(mapped)):
                    if mapped[i] == mapped[j]:
                        is_inj = False
                        break
                if not is_inj:
                    break
            h1 = is_inj
    except Exception:
        h1 = False

    # H2: alpha(alpha(x)) = x for all x in G
    h2 = False
    try:
        h2_ok = True
        for x in elements:
            if alpha_func(alpha_func(x)) != x:
                h2_ok = False
                break
        h2 = h2_ok
    except Exception:
        h2 = False

    # H3: For all x in G, alpha(x) = x implies x = e
    h3 = False
    try:
        h3_ok = True
        for x in elements:
            if alpha_func(x) == x:
                if x != identity:
                    h3_ok = False
                    break
        h3 = h3_ok
    except Exception:
        h3 = False

    # neg_Q: G is not abelian OR there exists x such that alpha(x) != x^-1
    neg_q = False
    try:
        is_abelian = True
        for x in elements:
            for y in elements:
                if mul(x, y) != mul(y, x):
                    is_abelian = False
                    break
            if not is_abelian:
                break
        if not is_abelian:
            neg_q = True
    except Exception:
        pass

    if not neg_q:
        try:
            inverts_all = True
            for x in elements:
                if alpha_func(x) != inv(x):
                    inverts_all = False
                    break
            if not inverts_all:
                neg_q = True
        except Exception:
            pass

    return [h1, h2, h3, neg_q]