import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import itertools
import math
import functools

# Standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

class ModInt:
    """Helper class for elements of Z_n"""
    def __init__(self, val, mod):
        self.val = val % mod
        self.mod = mod
    def __add__(self, other):
        return ModInt(self.val + other.val, self.mod)
    def __mul__(self, other):
        return ModInt(self.val * other.val, self.mod)
    def __neg__(self):
        return ModInt(-self.val, self.mod)
    def __sub__(self, other):
        return ModInt(self.val - other.val, self.mod)
    def __eq__(self, other):
        if not isinstance(other, ModInt):
            return False
        return self.val == other.val and self.mod == other.mod
    def __hash__(self):
        return hash((self.val, self.mod))
    def __repr__(self):
        return f"{self.val} mod {self.mod}"

class ModMatrix:
    """Helper class for matrices over Z_n"""
    def __init__(self, mat, mod):
        self.mat = [[x % mod for x in row] for row in mat]
        self.mod = mod
        self.rows = len(mat)
        self.cols = len(mat[0]) if self.rows > 0 else 0

    def __add__(self, other):
        res = [[(self.mat[i][j] + other.mat[i][j]) % self.mod for j in range(self.cols)] for i in range(self.rows)]
        return ModMatrix(res, self.mod)

    def __mul__(self, other):
        res = [[0]*other.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(other.cols):
                s = 0
                for k in range(self.cols):
                    s += self.mat[i][k] * other.mat[k][j]
                res[i][j] = s % self.mod
        return ModMatrix(res, self.mod)

    def __eq__(self, other):
        if not isinstance(other, ModMatrix):
            return False
        return self.mod == other.mod and self.mat == other.mat

    def __hash__(self):
        return hash((tuple(tuple(row) for row in self.mat), self.mod))

    def __repr__(self):
        return f"ModMatrix({self.mat}, {self.mod})"

def conditions(witness) -> list[bool]:
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False, False]
        
    def unique_list(lst):
        res = []
        for x in lst:
            if x not in res:
                res.append(x)
        return res

    def is_add_closed(lst):
        for a in lst:
            for b in lst:
                if (a + b) not in lst:
                    return False
        return True

    def is_mul_closed(lst):
        for a in lst:
            for b in lst:
                if (a * b) not in lst:
                    return False
        return True

    def is_subset(sub, sup):
        for x in sub:
            if x not in sup:
                return False
        return True

    def list_eq(l1, l2):
        return is_subset(l1, l2) and is_subset(l2, l1)

    try:
        R_lst = unique_list(R)
        I_lst = unique_list(I)
        J_lst = unique_list(J)
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring with identity
    h1_ok = False
    try:
        if len(R_lst) > 0:
            if is_add_closed(R_lst) and is_mul_closed(R_lst):
                zero = None
                for e in R_lst:
                    if all((a + e) == a and (e + a) == a for a in R_lst):
                        zero = e
                        break
                if zero is not None:
                    inv_ok = True
                    for a in R_lst:
                        has_inv = False
                        for b in R_lst:
                            if (a + b) == zero and (b + a) == zero:
                                has_inv = True
                                break
                        if not has_inv:
                            inv_ok = False
                            break
                    if inv_ok:
                        one = None
                        for e in R_lst:
                            if all((a * e) == a and (e * a) == a for a in R_lst):
                                one = e
                                break
                        if one is not None:
                            h1_ok = True
    except Exception:
        h1_ok = False

    # H2: I is a two-sided ideal of R
    h2_ok = False
    try:
        if is_subset(I_lst, R_lst) and len(I_lst) > 0:
            if is_add_closed(I_lst):
                zero = None
                for e in R_lst:
                    if all((a + e) == a for a in R_lst):
                        zero = e
                        break
                if zero is not None:
                    inv_ok = True
                    for a in I_lst:
                        has_inv = False
                        for b in I_lst:
                            if (a + b) == zero:
                                has_inv = True
                                break
                        if not has_inv:
                            inv_ok = False
                            break
                    if inv_ok:
                        ideal_ok = True
                        for i in I_lst:
                            for r in R_lst:
                                if (i * r) not in I_lst or (r * i) not in I_lst:
                                    ideal_ok = False
                                    break
                            if not ideal_ok:
                                break
                        if ideal_ok:
                            h2_ok = True
    except Exception:
        h2_ok = False

    # H3: J is a two-sided ideal of R
    h3_ok = False
    try:
        if is_subset(J_lst, R_lst) and len(J_lst) > 0:
            if is_add_closed(J_lst):
                zero = None
                for e in R_lst:
                    if all((a + e) == a for a in R_lst):
                        zero = e
                        break
                if zero is not None:
                    inv_ok = True
                    for a in J_lst:
                        has_inv = False
                        for b in J_lst:
                            if (a + b) == zero:
                                has_inv = True
                                break
                        if not has_inv:
                            inv_ok = False
                            break
                    if inv_ok:
                        ideal_ok = True
                        for j in J_lst:
                            for r in R_lst:
                                if (j * r) not in J_lst or (r * j) not in J_lst:
                                    ideal_ok = False
                                    break
                            if not ideal_ok:
                                break
                        if ideal_ok:
                            h3_ok = True
    except Exception:
        h3_ok = False

    # neg_Q: I \cap J != IJ + JI
    neg_q_ok = False
    try:
        I_cap_J = [x for x in I_lst if x in J_lst]
        
        IJ_gens = []
        for i in I_lst:
            for j in J_lst:
                IJ_gens.append(i * j)
                
        JI_gens = []
        for j in J_lst:
            for i in I_lst:
                JI_gens.append(j * i)
                
        def add_closure(elements):
            closure = unique_list(elements)
            added = True
            while added:
                added = False
                new_elements = []
                for a in closure:
                    for b in closure:
                        c = a + b
                        if c not in closure and c not in new_elements:
                            new_elements.append(c)
                if new_elements:
                    closure.extend(new_elements)
                    added = True
            return closure

        IJ = add_closure(IJ_gens)
        JI = add_closure(JI_gens)
        
        IJ_plus_JI_gens = []
        for x in IJ:
            for y in JI:
                IJ_plus_JI_gens.append(x + y)
                
        IJ_plus_JI = add_closure(IJ_plus_JI_gens)
        
        if not list_eq(I_cap_J, IJ_plus_JI):
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "H_2: I is a two-sided ideal of R",
    "H_3: J is a two-sided ideal of R",
    "¬Q: I \\cap J \\neq IJ + JI"
]

N_HYP = 3
NEG_Q_INDEX = 3