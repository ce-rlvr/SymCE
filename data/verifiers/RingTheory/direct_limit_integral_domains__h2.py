import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: {R_i, f_{ij}} is a directed system of rings over a directed set I",
    "H_2: For every i <= j in I, the transition homomorphism f_{ij} is injective",
    "¬Q: The direct limit is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    if isinstance(witness, (int, sympy.Integer)):
        n = int(witness)
        if n < 1:
            return [False, False, False]
        # Default witness: constant directed system of Z/nZ
        I = [1, 2, 3]
        leq = lambda i, j: i <= j
        R_elements = lambda i: list(range(n))
        R_add = lambda i, a, b: (a + b) % n
        R_mul = lambda i, a, b: (a * b) % n
        R_zero = lambda i: 0
        R_one = lambda i: 1 % n
        f = lambda i, j, a: a
    elif isinstance(witness, dict):
        try:
            I = witness['I']
            leq = witness['leq']
            R_elements = witness['R_elements']
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            R_zero = witness['R_zero']
            R_one = witness['R_one']
            f = witness['f']
        except KeyError:
            return [False, False, False]
    else:
        return [False, False, False]

    def check_h1():
        try:
            if not I or not isinstance(I, list): 
                return False
            
            # Directed set conditions
            for i in I:
                if not leq(i, i): return False
            for i in I:
                for j in I:
                    for k in I:
                        if leq(i, j) and leq(j, k):
                            if not leq(i, k): return False
            for i in I:
                for j in I:
                    has_ub = False
                    for k in I:
                        if leq(i, k) and leq(j, k):
                            has_ub = True
                            break
                    if not has_ub: return False
                    
            # Ring conditions for each R_i
            for i in I:
                elems = R_elements(i)
                z_el = R_zero(i)
                o_el = R_one(i)
                if z_el not in elems or o_el not in elems: return False
                if z_el == o_el and len(elems) > 1: return False
                
                for a in elems:
                    for b in elems:
                        if R_add(i, a, b) not in elems: return False
                        if R_mul(i, a, b) not in elems: return False
                        if R_add(i, a, b) != R_add(i, b, a): return False
                        
                        for c in elems:
                            if R_add(i, R_add(i, a, b), c) != R_add(i, a, R_add(i, b, c)): return False
                            if R_mul(i, R_mul(i, a, b), c) != R_mul(i, a, R_mul(i, b, c)): return False
                            if R_mul(i, a, R_add(i, b, c)) != R_add(i, R_mul(i, a, b), R_mul(i, a, c)): return False
                            if R_mul(i, R_add(i, a, b), c) != R_add(i, R_mul(i, a, c), R_mul(i, b, c)): return False
                            
                    if R_add(i, a, z_el) != a: return False
                    if R_mul(i, a, o_el) != a: return False
                    if R_mul(i, o_el, a) != a: return False
                    
                    has_inv = False
                    for b in elems:
                        if R_add(i, a, b) == z_el:
                            has_inv = True
                            break
                    if not has_inv: return False
                    
            # Homomorphisms and directed system conditions
            for i in I:
                for j in I:
                    if leq(i, j):
                        if f(i, j, R_one(i)) != R_one(j): return False
                        for a in R_elements(i):
                            if f(i, j, a) not in R_elements(j): return False
                            for b in R_elements(i):
                                if f(i, j, R_add(i, a, b)) != R_add(j, f(i, j, a), f(i, j, b)): return False
                                if f(i, j, R_mul(i, a, b)) != R_mul(j, f(i, j, a), f(i, j, b)): return False
                                
                        if i == j:
                            for a in R_elements(i):
                                if f(i, i, a) != a: return False
                                
                        for k in I:
                            if leq(j, k):
                                for a in R_elements(i):
                                    if f(j, k, f(i, j, a)) != f(i, k, a): return False
            return True
        except Exception:
            return False

    def check_h2():
        try:
            for i in I:
                for j in I:
                    if leq(i, j):
                        for a in R_elements(i):
                            for b in R_elements(i):
                                if f(i, j, a) == f(i, j, b):
                                    if a != b: return False
            return True
        except Exception:
            return False

    def check_neg_q():
        try:
            pairs = [(i, a) for i in I for a in R_elements(i)]
            
            def equiv(p1, p2):
                i, a = p1
                j, b = p2
                for k in I:
                    if leq(i, k) and leq(j, k):
                        if f(i, k, a) == f(j, k, b):
                            return True
                return False
                
            classes = []
            for p in pairs:
                found = False
                for c in classes:
                    if equiv(p, c[0]):
                        c.append(p)
                        found = True
                        break
                if not found:
                    classes.append([p])
                    
            def get_class(p):
                for idx, c in enumerate(classes):
                    if equiv(p, c[0]):
                        return idx
                return None
                
            def L_mul(idxA, idxB):
                i, a = classes[idxA][0]
                j, b = classes[idxB][0]
                for k in I:
                    if leq(i, k) and leq(j, k):
                        mul_val = R_mul(k, f(i, k, a), f(j, k, b))
                        return get_class((k, mul_val))
                return None
                
            L_zero = get_class((I[0], R_zero(I[0])))
            L_one = get_class((I[0], R_one(I[0])))
            
            if L_zero is None or L_one is None:
                return False
                
            if L_zero == L_one:
                return True # Trivial ring is not an integral domain
                
            # Check commutativity
            for a in range(len(classes)):
                for b in range(len(classes)):
                    m1 = L_mul(a, b)
                    m2 = L_mul(b, a)
                    if m1 is None or m2 is None:
                        return False
                    if m1 != m2:
                        return True # Not commutative -> not an integral domain
                        
            # Check for zero divisors
            for a in range(len(classes)):
                for b in range(len(classes)):
                    m = L_mul(a, b)
                    if m is None:
                        return False
                    if m == L_zero:
                        if a != L_zero and b != L_zero:
                            return True # Has zero divisors -> not an integral domain
                            
            return False # Is an integral domain -> neg_Q is False
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_q()]