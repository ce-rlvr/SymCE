import itertools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def unique(lst):
    res = []
    for item in lst:
        if item not in res:
            res.append(item)
    return res

def is_subset(sub, sup):
    return all(item in sup for item in sub)

def set_eq(A, B):
    return is_subset(A, B) and is_subset(B, A)

def apply_f(f, val):
    if isinstance(f, dict):
        return f[val]
    return f(val)

def additive_closure(gens, elements, add_func):
    closure = unique(gens)
    queue = list(closure)
    max_size = len(elements)
    while queue:
        curr = queue.pop(0)
        for item in closure:
            try:
                nxt = add_func(curr, item)
            except Exception:
                continue
            if nxt not in closure:
                closure.append(nxt)
                queue.append(nxt)
                if len(closure) >= max_size:
                    return closure
    return closure

def ideal_generated(X, R, add_R, mul_R):
    gens = list(X)
    zero_elements = [z for z in R if all(add_R(z, r) == r for r in R)]
    if zero_elements:
        gens.append(zero_elements[0])
    for item in X:
        for r in R:
            try:
                gens.append(mul_R(r, item))
                gens.append(mul_R(item, r))
                for s in R:
                    gens.append(mul_R(mul_R(r, item), s))
            except Exception:
                pass
    return additive_closure(gens, R, add_R)

def subset_product(A, B, elements, add, mul):
    prods = []
    zero_elements = [z for z in elements if all(add(z, e) == e for e in elements)]
    if zero_elements:
        prods.append(zero_elements[0])
    for a in A:
        for b in B:
            try:
                prods.append(mul(a, b))
            except Exception:
                pass
    return additive_closure(prods, elements, add)

def is_ring(elements, add, mul):
    if not elements: return False
    for a in elements:
        for b in elements:
            try:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
            except Exception:
                return False
    for a in elements:
        for b in elements:
            try:
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
            except Exception:
                return False
    zeros = [z for z in elements if all(add(z, a) == a for a in elements)]
    if not zeros: return False
    zero = zeros[0]
    for a in elements:
        if not any(add(a, b) == zero for b in elements): return False
    return True

def is_ideal(J, R, add_R, mul_R):
    if not J or not is_subset(J, R): return False
    for a in J:
        for b in J:
            try:
                if add_R(a, b) not in J: return False
            except Exception:
                return False
    zeros = [z for z in R if all(add_R(z, a) == a for a in R)]
    if not zeros or zeros[0] not in J: return False
    for a in J:
        if not any(add_R(a, b) == zeros[0] and b in J for b in R): return False
    for r in R:
        for j in J:
            try:
                if mul_R(r, j) not in J: return False
                if mul_R(j, r) not in J: return False
            except Exception:
                return False
    return True

def conditions(witness):
    try:
        R = witness['R']
        S = witness['S']
        add_R = witness['add_R']
        mul_R = witness['mul_R']
        add_S = witness['add_S']
        mul_S = witness['mul_S']
        f = witness['f']
        I = witness['I']
        J = witness['J']
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_ring(R, add_R, mul_R) and is_ring(S, add_S, mul_S)
    except Exception:
        h1 = False

    try:
        h2 = True
        for x in R:
            try:
                fx = apply_f(f, x)
                if fx not in S:
                    h2 = False
                    break
            except Exception:
                h2 = False
                break
        if h2:
            for x in R:
                for y in R:
                    try:
                        if apply_f(f, add_R(x, y)) != add_S(apply_f(f, x), apply_f(f, y)): h2 = False
                        if apply_f(f, mul_R(x, y)) != mul_S(apply_f(f, x), apply_f(f, y)): h2 = False
                    except Exception:
                        h2 = False
            try:
                image = unique([apply_f(f, x) for x in R])
                if not set_eq(image, S): h2 = False
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    try:
        h3 = is_ideal(J, R, add_R, mul_R)
    except Exception:
        h3 = False

    try:
        if not is_subset(I, R):
            neg_q = False
        else:
            prods_R = []
            for i in I:
                for j in J:
                    prods_R.append(mul_R(i, j))
            IJ = ideal_generated(prods_R, R, add_R, mul_R)
            f_IJ = unique([apply_f(f, x) for x in IJ])
            
            f_I = unique([apply_f(f, i) for i in I])
            f_J = unique([apply_f(f, j) for j in J])
            fI_fJ = subset_product(f_I, f_J, S, add_S, mul_S)
            
            neg_q = not set_eq(f_IJ, fI_fJ)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R \\to S is a surjective ring homomorphism",
    "H_3: J is an ideal of R",
    "¬Q: f(IJ) != f(I)f(J)"
]

N_HYP = 3
NEG_Q_INDEX = 3