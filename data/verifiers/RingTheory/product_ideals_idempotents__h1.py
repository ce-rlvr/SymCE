import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools
import math
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

def conditions(witness) -> list[bool]:
    try:
        R, e, f, I, J = witness
    except Exception:
        return [False] * 5

    def in_list(lst, elem):
        for x in lst:
            try:
                if bool(x == elem):
                    return True
            except Exception:
                pass
        return False

    def remove_duplicates(lst):
        res = []
        for x in lst:
            if not in_list(res, x):
                res.append(x)
        return res

    def set_eq(A, B):
        try:
            return set(A) == set(B)
        except TypeError:
            for a in A:
                if not in_list(B, a): return False
            for b in B:
                if not in_list(A, b): return False
            return True

    def is_ideal(K, R):
        if not K: return False
        try:
            K_set = set(K)
            R_set = set(R)
            if not K_set.issubset(R_set): return False
            for a in K_set:
                for b in K_set:
                    if (a + b) not in K_set: return False
            for a in K_set:
                for r in R_set:
                    if (r * a) not in K_set: return False
                    if (a * r) not in K_set: return False
            return True
        except TypeError:
            for x in K:
                if not in_list(R, x): return False
            for a in K:
                for b in K:
                    if not in_list(K, a + b): return False
            for a in K:
                for r in R:
                    if not in_list(K, r * a): return False
                    if not in_list(K, a * r): return False
            return True

    def principal_ideal(x, R):
        gens = [x]
        for r in R:
            gens.append(r * x)
            gens.append(x * r)
            for r2 in R:
                gens.append(r * x * r2)
        
        try:
            closure_set = set(gens)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for a in closure_set:
                    for b in closure_set:
                        c = a + b
                        if c not in closure_set and c not in new_elements:
                            new_elements.add(c)
                if new_elements:
                    closure_set.update(new_elements)
                    changed = True
                    if len(closure_set) > len(R):
                        break
            return list(closure_set)
        except TypeError:
            closure = remove_duplicates(gens)
            changed = True
            while changed:
                changed = False
                new_elements = []
                for a in closure:
                    for b in closure:
                        c = a + b
                        if not in_list(closure, c) and not in_list(new_elements, c):
                            new_elements.append(c)
                if new_elements:
                    closure.extend(new_elements)
                    changed = True
                    if len(closure) > len(R):
                        break
            return closure

    def product_ideal(I, J, R):
        gens = []
        for x in I:
            for y in J:
                gens.append(x * y)
        
        try:
            closure_set = set(gens)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for a in closure_set:
                    for b in closure_set:
                        c = a + b
                        if c not in closure_set and c not in new_elements:
                            new_elements.add(c)
                if new_elements:
                    closure_set.update(new_elements)
                    changed = True
                    if len(closure_set) > len(R):
                        break
            return list(closure_set)
        except TypeError:
            closure = remove_duplicates(gens)
            changed = True
            while changed:
                changed = False
                new_elements = []
                for a in closure:
                    for b in closure:
                        c = a + b
                        if not in_list(closure, c) and not in_list(new_elements, c):
                            new_elements.append(c)
                if new_elements:
                    closure.extend(new_elements)
                    changed = True
                    if len(closure) > len(R):
                        break
            return closure

    # H1: e is an idempotent element of R
    try:
        h1 = in_list(R, e) and bool(e * e == e)
    except Exception:
        h1 = False

    # H2: f is an idempotent element of R
    try:
        h2 = in_list(R, f) and bool(f * f == f)
    except Exception:
        h2 = False

    # H3: I is the principal ideal generated by e
    try:
        PI_e = principal_ideal(e, R)
        h3 = is_ideal(I, R) and set_eq(I, PI_e)
    except Exception:
        h3 = False

    # H4: J is the principal ideal generated by f
    try:
        PI_f = principal_ideal(f, R)
        h4 = is_ideal(J, R) and set_eq(J, PI_f)
    except Exception:
        h4 = False

    # neg_Q: The product ideal IJ is not the principal ideal generated by the idempotent element ef
    try:
        ef = e * f
        ef_is_idempotent = bool(ef * ef == ef)
        IJ = product_ideal(I, J, R)
        PI_ef = principal_ideal(ef, R)
        
        q = ef_is_idempotent and set_eq(IJ, PI_ef)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: e is an idempotent element of R",
    "H_2: f is an idempotent element of R",
    "H_3: I is the principal ideal generated by e",
    "H_4: J is the principal ideal generated by f",
    "¬Q: The product ideal IJ is not the principal ideal generated by the idempotent element ef"
]

N_HYP = 4
NEG_Q_INDEX = 4