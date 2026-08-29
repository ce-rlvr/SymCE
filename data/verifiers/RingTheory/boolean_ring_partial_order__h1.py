import itertools

class ZnRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def __str__(self):
        return f"Z_{self.n}"

class MatrixRing2x2:
    def __init__(self, n):
        self.n = n
        self.elements = list(itertools.product(range(n), repeat=4))
    def add(self, A, B):
        return tuple((a + b) % self.n for a, b in zip(A, B))
    def mul(self, A, B):
        a, b, c, d = A
        e, f, g, h = B
        return (
            (a*e + b*g) % self.n,
            (a*f + b*h) % self.n,
            (c*e + d*g) % self.n,
            (c*f + d*h) % self.n
        )
    def __str__(self):
        return f"M_2(Z_{self.n})"

# Standard finite rings for witness testing
Z2 = ZnRing(2)
Z3 = ZnRing(3)
Z4 = ZnRing(4)
Z6 = ZnRing(6)
M2_Z2 = MatrixRing2x2(2)

def is_ring(R):
    try:
        if not hasattr(R, 'elements') or not hasattr(R, 'add') or not hasattr(R, 'mul'):
            return False
        elements = list(R.elements)
        add = R.add
        mul = R.mul
        
        # check closure
        for a in elements:
            for b in elements:
                if add(a, b) not in elements: return False
                if mul(a, b) not in elements: return False
                
        # check associativity of add
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    
        # check commutativity of add
        for a in elements:
            for b in elements:
                if add(a, b) != add(b, a): return False
                
        # check identity of add
        has_zero = False
        zero = None
        for z in elements:
            if all(add(z, a) == a and add(a, z) == a for a in elements):
                has_zero = True
                zero = z
                break
        if not has_zero: return False
        
        # check inverses of add
        for a in elements:
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # check associativity of mul
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    
        # check distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                    
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = is_ring(witness)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            elements = list(witness.elements)
            mul = witness.mul
            
            is_po = True
            # Reflexive: x <= x iff x*x = x
            for x in elements:
                if mul(x, x) != x:
                    is_po = False
                    break
            
            # Antisymmetric: x <= y and y <= x implies x = y
            if is_po:
                for x in elements:
                    for y in elements:
                        if mul(x, y) == x and mul(y, x) == y:
                            if x != y:
                                is_po = False
                                break
                    if not is_po:
                        break
                        
            # Transitive: x <= y and y <= z implies x <= z
            if is_po:
                for x in elements:
                    for y in elements:
                        for z in elements:
                            if mul(x, y) == x and mul(y, z) == y:
                                if mul(x, z) != x:
                                    is_po = False
                                    break
                        if not is_po:
                            break
                    if not is_po:
                        break
                        
            neg_q = not is_po
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring and <= is defined as xy = x",
    "¬Q: <= is not a partial order on R"
]

N_HYP = 1
NEG_Q_INDEX = 1