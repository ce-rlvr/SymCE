import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class ZmodElement:
    def __init__(self, val, n):
        self.val = val % n
        self.n = n
    def __add__(self, other):
        if isinstance(other, ZmodElement) and self.n == other.n:
            return ZmodElement((self.val + other.val) % self.n, self.n)
        return NotImplemented
    def __mul__(self, other):
        if isinstance(other, ZmodElement) and self.n == other.n:
            return ZmodElement((self.val * other.val) % self.n, self.n)
        return NotImplemented
    def __eq__(self, other):
        if isinstance(other, ZmodElement):
            return self.val == other.val and self.n == other.n
        return False
    def __hash__(self):
        return hash((self.val, self.n))
    def __repr__(self):
        return f"{self.val} mod {self.n}"

Z2 = [ZmodElement(i, 2) for i in range(2)]
Z3 = [ZmodElement(i, 3) for i in range(3)]
Z4 = [ZmodElement(i, 4) for i in range(4)]
Z6 = [ZmodElement(i, 6) for i in range(6)]
Z8 = [ZmodElement(i, 8) for i in range(8)]
Z9 = [ZmodElement(i, 9) for i in range(9)]

def check_ring(R_elements, add_func, mul_func):
    n = len(R_elements)
    if n == 0: return False, None, None
    
    def eq(a, b):
        try: return bool(a == b)
        except: return False

    # Find zero
    zero = None
    for z in R_elements:
        is_zero = True
        for a in R_elements:
            try:
                if not eq(add_func(a, z), a) or not eq(add_func(z, a), a):
                    is_zero = False
                    break
            except:
                is_zero = False
                break
        if is_zero:
            zero = z
            break
    if zero is None: return False, None, None

    # Check additive inverses and closure
    for a in R_elements:
        has_inv = False
        for b in R_elements:
            try:
                s1 = add_func(a, b)
                s2 = add_func(b, a)
                if not any(eq(s1, x) for x in R_elements): return False, None, None
                if not eq(s1, s2): return False, None, None
                if eq(s1, zero):
                    has_inv = True
            except:
                return False, None, None
        if not has_inv: return False, None, None

    # Check associativity of addition
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                try:
                    if not eq(add_func(add_func(a, b), c), add_func(a, add_func(b, c))):
                        return False, None, None
                except:
                    return False, None, None

    # Find one
    one = None
    for o in R_elements:
        is_one = True
        for a in R_elements:
            try:
                if not eq(mul_func(a, o), a) or not eq(mul_func(o, a), a):
                    is_one = False
                    break
            except:
                is_one = False
                break
        if is_one:
            one = o
            break
    if one is None or eq(one, zero): return False, None, None

    # Check multiplication closure, commutativity, associativity
    for a in R_elements:
        for b in R_elements:
            try:
                p1 = mul_func(a, b)
                p2 = mul_func(b, a)
                if not any(eq(p1, x) for x in R_elements): return False, None, None
                if not eq(p1, p2): return False, None, None
            except:
                return False, None, None
            for c in R_elements:
                try:
                    if not eq(mul_func(mul_func(a, b), c), mul_func(a, mul_func(b, c))):
                        return False, None, None
                except:
                    return False, None, None

    # Check distributivity
    for a in R_elements:
        for b in R_elements:
            for c in R_elements:
                try:
                    lhs = mul_func(a, add_func(b, c))
                    rhs = add_func(mul_func(a, b), mul_func(a, c))
                    if not eq(lhs, rhs): return False, None, None
                except:
                    return False, None, None

    return True, zero, one

def check_local(R_elements, add_func, mul_func, one):
    def eq(a, b):
        try: return bool(a == b)
        except: return False

    units = []
    non_units = []
    for a in R_elements:
        is_unit = False
        for b in R_elements:
            try:
                if eq(mul_func(a, b), one):
                    is_unit = True
                    break
            except:
                pass
        if is_unit:
            units.append(a)
        else:
            non_units.append(a)

    # Non-units must be closed under addition
    for a in non_units:
        for b in non_units:
            try:
                s = add_func(a, b)
                if not any(eq(s, nu) for nu in non_units):
                    return False
            except:
                return False
    return True

def is_subset(R_elements, subset):
    def eq(a, b):
        try: return bool(a == b)
        except: return False
    for s in subset:
        if not any(eq(s, r) for r in R_elements):
            return False
    return True

def check_sum_equals_R(R_elements, add_func, I, J):
    def eq(a, b):
        try: return bool(a == b)
        except: return False

    sum_set = []
    for i in I:
        for j in J:
            try:
                s = add_func(i, j)
                if not any(eq(s, x) for x in sum_set):
                    sum_set.append(s)
            except:
                pass

    for r in R_elements:
        if not any(eq(r, s) for s in sum_set):
            return False
    return True

def check_not_equal_R(R_elements, subset):
    def eq(a, b):
        try: return bool(a == b)
        except: return False

    for r in R_elements:
        if not any(eq(r, s) for s in subset):
            return True
    return False

def conditions(witness):
    try:
        if len(witness) == 5:
            n, add_table, mul_table, I_idx, J_idx = witness
            R_elements = list(range(n))
            add_func = lambda x, y: add_table[x][y]
            mul_func = lambda x, y: mul_table[x][y]
            I = I_idx
            J = J_idx
        elif len(witness) == 4:
            add_table, mul_table, I_idx, J_idx = witness
            n = len(add_table)
            R_elements = list(range(n))
            add_func = lambda x, y: add_table[x][y]
            mul_func = lambda x, y: mul_table[x][y]
            I = I_idx
            J = J_idx
        elif len(witness) == 3:
            R, I, J = witness
            R_elements = list(R)
            if len(R_elements) > 100:
                return [False, False, False]
            add_func = lambda x, y: x + y
            mul_func = lambda x, y: x * y
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a commutative local ring
    h1_ok = False
    try:
        is_ring, zero, one = check_ring(R_elements, add_func, mul_func)
        if is_ring:
            h1_ok = check_local(R_elements, add_func, mul_func, one)
    except Exception:
        h1_ok = False

    # H2: I + J = R
    h2_ok = False
    try:
        if is_subset(R_elements, I) and is_subset(R_elements, J):
            h2_ok = check_sum_equals_R(R_elements, add_func, I, J)
    except Exception:
        h2_ok = False

    # neg_Q: I != R and J != R
    neg_q_ok = False
    try:
        neg_q_ok = check_not_equal_R(R_elements, I) and check_not_equal_R(R_elements, J)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring",
    "H_2: I + J = R",
    "¬Q: I != R and J != R"
]
N_HYP = 2
NEG_Q_INDEX = 2