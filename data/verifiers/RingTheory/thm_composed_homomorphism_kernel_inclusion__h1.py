import sympy
from sympy import Matrix, eye, zeros

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class ZRing:
    """A simple representation of the ring Z/nZ."""
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
    def add(self, a, b): 
        return (a + b) % self.n
    def mul(self, a, b): 
        return (a * b) % self.n
    def zero(self): 
        return 0
    def one(self): 
        return 1 % self.n

def get_elements(ring):
    if hasattr(ring, 'elements'):
        return ring.elements
    return list(ring)

def get_zero(ring):
    if hasattr(ring, 'zero'):
        z = ring.zero
        return z() if callable(z) else z
    return 0

def get_one(ring):
    if hasattr(ring, 'one'):
        o = ring.one
        return o() if callable(o) else o
    return 1

def ring_add(ring, a, b):
    if hasattr(ring, 'add'): 
        return ring.add(a, b)
    return a + b

def ring_mul(ring, a, b):
    if hasattr(ring, 'mul'): 
        return ring.mul(a, b)
    return a * b

def get_eval(f):
    if isinstance(f, dict):
        return lambda x: f.get(x, 0)
    return f

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        # Matrix fallback
        if isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[0], 'nullspace'):
            f, g = witness
            try:
                h1 = (f.cols > 0 and f.rows > 0)
                h2 = (g.cols == f.rows and g.rows > 0)
                ns_f = f.nullspace()
                gf = g * f
                is_subset = True
                for v in ns_f:
                    if not (gf * v).is_zero_matrix:
                        is_subset = False
                        break
                neg_q = not is_subset
                return [h1, h2, neg_q]
            except Exception:
                return [False, False, False]

        # Unpack witness
        if isinstance(witness, tuple):
            if len(witness) == 5:
                R, S, T, f, g = witness
            elif len(witness) == 2:
                f, g = witness
                if isinstance(f, dict) and isinstance(g, dict):
                    R_n = max(f.keys()) + 1 if f else 1
                    S_n = max(list(f.values()) + list(g.keys())) + 1 if f or g else 1
                    T_n = max(g.values()) + 1 if g else 1
                    R = ZRing(R_n)
                    S = ZRing(S_n)
                    T = ZRing(T_n)
                else:
                    return [False, False, False]
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            T = witness.get('T')
            f = witness.get('f')
            g = witness.get('g')
        else:
            return [False, False, False]

        eval_f = get_eval(f)
        eval_g = get_eval(g)
        
        R_elems = get_elements(R)
        S_elems = get_elements(S)
        
        # Check H1: f is a ring hom R -> S
        try:
            h1 = True
            if eval_f(get_one(R)) != get_one(S):
                h1 = False
            for a in R_elems:
                for b in R_elems:
                    if eval_f(ring_add(R, a, b)) != ring_add(S, eval_f(a), eval_f(b)):
                        h1 = False
                    if eval_f(ring_mul(R, a, b)) != ring_mul(S, eval_f(a), eval_f(b)):
                        h1 = False
        except Exception:
            h1 = False
            
        # Check H2: g is a ring hom S -> T
        try:
            h2 = True
            if eval_g(get_one(S)) != get_one(T):
                h2 = False
            for a in S_elems:
                for b in S_elems:
                    if eval_g(ring_add(S, a, b)) != ring_add(T, eval_g(a), eval_g(b)):
                        h2 = False
                    if eval_g(ring_mul(S, a, b)) != ring_mul(T, eval_g(a), eval_g(b)):
                        h2 = False
        except Exception:
            h2 = False
            
        # Check Conclusion: ker(f) is a subset of ker(g o f)
        try:
            ker_f = []
            for x in R_elems:
                if eval_f(x) == get_zero(S):
                    ker_f.append(x)
                    
            ker_gf = []
            for x in R_elems:
                if eval_g(eval_f(x)) == get_zero(T):
                    ker_gf.append(x)
                    
            is_subset = True
            for x in ker_f:
                if x not in ker_gf:
                    is_subset = False
                    break
            neg_q = not is_subset
        except Exception:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: g is a ring homomorphism from S to T",
    "¬Q: ker(f) is not a subset of ker(g o f)"
]

N_HYP = 2
NEG_Q_INDEX = 2