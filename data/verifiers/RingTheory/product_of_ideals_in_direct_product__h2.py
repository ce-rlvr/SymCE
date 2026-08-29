import sympy
from sympy.matrices import eye, zeros

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_zero(R):
    for z in R:
        if all(z + a == a for a in R):
            return z
    return None

def get_neg(x, R):
    z = get_zero(R)
    for y in R:
        if x + y == z:
            return y
    return None

def contains(lst, x):
    return any(x == y for y in lst)

def is_subset(sub, sup):
    return all(contains(sup, x) for x in sub)

def sets_equal(A, B):
    return is_subset(A, B) and is_subset(B, A)

def is_ring(R):
    if not R: return False
    zero = get_zero(R)
    if zero is None: return False
    
    for a in R:
        if get_neg(a, R) is None: return False
        for b in R:
            if not contains(R, a + b): return False
            if not contains(R, a * b): return False
            for c in R:
                if (a + b) + c != a + (b + c): return False
                if (a * b) * c != a * (b * c): return False
                if a * (b + c) != a * b + a * c: return False
                if (a + b) * c != a * c + b * c: return False
    for a in R:
        for b in R:
            if a + b != b + a: return False
    return True

def is_ideal(I, R):
    if not I: return False
    if not is_subset(I, R): return False
    
    zero = get_zero(R)
    if not contains(I, zero): return False
    
    for a in I:
        neg_a = get_neg(a, R)
        if not contains(I, neg_a): return False
        for b in I:
            if not contains(I, a + b): return False
            
    for i in I:
        for r in R:
            if not contains(I, i * r): return False
            if not contains(I, r * i): return False
    return True

def ideal_product(I, J, R):
    prods = []
    for i in I:
        for j in J:
            p = i * j
            if not contains(prods, p):
                prods.append(p)
    
    changed = True
    while changed:
        changed = False
        new_elements = []
        for a in prods:
            for b in prods:
                s = a + b
                if not contains(prods, s) and not contains(new_elements, s):
                    new_elements.append(s)
                neg_b = get_neg(b, R)
                if neg_b is not None:
                    d = a + neg_b
                    if not contains(prods, d) and not contains(new_elements, d):
                        new_elements.append(d)
        if new_elements:
            prods.extend(new_elements)
            changed = True
    return prods

class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __add__(self, other):
        return Pair(self.a + other.a, self.b + other.b)
    def __mul__(self, other):
        return Pair(self.a * other.a, self.b * other.b)
    def __eq__(self, other):
        if not isinstance(other, Pair): return False
        return self.a == other.a and self.b == other.b
    def __repr__(self):
        return f"({self.a}, {self.b})"

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 6:
            R1, R2, I1, J1, I2, J2 = witness
        else:
            R1 = witness.R1
            R2 = witness.R2
            I1 = witness.I1
            J1 = witness.J1
            I2 = witness.I2
            J2 = witness.J2
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_ring(R1) and is_ring(R2)
    except Exception:
        h1 = False

    try:
        h2 = is_ideal(I1, R1) and is_ideal(J1, R1)
    except Exception:
        h2 = False

    try:
        h3 = is_ideal(I2, R2) and is_ideal(J2, R2)
    except Exception:
        h3 = False

    try:
        R1_times_R2 = [Pair(r1, r2) for r1 in R1 for r2 in R2]
        I1_times_I2 = [Pair(i1, i2) for i1 in I1 for i2 in I2]
        J1_times_J2 = [Pair(j1, j2) for j1 in J1 for j2 in J2]
        
        prod_times = ideal_product(I1_times_I2, J1_times_J2, R1_times_R2)
        
        I1_J1 = ideal_product(I1, J1, R1)
        I2_J2 = ideal_product(I2, J2, R2)
        times_prod = [Pair(x, y) for x in I1_J1 for y in I2_J2]
        
        neg_q = not sets_equal(prod_times, times_prod)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are rings",
    "H_2: I_1 and J_1 are ideals of R_1",
    "H_3: I_2 and J_2 are ideals of R_2",
    "¬Q: (I_1 x I_2)(J_1 x J_2) != (I_1 J_1) x (I_2 J_2)"
]

N_HYP = 3
NEG_Q_INDEX = 3