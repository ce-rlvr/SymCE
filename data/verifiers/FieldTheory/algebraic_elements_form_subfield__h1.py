import sympy
import itertools
import math

class MatrixMod:
    def __init__(self, mat, mod):
        self.mat = sympy.Matrix(mat).applyfunc(lambda x: x % mod)
        self.mod = mod
    def __add__(self, other):
        return MatrixMod(self.mat + other.mat, self.mod)
    def __mul__(self, other):
        return MatrixMod(self.mat * other.mat, self.mod)
    def __eq__(self, other):
        if not isinstance(other, MatrixMod):
            return False
        return self.mat == other.mat and self.mod == other.mod
    def __hash__(self):
        return hash((tuple(self.mat), self.mod))

class ModInt:
    def __init__(self, val, mod):
        self.val = val % mod
        self.mod = mod
    def __add__(self, other):
        return ModInt(self.val + other.val, self.mod)
    def __mul__(self, other):
        return ModInt(self.val * other.val, self.mod)
    def __eq__(self, other):
        if not isinstance(other, ModInt):
            return False
        return self.val == other.val and self.mod == other.mod
    def __hash__(self):
        return hash((self.val, self.mod))

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        L, K, A = witness
    except Exception:
        return [False, False]

    def get_zero(lst):
        for z in lst:
            if all(z + x == x for x in lst):
                return z
        return None

    def get_one(lst):
        for e in lst:
            if all(e * x == x and x * e == x for x in lst):
                return e
        return None

    def contains(lst, item):
        return any(x == item for x in lst)

    try:
        zero = get_zero(L)
        one = get_one(L)
        if zero is None or one is None:
            h1 = False
        else:
            h1 = True
            max_deg = 1
            while max_deg < len(L):
                if len(K) ** (max_deg + 1) > 20000:
                    break
                max_deg += 1

            for x in L:
                pows = [one]
                curr = one
                for _ in range(max_deg):
                    curr = curr * x
                    pows.append(curr)

                is_alg = False
                for deg in range(1, max_deg + 1):
                    if is_alg:
                        break
                    for coeffs in itertools.product(K, repeat=deg):
                        for c_d in K:
                            if c_d == zero:
                                continue
                            val = c_d * pows[deg]
                            for c, p in zip(coeffs, pows):
                                val = val + c * p
                            if val == zero:
                                is_alg = True
                                break
                        if is_alg:
                            break

                in_A = contains(A, x)
                if is_alg != in_A:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        zero = get_zero(L)
        one = get_one(L)

        contains_K = all(contains(A, k) for k in K)

        is_field = True
        if zero is None or one is None or zero == one:
            is_field = False
        elif not contains(A, zero) or not contains(A, one):
            is_field = False
        else:
            for a in A:
                if not is_field:
                    break
                for b in A:
                    if not contains(A, a + b):
                        is_field = False
                        break
                    if not contains(A, a * b):
                        is_field = False
                        break
                    if a * b != b * a:
                        is_field = False
                        break

            if is_field:
                for a in A:
                    if a != zero:
                        has_inv = False
                        for b in A:
                            if a * b == one:
                                has_inv = True
                                break
                        if not has_inv:
                            is_field = False
                            break

        Q = contains_K and is_field
        neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is the set of all elements in L that are algebraic over K",
    "¬Q: A is not a subfield of L that contains K"
]

N_HYP = 1
NEG_Q_INDEX = 1