import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness elements
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
    "H_1: M is an R-module",
    "H_2: I and J are ideals of R",
    "H_3: I + J = R",
    "¬Q: M/((I \\cap J)M) is not isomorphic to M/IM \\times M/JM"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = list(witness['R'])
            add_R = witness['add_R']
            mul_R = witness['mul_R']
            M = list(witness['M'])
            add_M = witness['add_M']
            act = witness['act']
            I = list(witness['I'])
            J = list(witness['J'])
        else:
            R = list(witness.R)
            add_R = witness.add_R
            mul_R = witness.mul_R
            M = list(witness.M)
            add_M = witness.add_M
            act = witness.act
            I = list(witness.I)
            J = list(witness.J)
    except Exception:
        return [False, False, False, False]

    try:
        zero_R = None
        for e in R:
            if all(add_R(e, r) == r and add_R(r, e) == r for r in R):
                zero_R = e
                break
        one_R = None
        for e in R:
            if all(mul_R(e, r) == r and mul_R(r, e) == r for r in R):
                one_R = e
                break
        zero_M = None
        for e in M:
            if all(add_M(e, m) == m and add_M(m, e) == m for m in M):
                zero_M = e
                break
    except Exception:
        zero_R = one_R = zero_M = None

    try:
        h1 = True
        if zero_R is None or one_R is None or zero_M is None:
            h1 = False
        if h1:
            # R is a ring
            for a in R:
                for b in R:
                    if add_R(a, b) != add_R(b, a): h1 = False
                    for c in R:
                        if add_R(a, add_R(b, c)) != add_R(add_R(a, b), c): h1 = False
                        if mul_R(a, mul_R(b, c)) != mul_R(mul_R(a, b), c): h1 = False
                        if mul_R(a, add_R(b, c)) != add_R(mul_R(a, b), mul_R(a, c)): h1 = False
                        if mul_R(add_R(a, b), c) != add_R(mul_R(a, c), mul_R(b, c)): h1 = False
            
            # M is an abelian group
            for x in M:
                has_inv = False
                for y in M:
                    if add_M(x, y) == zero_M and add_M(y, x) == zero_M:
                        has_inv = True
                        break
                if not has_inv: h1 = False
                for y in M:
                    if add_M(x, y) != add_M(y, x): h1 = False
                    for z in M:
                        if add_M(x, add_M(y, z)) != add_M(add_M(x, y), z): h1 = False
            
            # M is a left R-module
            for r in R:
                for s in R:
                    for x in M:
                        for y in M:
                            if act(r, add_M(x, y)) != add_M(act(r, x), act(r, y)): h1 = False
                            if act(add_R(r, s), x) != add_M(act(r, x), act(s, x)): h1 = False
                            if act(mul_R(r, s), x) != act(r, act(s, x)): h1 = False
            for x in M:
                if act(one_R, x) != x: h1 = False
    except Exception:
        h1 = False

    try:
        h2 = True
        if zero_R is None or zero_R not in I or zero_R not in J:
            h2 = False
        if h2:
            # I is a left ideal
            for i in I:
                if i not in R: h2 = False
                for j in I:
                    if add_R(i, j) not in I: h2 = False
                for r in R:
                    if mul_R(r, i) not in I: h2 = False
            for i in I:
                has_inv = False
                for j in I:
                    if add_R(i, j) == zero_R:
                        has_inv = True
                        break
                if not has_inv: h2 = False

            # J is a left ideal
            for i in J:
                if i not in R: h2 = False
                for j in J:
                    if add_R(i, j) not in J: h2 = False
                for r in R:
                    if mul_R(r, i) not in J: h2 = False
            for i in J:
                has_inv = False
                for j in J:
                    if add_R(i, j) == zero_R:
                        has_inv = True
                        break
                if not has_inv: h2 = False
    except Exception:
        h2 = False

    try:
        h3 = True
        sums = []
        for i in I:
            for j in J:
                s = add_R(i, j)
                if s not in sums:
                    sums.append(s)
        for r in R:
            if r not in sums:
                h3 = False
                break
    except Exception:
        h3 = False

    try:
        if zero_M is None:
            neg_Q = False
        else:
            I_cap_J = [x for x in I if x in J]
            
            def get_submodule(generators):
                closure = []
                for g in generators:
                    if g not in closure:
                        closure.append(g)
                if zero_M not in closure:
                    closure.append(zero_M)
                while True:
                    added = False
                    n = len(closure)
                    for i in range(n):
                        for j in range(n):
                            val = add_M(closure[i], closure[j])
                            if val not in closure:
                                closure.append(val)
                                added = True
                    for r in R:
                        for i in range(n):
                            val = act(r, closure[i])
                            if val not in closure:
                                closure.append(val)
                                added = True
                    if not added:
                        break
                return closure

            gen_I_cap_J = [act(k, x) for k in I_cap_J for x in M]
            sub_I_cap_J = get_submodule(gen_I_cap_J)
            
            gen_IM = [act(i, x) for i in I for x in M]
            sub_IM = get_submodule(gen_IM)
            
            gen_JM = [act(j, x) for j in J for x in M]
            sub_JM = get_submodule(gen_JM)
            
            size_M = len(M)
            size_I_cap_J_M = len(sub_I_cap_J)
            size_IM = len(sub_IM)
            size_JM = len(sub_JM)
            
            # For finite modules, the natural surjective map is an isomorphism iff sizes match
            if size_I_cap_J_M * size_M == size_IM * size_JM:
                neg_Q = False
            else:
                neg_Q = True
    except Exception:
        neg_Q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]