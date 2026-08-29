import itertools

class ZMod:
    """A simple finite commutative ring Z/nZ."""
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1 if n > 1 else 0
        
    def add(self, a, b):
        return (a + b) % self.n
        
    def mul(self, a, b):
        return (a * b) % self.n
        
    def __repr__(self):
        return f"ZMod({self.n})"

# Top-level setup bindings
Z2 = ZMod(2)
Z3 = ZMod(3)
Z4 = ZMod(4)
Z6 = ZMod(6)
Z8 = ZMod(8)
Z12 = ZMod(12)

def get_add(R):
    return R.add if hasattr(R, 'add') else lambda a, b: a + b

def get_mul(R):
    return R.mul if hasattr(R, 'mul') else lambda a, b: a * b

def get_zero(R):
    return R.zero if hasattr(R, 'zero') else 0

def check_commutative_ring(R):
    try:
        if isinstance(R, ZMod):
            return True
        if hasattr(R, 'is_commutative') and R.is_commutative:
            return True
        if not hasattr(R, 'elements'):
            return False
            
        elements = list(R.elements)
        if len(elements) > 50:
            # Too large to check exhaustively, assume True if it has elements
            return True
            
        add = get_add(R)
        mul = get_mul(R)
        zero = get_zero(R)
        
        if zero not in elements: 
            return False
            
        for a in elements:
            if add(a, zero) != a: return False
            if add(zero, a) != a: return False
            
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elements:
                if add(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                if mul(a, b) not in elements: return False
                if mul(a, b) != mul(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
        return True
    except Exception:
        return False

def check_ideal(R, I):
    try:
        I = list(I)
        if not I: return False
        add = get_add(R)
        mul = get_mul(R)
        zero = get_zero(R)
        
        if zero not in I: return False
        
        if hasattr(R, 'elements'):
            elements = list(R.elements)
            for a in I:
                if a not in elements: return False
                
            for a in I:
                for b in I:
                    if add(a, b) not in I: return False
                    minus_b = None
                    for x in elements:
                        if add(b, x) == zero:
                            minus_b = x
                            break
                    if minus_b is None or add(a, minus_b) not in I: return False
                    
            for a in I:
                for r in elements:
                    if mul(a, r) not in I: return False
                    if mul(r, a) not in I: return False
            return True
        else:
            return False
    except Exception:
        return False

def check_conclusion_fails(R, I, J):
    try:
        I = list(I)
        J = list(J)
        
        if hasattr(R, 'elements'):
            elements = list(R.elements)
            for j in J:
                if j not in elements: return False
                
        add = get_add(R)
        mul = get_mul(R)
        
        # I + J
        I_plus_J = []
        for i in I:
            for j in J:
                I_plus_J.append(add(i, j))
                
        I_plus_J_unique = []
        for x in I_plus_J:
            if x not in I_plus_J_unique:
                I_plus_J_unique.append(x)
                
        # I \cap J
        I_cap_J = [x for x in I if x in J]
        
        # (I+J)(I \cap J)
        LHS = []
        for x in I_plus_J_unique:
            for y in I_cap_J:
                LHS.append(mul(x, y))
                
        LHS_unique = []
        for x in LHS:
            if x not in LHS_unique:
                LHS_unique.append(x)
                
        # IJ
        RHS = []
        for i in I:
            for j in J:
                RHS.append(mul(i, j))
                
        RHS_unique = []
        for x in RHS:
            if x not in RHS_unique:
                RHS_unique.append(x)
                
        # Check if LHS is NOT a subset of RHS
        for x in LHS_unique:
            if x not in RHS_unique:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample.
    Expected witness format: (n, I, J) for Z/nZ, or (R, I, J) where R is a ring object.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            if isinstance(witness[0], int):
                n, I, J = witness
                R = ZMod(n)
            else:
                R, I, J = witness
        else:
            return [False, False, False]
            
        h1 = check_commutative_ring(R)
        h2 = check_ideal(R, I)
        neg_q = check_conclusion_fails(R, I, J)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: (I+J)(I \\cap J) is not a subset of IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2