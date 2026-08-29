import itertools
import functools

class FiniteRing:
    def __init__(self, elements, add, mul, zero, one):
        self.elements = list(elements)
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one

def make_Zn(n):
    return FiniteRing(
        elements=list(range(n)),
        add=lambda a, b: (a + b) % n,
        mul=lambda a, b: (a * b) % n,
        zero=0,
        one=1
    )

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)

class ProductRing(FiniteRing):
    def __init__(self, R1, R2):
        elements = [(a, b) for a in R1.elements for b in R2.elements]
        add = lambda x, y: (R1.add(x[0], y[0]), R2.add(x[1], y[1]))
        mul = lambda x, y: (R1.mul(x[0], y[0]), R2.mul(x[1], y[1]))
        zero = (R1.zero, R2.zero)
        one = (R1.one, R2.one)
        super().__init__(elements, add, mul, zero, one)

def check_ring(elements, add, mul, zero, one):
    elements = list(elements)
    if zero not in elements or one not in elements: return False
    if zero == one: return False
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: return False
        if mul(a, one) != a or mul(one, a) != a: return False
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
        for b in elements:
            try:
                sum_ab = add(a, b)
                prod_ab = mul(a, b)
            except Exception:
                return False
            if sum_ab not in elements: return False
            if prod_ab not in elements: return False
            if sum_ab != add(b, a): return False
            if prod_ab != mul(b, a): return False
            for c in elements:
                if add(sum_ab, c) != add(a, add(b, c)): return False
                if mul(prod_ab, c) != mul(a, mul(b, c)): return False
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    return True

def is_ideal(elements, add, mul, zero, Q):
    Q = list(Q)
    if not Q: return False
    if zero not in Q: return False
    for q1 in Q:
        if q1 not in elements: return False
        has_inv = False
        for q2 in Q:
            if add(q1, q2) == zero:
                has_inv = True
                break
        if not has_inv: return False
        for q2 in Q:
            if add(q1, q2) not in Q: return False
        for r in elements:
            if mul(r, q1) not in Q: return False
            if mul(q1, r) not in Q: return False
    return True

def is_primary_ideal(elements, add, mul, zero, Q):
    Q = list(Q)
    if not is_ideal(elements, add, mul, zero, Q): return False
    
    is_proper = False
    for e in elements:
        if e not in Q:
            is_proper = True
            break
    if not is_proper: return False
    
    for a in elements:
        for b in elements:
            if mul(a, b) in Q:
                if a in Q:
                    continue
                b_pow = b
                found = False
                visited = []
                while b_pow not in visited:
                    if b_pow in Q:
                        found = True
                        break
                    visited.append(b_pow)
                    b_pow = mul(b_pow, b)
                if not found:
                    return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            f = witness['f']
            Q = witness['Q']
        else:
            R = witness.R
            S = witness.S
            f = witness.f
            Q = witness.Q
            
        def get_ring(obj):
            if isinstance(obj, dict):
                return obj['elements'], obj['add'], obj['mul'], obj['zero'], obj['one']
            else:
                return obj.elements, obj.add, obj.mul, obj.zero, obj.one

        R_el, R_add, R_mul, R_z, R_o = get_ring(R)
        S_el, S_add, S_mul, S_z, S_o = get_ring(S)
        
        R_el = list(R_el)
        S_el = list(S_el)
        Q = list(Q)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = check_ring(R_el, R_add, R_mul, R_z, R_o) and check_ring(S_el, S_add, S_mul, S_z, S_o)
    except Exception:
        h1 = False

    try:
        h2 = True
        f_dict = f if isinstance(f, dict) else None
        def eval_f(x):
            if f_dict is not None: return f_dict[x]
            return f(x)
            
        for a in R_el:
            if eval_f(a) not in S_el:
                h2 = False
                break
            for b in R_el:
                if eval_f(R_add(a, b)) != S_add(eval_f(a), eval_f(b)):
                    h2 = False
                    break
                if eval_f(R_mul(a, b)) != S_mul(eval_f(a), eval_f(b)):
                    h2 = False
                    break
            if not h2: break
    except Exception:
        h2 = False

    try:
        h3 = is_primary_ideal(S_el, S_add, S_mul, S_z, Q)
    except Exception:
        h3 = False

    try:
        f_dict = f if isinstance(f, dict) else None
        def eval_f(x):
            if f_dict is not None: return f_dict[x]
            return f(x)
            
        preimage = []
        for x in R_el:
            if eval_f(x) in Q:
                preimage.append(x)
                
        neg_q = not is_primary_ideal(R_el, R_add, R_mul, R_z, preimage)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: Q is a primary ideal of S",
    "¬Q: The preimage of Q under f is not a primary ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3