import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
class RingElement:
    def __init__(self, val, mod):
        self.val = val % mod
        self.mod = mod
    def __add__(self, other):
        return RingElement((self.val + other.val) % self.mod, self.mod)
    def __sub__(self, other):
        return RingElement((self.val - other.val) % self.mod, self.mod)
    def __mul__(self, other):
        return RingElement((self.val * other.val) % self.mod, self.mod)
    def __eq__(self, other):
        if not isinstance(other, RingElement):
            return False
        return self.val == other.val and self.mod == other.mod
    def __hash__(self):
        return hash((self.val, self.mod))
    def __repr__(self):
        return f"{self.val} mod {self.mod}"

def make_ring(elements, mod):
    return [RingElement(e, mod) for e in elements]

# A standard counterexample: 2Z/8Z (a commutative ring without identity)
R_2Z8 = make_ring([0, 2, 4, 6], 8)
I_2Z8 = make_ring([0, 4], 8)
J_2Z8 = make_ring([0, 4], 8)
Nil_2Z8 = make_ring([0, 2, 4, 6], 8)

# Standard algebra objects
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

def set_equals(A, B):
    for a in A:
        if a not in B: return False
    for b in B:
        if b not in A: return False
    return True

def get_nilradical_general(R, zero):
    nilradical = []
    for x in R:
        ideal = [x]
        while True:
            new_elements = []
            for a in ideal:
                for r in R:
                    ar = a * r
                    if ar in R and ar not in ideal and ar not in new_elements:
                        new_elements.append(ar)
                    ra = r * a
                    if ra in R and ra not in ideal and ra not in new_elements:
                        new_elements.append(ra)
                for b in ideal:
                    ab = a + b
                    if ab in R and ab not in ideal and ab not in new_elements:
                        new_elements.append(ab)
            if not new_elements:
                break
            ideal.extend(new_elements)
        
        power = list(ideal)
        is_nil = False
        for _ in range(len(R) + 1):
            if all(e == zero for e in power):
                is_nil = True
                break
            next_power = []
            for a in power:
                for b in ideal:
                    p = a * b
                    if p not in next_power:
                        next_power.append(p)
            while True:
                new_add = []
                for a in next_power:
                    for b in next_power:
                        ab = a + b
                        if ab not in next_power and ab not in new_add:
                            new_add.append(ab)
                if not new_add:
                    break
                next_power.extend(new_add)
            power = next_power
            
        if is_nil:
            nilradical.append(x)
            
    return nilradical

def is_ideal(I, R, zero):
    if not I:
        return False
    if zero not in I:
        return False
    for x in I:
        if x not in R:
            return False
        has_neg = False
        for y in I:
            if x + y == zero:
                has_neg = True
                break
        if not has_neg:
            return False
        for y in I:
            if (x + y) not in I:
                return False
        for r in R:
            if (x * r) not in I:
                return False
            if (r * x) not in I:
                return False
    return True

def is_comaximal_mod_N(I, J, N, R):
    sums = []
    for i in I:
        for j in J:
            for n in N:
                s = (i + j) + n
                if s not in sums:
                    sums.append(s)
    for r in R:
        if r not in sums:
            return False
    return True

def is_comaximal(I, J, R):
    sums = []
    for i in I:
        for j in J:
            s = i + j
            if s not in sums:
                sums.append(s)
    for r in R:
        if r not in sums:
            return False
    return True

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            R, I, J, Nil_R = witness
            provided_nil = True
        elif len(witness) == 3:
            R, I, J = witness
            provided_nil = False
        else:
            return [False, False, False, False]
            
        R_list = list(R)
        I_list = list(I)
        J_list = list(J)
        
        # Check closure of R
        for a in R_list:
            for b in R_list:
                if (a + b) not in R_list:
                    return [False, False, False, False]
                if (a * b) not in R_list:
                    return [False, False, False, False]
        
        # Find zero element
        zero = None
        for z in R_list:
            if all(z + x == x for x in R_list) and all(x + z == x for x in R_list):
                zero = z
                break
        if zero is None:
            return [False, False, False, False]
            
        # H1: Nil(R) is the nilradical of R
        if provided_nil:
            Nil_R_list = list(Nil_R)
            expected_nil = get_nilradical_general(R_list, zero)
            H1 = set_equals(Nil_R_list, expected_nil)
        else:
            Nil_R_list = get_nilradical_general(R_list, zero)
            H1 = True
            
        # H2: I and J are ideals of R
        H2 = is_ideal(I_list, R_list, zero) and is_ideal(J_list, R_list, zero)
        
        # H3: The image of I and J in R/Nil(R) are comaximal
        H3 = is_comaximal_mod_N(I_list, J_list, Nil_R_list, R_list)
        
        # ¬Q: I and J are NOT comaximal in R
        neg_Q = not is_comaximal(I_list, J_list, R_list)
        
        return [H1, H2, H3, neg_Q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: Nil(R) is the nilradical of R",
    "H_2: I and J are ideals of R",
    "H_3: The image of I and J in R/Nil(R) are comaximal",
    "¬Q: I and J are not comaximal in R"
]

N_HYP = 3
NEG_Q_INDEX = 3