import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

class FiniteRing:
    def __init__(self, elements, add_table, mul_table, zero, one):
        self.elements = list(elements)
        self.add_table = add_table
        self.mul_table = mul_table
        self.zero = zero
        self.one = one

    def add(self, a, b):
        return self.add_table[(a, b)]

    def mul(self, a, b):
        return self.mul_table[(a, b)]

    def is_unit(self, x):
        for y in self.elements:
            if self.mul(x, y) == self.one and self.mul(y, x) == self.one:
                return True
        return False

    def is_local(self):
        if self.one == self.zero:
            return False
        non_units = [x for x in self.elements if not self.is_unit(x)]
        for x in non_units:
            for y in non_units:
                if self.add(x, y) not in non_units:
                    return False
        return True

    def is_valid_ring(self):
        for a in self.elements:
            for b in self.elements:
                if self.add(a, b) != self.add(b, a): return False
                if self.mul(a, b) != self.mul(b, a): return False
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    if self.add(self.add(a, b), c) != self.add(a, self.add(b, c)): return False
                    if self.mul(self.mul(a, b), c) != self.mul(a, self.mul(b, c)): return False
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    if self.mul(a, self.add(b, c)) != self.add(self.mul(a, b), self.mul(a, c)): return False
        for a in self.elements:
            if self.add(a, self.zero) != a: return False
        for a in self.elements:
            if self.mul(a, self.one) != a: return False
        for a in self.elements:
            has_inv = False
            for b in self.elements:
                if self.add(a, b) == self.zero:
                    has_inv = True
                    break
            if not has_inv: return False
        return True

Z6_elements = [0, 1, 2, 3, 4, 5]
Z6_add = {(a, b): (a + b) % 6 for a in Z6_elements for b in Z6_elements}
Z6_mul = {(a, b): (a * b) % 6 for a in Z6_elements for b in Z6_elements}
Z6_ring = FiniteRing(Z6_elements, Z6_add, Z6_mul, 0, 1)

Z2_elements = [0, 1]
Z2_add = {(a, b): (a + b) % 2 for a in Z2_elements for b in Z2_elements}
Z2_mul = {(a, b): (a * b) % 2 for a in Z2_elements for b in Z2_elements}
Z2_ring = FiniteRing(Z2_elements, Z2_add, Z2_mul, 0, 1)

Z4_elements = [0, 1, 2, 3]
Z4_add = {(a, b): (a + b) % 4 for a in Z4_elements for b in Z4_elements}
Z4_mul = {(a, b): (a * b) % 4 for a in Z4_elements for b in Z4_elements}
Z4_ring = FiniteRing(Z4_elements, Z4_add, Z4_mul, 0, 1)

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

def conditions(witness):
    try:
        rings, transition_maps, limit_ring, limit_maps = witness
    except Exception:
        return [False, False]
        
    def is_valid_system():
        try:
            if not limit_ring.is_valid_ring(): return False
            for R in rings.values():
                if not R.is_valid_ring(): return False
            I = list(rings.keys())
            if not I: return False
            le = { (i, j) for (i, j) in transition_maps.keys() }
            for i in I:
                if (i, i) not in le: return False
                f_ii = transition_maps[(i, i)]
                for x in rings[i].elements:
                    if f_ii(x) != x: return False
            for i in I:
                for j in I:
                    for k in I:
                        if (i, j) in le and (j, k) in le:
                            if (i, k) not in le: return False
                            f_ij = transition_maps[(i, j)]
                            f_jk = transition_maps[(j, k)]
                            f_ik = transition_maps[(i, k)]
                            for x in rings[i].elements:
                                if f_jk(f_ij(x)) != f_ik(x): return False
            for i in I:
                for j in I:
                    if not any((i, k) in le and (j, k) in le for k in I): return False
            for (i, j), f in transition_maps.items():
                R = rings[i]
                S = rings[j]
                if f(R.zero) != S.zero or f(R.one) != S.one: return False
                for x in R.elements:
                    for y in R.elements:
                        if f(R.add(x, y)) != S.add(f(x), f(y)): return False
                        if f(R.mul(x, y)) != S.mul(f(x), f(y)): return False
            for i, f in limit_maps.items():
                R = rings[i]
                S = limit_ring
                if f(R.zero) != S.zero or f(R.one) != S.one: return False
                for x in R.elements:
                    for y in R.elements:
                        if f(R.add(x, y)) != S.add(f(x), f(y)): return False
                        if f(R.mul(x, y)) != S.mul(f(x), f(y)): return False
            for (i, j), f in transition_maps.items():
                for x in rings[i].elements:
                    if limit_maps[j](f(x)) != limit_maps[i](x): return False
            limit_elements = []
            for i, f in limit_maps.items():
                for x in rings[i].elements:
                    fx = f(x)
                    if fx not in limit_elements:
                        limit_elements.append(fx)
            if len(limit_elements) != len(limit_ring.elements): return False
            for x in limit_ring.elements:
                if x not in limit_elements: return False
            for i, f in limit_maps.items():
                for x in rings[i].elements:
                    if f(x) == limit_ring.zero:
                        found = False
                        for j in I:
                            if (i, j) in le and transition_maps[(i, j)](x) == rings[j].zero:
                                found = True
                                break
                        if not found: return False
            return True
        except Exception:
            return False

    if not is_valid_system():
        return [False, False]

    h1_ok = False
    try:
        h1_ok = True
        for (i, j), f in transition_maps.items():
            R = rings[i]
            S = rings[j]
            for x in R.elements:
                if S.is_unit(f(x)) and not R.is_unit(x):
                    h1_ok = False
                    break
            if not h1_ok:
                break
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        neg_q_ok = not limit_ring.is_local()
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: All transition maps f_{ij} are local homomorphisms",
    "¬Q: The direct limit of the system is not a local ring"
]
N_HYP = 1
NEG_Q_INDEX = 1