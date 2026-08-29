import math

class ZnRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        
    def add(self, x, y):
        return (x + y) % self.n
        
    def mul(self, x, y):
        return (x * y) % self.n
        
    def ideal(self, *gens):
        g = self.n
        for x in gens:
            g = math.gcd(g, x)
        return [i for i in self.elements if i % g == 0]
        
    def __iter__(self):
        return iter(self.elements)
        
    def __contains__(self, item):
        return item in self.elements
        
    def intersection(self, I, J):
        return [x for x in I if x in J]
        
    def __str__(self):
        return f"Z_{self.n}"
        
    def __repr__(self):
        return f"Z_{self.n}"

# Standard finite rings that can be used to construct counterexamples
Z2 = ZnRing(2)
Z3 = ZnRing(3)
Z4 = ZnRing(4)
Z5 = ZnRing(5)
Z6 = ZnRing(6)
Z8 = ZnRing(8)
Z10 = ZnRing(10)
Z12 = ZnRing(12)

def conditions(witness) -> list[bool]:
    try:
        R, I, J = witness
        
        # Parse the ring R
        if hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul'):
            elements = list(R.elements)
            add = R.add
            mul = R.mul
        elif isinstance(R, tuple) and len(R) == 3:
            elements = list(R[0])
            add = R[1]
            mul = R[2]
        elif isinstance(R, int):
            n = R
            if n <= 0:
                return [False, False, False]
            elements = list(range(n))
            add = lambda x, y, n=n: (x + y) % n
            mul = lambda x, y, n=n: (x * y) % n
        else:
            return [False, False, False]
            
        # Limit size for performance
        if len(elements) > 2000:
            return [False, False, False]
            
        # Find the zero element of the ring
        zero = None
        for e in elements:
            if all(add(e, x) == x for x in elements):
                zero = e
                break
        if zero is None:
            return [False, False, False]
                
        def check_ideal(S):
            try:
                S_coll = set(S)
                elem_coll = set(elements)
            except TypeError:
                S_coll = list(S)
                elem_coll = list(elements)
                
            if not S_coll: 
                return False
                
            for x in S_coll:
                if x not in elem_coll: 
                    return False
            
            if zero not in S_coll: 
                return False
            
            # Check closure under addition and existence of additive inverses
            for x in S_coll:
                for y in S_coll:
                    if add(x, y) not in S_coll: 
                        return False
                has_inv = False
                for y in S_coll:
                    if add(x, y) == zero:
                        has_inv = True
                        break
                if not has_inv: 
                    return False
                
            # Check absorption property (left and right)
            for r in elements:
                for x in S_coll:
                    if mul(r, x) not in S_coll: 
                        return False
                    if mul(x, r) not in S_coll: 
                        return False
            return True

        try:
            I_list = list(I)
            J_list = list(J)
        except Exception:
            return [False, False, False]

        # H_1: I is a non-zero ideal of R
        try:
            is_non_zero_I = any(x != zero for x in I_list)
            h1 = check_ideal(I_list) and is_non_zero_I
        except Exception:
            h1 = False
            
        # H_2: J is a non-zero ideal of R
        try:
            is_non_zero_J = any(x != zero for x in J_list)
            h2 = check_ideal(J_list) and is_non_zero_J
        except Exception:
            h2 = False
            
        # ¬Q: The intersection I \cap J is not a non-zero ideal of R
        try:
            try:
                J_set = set(J_list)
                intersection = [x for x in I_list if x in J_set]
            except TypeError:
                intersection = [x for x in I_list if x in J_list]
                
            is_ideal_int = check_ideal(intersection)
            is_non_zero_int = any(x != zero for x in intersection)
            is_non_zero_ideal_int = is_ideal_int and is_non_zero_int
            neg_q = not is_non_zero_ideal_int
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a non-zero ideal of R",
    "H_2: J is a non-zero ideal of R",
    "¬Q: The intersection I \\cap J is not a non-zero ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2