import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        elements, add, mul, zero = witness
        
        h1 = True
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a:
                h1 = False
            inv_found = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    inv_found = True
                    break
            if not inv_found:
                h1 = False
            for b in elements:
                if add(a, b) not in elements or mul(a, b) not in elements:
                    h1 = False
                if add(a, b) != add(b, a) or mul(a, b) != mul(b, a):
                    h1 = False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)):
                        h1 = False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)):
                        h1 = False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)):
                        h1 = False
        
        def is_qr(a, elems, add_f, mul_f):
            for b in elems:
                if add_f(a, b) == mul_f(a, b):
                    return True
            return False

        def get_J(elems, add_f, mul_f):
            j_rad = []
            for x in elems:
                if all(is_qr(mul_f(x, y), elems, add_f, mul_f) for y in elems):
                    j_rad.append(x)
            return j_rad

        J = get_J(elements, add, mul)
        
        cosets = []
        for x in elements:
            found = False
            for c in cosets:
                if any(add(c[0], j) == x for j in J):
                    c.append(x)
                    found = True
                    break
            if not found:
                cosets.append([x])
        
        q_elems = [c[0] for c in cosets]
        
        def q_add(x, y):
            s = add(x, y)
            for c in cosets:
                if s in c: return c[0]
            return s
            
        def q_mul(x, y):
            p = mul(x, y)
            for c in cosets:
                if p in c: return c[0]
            return p

        J_q = get_J(q_elems, q_add, q_mul)
        
        neg_q = len(J_q) > 1
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The Jacobson radical of R/J(R) is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1