import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def apply_f(f, x):
    if callable(f):
        return f(x)
    elif isinstance(f, dict):
        return f[x]
    else:
        return f[x]

def conditions(witness):
    try:
        if len(witness) == 3:
            G, alpha, beta = witness
            F_alpha_provided = False
        elif len(witness) == 4:
            G, alpha, beta, F_alpha = witness
            F_alpha_provided = True
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        elements = []
        iterable = G.elements if hasattr(G, 'elements') else G
        for i, el in enumerate(iterable):
            if i > 500:
                return [False, False, False, False]
            elements.append(el)
        if not elements:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: alpha and beta are automorphisms of G
    h1_ok = False
    try:
        def is_auto(f):
            mapped = []
            for x in elements:
                fx = apply_f(f, x)
                if fx not in elements:
                    return False
                mapped.append(fx)
            
            # Check injectivity
            for i in range(len(mapped)):
                for j in range(i + 1, len(mapped)):
                    if mapped[i] == mapped[j]:
                        return False
                        
            # Check homomorphism property
            for x in elements:
                for y in elements:
                    fx = apply_f(f, x)
                    fy = apply_f(f, y)
                    fxy = apply_f(f, x * y)
                    if fxy != fx * fy:
                        return False
            return True
            
        h1_ok = is_auto(alpha) and is_auto(beta)
    except Exception:
        h1_ok = False

    # H2: alpha(beta(x)) = beta(alpha(x)) for all x in G
    h2_ok = False
    try:
        h2_ok = True
        for x in elements:
            ax = apply_f(alpha, x)
            bx = apply_f(beta, x)
            abx = apply_f(alpha, bx)
            bax = apply_f(beta, ax)
            if abx != bax:
                h2_ok = False
                break
    except Exception:
        h2_ok = False

    # H3: F_alpha is the set of all x in G such that alpha(x) = x
    h3_ok = False
    try:
        expected_F = []
        for x in elements:
            if apply_f(alpha, x) == x:
                expected_F.append(x)
        
        if F_alpha_provided:
            h3_ok = True
            for x in F_alpha:
                if x not in expected_F:
                    h3_ok = False
                    break
            for x in expected_F:
                if x not in F_alpha:
                    h3_ok = False
                    break
        else:
            F_alpha = expected_F
            h3_ok = True
    except Exception:
        h3_ok = False

    # neg_Q: For every y in F_alpha, beta(y) in F_alpha (Conclusion must FAIL)
    neg_q = False
    try:
        conclusion_holds = True
        for y in F_alpha:
            by = apply_f(beta, y)
            if by not in F_alpha:
                conclusion_holds = False
                break
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: alpha and beta are automorphisms of G",
    "H_2: alpha(beta(x)) = beta(alpha(x)) for all x in G",
    "H_3: F_alpha is the set of all x in G such that alpha(x) = x",
    "¬Q: There exists y in F_alpha such that beta(y) is not in F_alpha"
]

N_HYP = 3
NEG_Q_INDEX = 3