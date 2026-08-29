import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: J is an ideal of R",
    "¬Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals in S^{-1}R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    if not isinstance(witness, dict):
        return [False, False, False, False]
    if not all(k in witness for k in ['n', 'add', 'mul', 'S', 'I', 'J']):
        return [False, False, False, False]
        
    try:
        n = witness['n']
        add_obj = witness['add']
        mul_obj = witness['mul']
        S = witness['S']
        I = witness['I']
        J = witness['J']
        
        if callable(add_obj):
            add = add_obj
        else:
            add = lambda a, b: add_obj[a][b]
            
        if callable(mul_obj):
            mul = mul_obj
        else:
            mul = lambda a, b: mul_obj[a][b]
            
        def check_commutative_ring():
            if n <= 0: return False
            elements = list(range(n))
            for a in elements:
                for b in elements:
                    if add(a, b) not in elements: return False
                    if mul(a, b) not in elements: return False
                    if add(a, b) != add(b, a): return False
                    if mul(a, b) != mul(b, a): return False
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
            zero = None
            for a in elements:
                if all(add(a, b) == b for b in elements):
                    zero = a
                    break
            if zero is None: return False
            for a in elements:
                if not any(add(a, b) == zero for b in elements): return False
            one = None
            for a in elements:
                if all(mul(a, b) == b for b in elements):
                    one = a
                    break
            if one is None: return False
            return True
            
        h1 = check_commutative_ring()
    except Exception:
        h1 = False

    try:
        def check_S():
            if not S: return False
            elements = list(range(n))
            for s in S:
                if s not in elements: return False
            for a in S:
                for b in S:
                    if mul(a, b) not in S: return False
            return True
        h2 = check_S()
    except Exception:
        h2 = False

    try:
        def check_ideal():
            if not J: return False
            elements = list(range(n))
            for j in J:
                if j not in elements: return False
            for a in J:
                for b in J:
                    if add(a, b) not in J: return False
            for j in J:
                for r in elements:
                    if mul(j, r) not in J: return False
            zero = None
            for a in elements:
                if all(add(a, b) == b for b in elements):
                    zero = a
                    break
            if zero not in J: return False
            for j in J:
                neg_j = None
                for x in elements:
                    if add(j, x) == zero:
                        neg_j = x
                        break
                if neg_j not in J: return False
            return True
        h3 = check_ideal()
    except Exception:
        h3 = False

    try:
        def check_neg_Q():
            elements = list(range(n))
            zero = None
            for a in elements:
                if all(add(a, b) == b for b in elements):
                    zero = a
                    break
                    
            def neg(b):
                for x in elements:
                    if add(b, x) == zero:
                        return x
                return None

            pairs = [(r, s) for r in elements for s in S]
            
            def eq(p1, p2):
                r1, s1 = p1
                r2, s2 = p2
                diff = add(mul(r1, s2), neg(mul(r2, s1)))
                for u in S:
                    if mul(u, diff) == zero:
                        return True
                return False

            classes = []
            for p in pairs:
                found = False
                for c in classes:
                    if eq(p, c[0]):
                        c.append(p)
                        found = True
                        break
                if not found:
                    classes.append([p])
                    
            def localize_subset(X):
                res = set()
                for x in X:
                    for s in S:
                        p = (x, s)
                        for i, c in enumerate(classes):
                            if eq(p, c[0]):
                                res.add(i)
                                break
                return res

            def is_ideal(subset_indices):
                if not subset_indices:
                    return False
                zero_class = None
                for i, c in enumerate(classes):
                    if eq((zero, S[0]), c[0]):
                        zero_class = i
                        break
                if zero_class not in subset_indices:
                    return False
                    
                for i in subset_indices:
                    for j in subset_indices:
                        p1 = classes[i][0]
                        p2 = classes[j][0]
                        sum_p = (add(mul(p1[0], p2[1]), mul(p2[0], p1[1])), mul(p1[1], p2[1]))
                        sum_class = None
                        for k, c in enumerate(classes):
                            if eq(sum_p, c[0]):
                                sum_class = k
                                break
                        if sum_class not in subset_indices:
                            return False
                            
                for i in subset_indices:
                    for k in range(len(classes)):
                        p1 = classes[i][0]
                        p2 = classes[k][0]
                        prod_p = (mul(p1[0], p2[0]), mul(p1[1], p2[1]))
                        prod_class = None
                        for m, c in enumerate(classes):
                            if eq(prod_p, c[0]):
                                prod_class = m
                                break
                        if prod_class not in subset_indices:
                            return False
                return True

            def ideal_product(A_indices, B_indices):
                prods = set()
                for i in A_indices:
                    for j in B_indices:
                        p1 = classes[i][0]
                        p2 = classes[j][0]
                        prod_p = (mul(p1[0], p2[0]), mul(p1[1], p2[1]))
                        for k, c in enumerate(classes):
                            if eq(prod_p, c[0]):
                                prods.add(k)
                                break
                gen = set()
                for p in prods:
                    for k in range(len(classes)):
                        p1 = classes[p][0]
                        p2 = classes[k][0]
                        prod_p = (mul(p1[0], p2[0]), mul(p1[1], p2[1]))
                        for m, c in enumerate(classes):
                            if eq(prod_p, c[0]):
                                gen.add(m)
                                break
                closure = set(gen)
                added = True
                while added:
                    added = False
                    new_elems = set()
                    for a in closure:
                        for b in closure:
                            p1 = classes[a][0]
                            p2 = classes[b][0]
                            sum_p = (add(mul(p1[0], p2[1]), mul(p2[0], p1[1])), mul(p1[1], p2[1]))
                            for k, c in enumerate(classes):
                                if eq(sum_p, c[0]):
                                    if k not in closure:
                                        new_elems.add(k)
                                    break
                    if new_elems:
                        closure.update(new_elems)
                        added = True
                return closure

            S_inv_I = localize_subset(I)
            S_inv_J = localize_subset(J)
            
            prods = set()
            for i in I:
                for j in J:
                    prods.add(mul(i, j))
                    
            closure = set(prods)
            added = True
            while added:
                added = False
                new_elems = set()
                for a in closure:
                    for b in closure:
                        s_val = add(a, b)
                        if s_val not in closure:
                            new_elems.add(s_val)
                if new_elems:
                    closure.update(new_elems)
                    added = True
                    
            S_inv_IJ = localize_subset(closure)
            
            if not is_ideal(S_inv_I): return True
            if not is_ideal(S_inv_J): return True
            if not is_ideal(S_inv_IJ): return True
            
            prod_ideal = ideal_product(S_inv_I, S_inv_J)
            
            if S_inv_IJ != prod_ideal: return True
            
            return False
            
        neg_q = check_neg_Q()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]