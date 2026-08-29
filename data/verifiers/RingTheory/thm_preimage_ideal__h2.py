import itertools

class Ring:
    def __init__(self, elements, add_func, mul_func):
        self.elements = list(elements)
        self._add = add_func
        self._mul = mul_func
        self.zero = None
        for e in self.elements:
            try:
                if all(self.add(e, x) == x for x in self.elements):
                    self.zero = e
                    break
            except Exception:
                pass

    def add(self, a, b):
        if callable(self._add):
            return self._add(a, b)
        return self._add[(a, b)]

    def mul(self, a, b):
        if callable(self._mul):
            return self._mul(a, b)
        return self._mul[(a, b)]

def Z(n):
    return Ring(list(range(n)), lambda a, b: (a + b) % n, lambda a, b: (a * b) % n)

Z2 = Z(2)
Z3 = Z(3)
Z4 = Z(4)
Z5 = Z(5)
Z6 = Z(6)

def ProductRing(R1, R2):
    elements = list(itertools.product(R1.elements, R2.elements))
    def add(x, y): return (R1.add(x[0], y[0]), R2.add(x[1], y[1]))
    def mul(x, y): return (R1.mul(x[0], y[0]), R2.mul(x[1], y[1]))
    return Ring(elements, add, mul)

def is_function(f, R, S):
    try:
        for r in R.elements:
            val = f(r) if callable(f) else f[r]
            if val not in S.elements:
                return False
        return True
    except Exception:
        return False

def is_ring(R):
    try:
        elements = R.elements
        zero = R.zero
        add = R.add
        mul = R.mul
            
        if not elements: return False
        if zero is None: return False
        if zero not in elements: return False
        
        # check add commutative group
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
        # check add inverse
        for a in elements:
            if not any(add(a, b) == zero for b in elements): return False
        # check mul associative
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
        # check distributive
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
        return True
    except Exception:
        return False

def is_ideal(J, S):
    try:
        if not isinstance(J, (list, set, tuple)): return False
        J = list(J)
        if not J: return False
        if not all(x in S.elements for x in J): return False
        
        # check subgroup under add
        for a in J:
            for b in J:
                if S.add(a, b) not in J: return False
                
        # check absorbing under mul
        for j in J:
            for s in S.elements:
                if S.mul(j, s) not in J: return False
                if S.mul(s, j) not in J: return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        R, S, f, J = witness
    except Exception:
        return [False, False, False]
        
    # H1: R and S are rings
    try:
        h1 = is_ring(R) and is_ring(S) and is_function(f, R, S)
    except Exception:
        h1 = False
        
    # H2: J is an ideal of S
    try:
        h2 = is_ideal(J, S)
    except Exception:
        h2 = False
        
    # neg_Q: f^{-1}(J) is NOT an ideal of R containing ker(f)
    try:
        if not is_function(f, R, S):
            neg_q = False
        else:
            ker_f = []
            for r in R.elements:
                val = f(r) if callable(f) else f[r]
                if val == S.zero:
                    ker_f.append(r)
            
            preimage = []
            for r in R.elements:
                val = f(r) if callable(f) else f[r]
                if val in J:
                    preimage.append(r)
            
            contains_ker = all(x in preimage for x in ker_f)
            is_id = is_ideal(preimage, R)
            
            concl = contains_ker and is_id
            neg_q = not concl
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings and f is a function from R to S",
    "H_2: J is an ideal of S",
    "¬Q: The preimage f^{-1}(J) is not an ideal of R containing ker(f)"
]

N_HYP = 2
NEG_Q_INDEX = 2