import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import itertools
import math
import functools

def make_Zn(n):
    elements = list(range(n))
    add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
    return elements, add_table, mul_table

def make_Z2xZ2():
    elements = [0, 1, 2, 3]
    add_table = [
        [0, 1, 2, 3],
        [1, 0, 3, 2],
        [2, 3, 0, 1],
        [3, 2, 1, 0]
    ]
    mul_table = [
        [0, 0, 0, 0],
        [0, 1, 2, 3],
        [0, 2, 2, 0],
        [0, 3, 0, 3]
    ]
    return elements, add_table, mul_table

Z2xZ2 = make_Z2xZ2()

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: I is an ideal of R",
    "¬Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals in S^{-1}R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        elements, add_table, mul_table, S, I, J = witness
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    h1 = True
    try:
        n = len(elements)
        for i in elements:
            for j in elements:
                if add_table[i][j] not in elements: h1 = False
                if mul_table[i][j] not in elements: h1 = False
                if add_table[i][j] != add_table[j][i]: h1 = False
                if mul_table[i][j] != mul_table[j][i]: h1 = False
        for i in elements:
            for j in elements:
                for k in elements:
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: h1 = False
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: h1 = False
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: h1 = False
        zero = None
        for z in elements:
            if all(add_table[a][z] == a for a in elements):
                zero = z
                break
        if zero is None: h1 = False
        one = None
        for o in elements:
            if all(mul_table[a][o] == a for a in elements):
                one = o
                break
        if one is None: h1 = False
        if h1:
            for a in elements:
                has_inv = False
                for b in elements:
                    if add_table[a][b] == zero:
                        has_inv = True
                        break
                if not has_inv: h1 = False
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    h2 = True
    try:
        if not set(S).issubset(set(elements)): h2 = False
        if not S: h2 = False
        for a in S:
            for b in S:
                if mul_table[a][b] not in S: h2 = False
        one_h2 = None
        for o in elements:
            if all(mul_table[a][o] == a for a in elements):
                one_h2 = o
                break
        if one_h2 not in S: h2 = False
    except Exception:
        h2 = False

    # H3: I is an ideal of R
    h3 = True
    try:
        if not set(I).issubset(set(elements)): h3 = False
        if not I: h3 = False
        for a in I:
            for b in I:
                if add_table[a][b] not in I: h3 = False
        for a in I:
            for r in elements:
                if mul_table[r][a] not in I: h3 = False
    except Exception:
        h3 = False

    # neg_Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals
    neg_q = False
    try:
        if not set(J).issubset(set(elements)):
            return [h1, h2, h3, False]
            
        zero_q = None
        for z in elements:
            if all(add_table[a][z] == a for a in elements):
                zero_q = z
                break
        if zero_q is None:
            return [h1, h2, h3, False]

        IJ = set()
        for i in I:
            for j in J:
                IJ.add(mul_table[i][j])

        neg_map = {}
        for a in elements:
            for b in elements:
                if add_table[a][b] == zero_q:
                    neg_map[a] = b
                    break

        def are_equiv(p1, p2):
            r1, s1 = p1
            r2, s2 = p2
            t1 = mul_table[r1][s2]
            t2 = mul_table[r2][s1]
            diff = add_table[t1][neg_map[t2]]
            for u in S:
                if mul_table[u][diff] == zero_q:
                    return True
            return False

        pairs = [(r, s) for r in elements for s in S]
        classes = []
        for p in pairs:
            found = False
            for c in classes:
                if are_equiv(p, c[0]):
                    c.append(p)
                    found = True
                    break
            if not found:
                classes.append([p])

        def loc_set(A):
            res = set()
            for a in A:
                for s in S:
                    for idx, c in enumerate(classes):
                        if are_equiv((a, s), c[0]):
                            res.add(idx)
                            break
            return res

        S_inv_IJ = loc_set(IJ)
        S_inv_I = loc_set(I)
        S_inv_J = loc_set(J)

        prod_S_inv = set()
        for c1 in S_inv_I:
            for c2 in S_inv_J:
                r1, s1 = classes[c1][0]
                r2, s2 = classes[c2][0]
                r = mul_table[r1][r2]
                s = mul_table[s1][s2]
                for idx, c in enumerate(classes):
                    if are_equiv((r, s), c[0]):
                        prod_S_inv.add(idx)
                        break

        def is_ideal(X):
            if not X: return False
            for x in X:
                for y in X:
                    r1, s1 = classes[x][0]
                    r2, s2 = classes[y][0]
                    r = add_table[mul_table[r1][s2]][mul_table[r2][s1]]
                    s = mul_table[s1][s2]
                    sum_idx = None
                    for idx, c in enumerate(classes):
                        if are_equiv((r, s), c[0]):
                            sum_idx = idx
                            break
                    if sum_idx not in X:
                        return False
            for x in X:
                for r_idx in range(len(classes)):
                    r1, s1 = classes[x][0]
                    r2, s2 = classes[r_idx][0]
                    r = mul_table[r1][r2]
                    s = mul_table[s1][s2]
                    mul_idx = None
                    for idx, c in enumerate(classes):
                        if are_equiv((r, s), c[0]):
                            mul_idx = idx
                            break
                    if mul_idx not in X:
                        return False
            return True

        ideal_1 = is_ideal(S_inv_IJ)
        ideal_2 = is_ideal(prod_S_inv)

        if not ideal_1 or not ideal_2 or S_inv_IJ != prod_S_inv:
            neg_q = True

    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]