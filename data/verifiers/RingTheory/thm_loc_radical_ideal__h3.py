import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import ZZ, QQ, Rational, Integer
import itertools
import math

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (n, S_list, I_list) representing Z/nZ, 
    or an object with elements, add, mul, zero, one, S, I.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            n, S_raw, I_raw = witness
            if not isinstance(n, int) or n <= 1:
                return [False, False, False]
            elements = list(range(n))
            add = lambda a, b: (a + b) % n
            mul = lambda a, b: (a * b) % n
            zero = 0
            one = 1
            S_raw = list(S_raw)
            I_raw = list(I_raw)
        else:
            elements = list(witness.elements)
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            S_raw = list(witness.S)
            I_raw = list(witness.I)
    except Exception:
        return [False, False, False]

    try:
        S_list = sorted(S_raw)
    except Exception:
        S_list = S_raw
        
    try:
        I_list = sorted(I_raw)
    except Exception:
        I_list = I_raw

    S_set = set(S_list)
    I_set = set(I_list)
    elements_set = set(elements)

    # H_1: R is a commutative ring
    try:
        h1 = True
        if zero not in elements_set or one not in elements_set:
            h1 = False
        else:
            for a in elements:
                if add(a, zero) != a: h1 = False; break
                if mul(a, one) != a: h1 = False; break
                has_inv = False
                for b in elements:
                    if add(a, b) == zero:
                        has_inv = True; break
                if not has_inv: h1 = False; break
                
                for b in elements:
                    ab_add = add(a, b)
                    ab_mul = mul(a, b)
                    if ab_add not in elements_set or ab_mul not in elements_set: h1 = False; break
                    if ab_add != add(b, a): h1 = False; break
                    if ab_mul != mul(b, a): h1 = False; break
                    for c in elements:
                        if add(ab_add, c) != add(a, add(b, c)): h1 = False; break
                        if mul(ab_mul, c) != mul(a, mul(b, c)): h1 = False; break
                        if mul(a, add(b, c)) != add(ab_mul, mul(a, c)): h1 = False; break
                    if not h1: break
                if not h1: break
    except Exception:
        h1 = False

    # H_2: S is a multiplicatively closed subset of R
    try:
        h2 = True
        if not S_set.issubset(elements_set):
            h2 = False
        else:
            for a in S_list:
                for b in S_list:
                    if mul(a, b) not in S_set:
                        h2 = False
                        break
                if not h2: break
            if one not in S_set:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: The radical of the extended ideal S^{-1}I in S^{-1}R is NOT equal to the extended ideal S^{-1}(\sqrt{I})
    try:
        if not I_set.issubset(elements_set):
            neg_q = False
        else:
            def get_neg(y):
                for z in elements:
                    if add(y, z) == zero:
                        return z
                return y

            def equiv(a, s, b, t):
                at = mul(a, t)
                bs = mul(b, s)
                neg_bs = get_neg(bs)
                diff = add(at, neg_bs)
                for u in S_list:
                    if mul(u, diff) == zero:
                        return True
                return False

            classes = []
            for a in elements:
                for s in S_list:
                    found = False
                    for c in classes:
                        b, t = c[0]
                        if equiv(a, s, b, t):
                            c.append((a, s))
                            found = True
                            break
                    if not found:
                        classes.append([(a, s)])

            def get_class(a, s):
                for k, c in enumerate(classes):
                    if equiv(a, s, c[0][0], c[0][1]):
                        return k
                return 0

            def add_frac(i, j):
                a, s = classes[i][0]
                b, t = classes[j][0]
                num = add(mul(a, t), mul(b, s))
                den = mul(s, t)
                for k, c in enumerate(classes):
                    if equiv(num, den, c[0][0], c[0][1]):
                        return k
                return 0

            def mul_frac(i, j):
                a, s = classes[i][0]
                b, t = classes[j][0]
                num = mul(a, b)
                den = mul(s, t)
                for k, c in enumerate(classes):
                    if equiv(num, den, c[0][0], c[0][1]):
                        return k
                return 0

            def ext(A_list):
                gen = set()
                for a in A_list:
                    gen.add(get_class(a, one))
                
                ideal_elements = set(gen)
                ideal_elements.add(get_class(zero, one))
                
                changed = True
                while changed:
                    new_elements = set(ideal_elements)
                    for x in ideal_elements:
                        for y in ideal_elements:
                            new_elements.add(add_frac(x, y))
                        for r in range(len(classes)):
                            new_elements.add(mul_frac(x, r))
                    if len(new_elements) > len(ideal_elements):
                        ideal_elements = new_elements
                        changed = True
                    else:
                        break
                return ideal_elements

            def rad(A_set):
                rad_elements = set()
                for x in elements:
                    curr = x
                    for _ in range(len(elements)):
                        if curr in A_set:
                            rad_elements.add(x)
                            break
                        curr = mul(curr, x)
                return rad_elements

            def rad_S(J):
                rad_elements = set()
                for x in range(len(classes)):
                    curr = x
                    for _ in range(len(classes)):
                        if curr in J:
                            rad_elements.add(x)
                            break
                        curr = mul_frac(curr, x)
                return rad_elements

            ext_I = ext(I_list)
            rad_ext_I = rad_S(ext_I)
            
            rad_I = rad(I_set)
            ext_rad_I = ext(list(rad_I))
            
            neg_q = (rad_ext_I != ext_rad_I)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The radical of the extended ideal S^{-1}I in S^{-1}R is NOT equal to the extended ideal S^{-1}(\\sqrt{I})"
]

N_HYP = 2
NEG_Q_INDEX = 2