import itertools
import sympy

class Ring:
    def __init__(self, elements, zero, add_table, mul_table):
        self.elements = elements
        self.zero = zero
        self.add_table = add_table
        self.mul_table = mul_table
        
    def add(self, a, b):
        return self.add_table[a][b]
        
    def mul(self, a, b):
        return self.mul_table[a][b]

# Top-level setup for potential witnesses
TR = Ring([0], 0, {0: {0: 0}}, {0: {0: 0}})
Z2_ring = Ring([0, 1], 0, {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}}, {0: {0: 0, 1: 0}, 1: {0: 0, 1: 1}})

def is_ring(R):
    try:
        elements = []
        for i, e in enumerate(R.elements):
            if i > 100: return False
            elements.append(e)
            
        zero = R.zero
        if zero not in elements: return False
        
        # Closure
        for a in elements:
            for b in elements:
                if R.add(a, b) not in elements: return False
                if R.mul(a, b) not in elements: return False
                
        # Associativity and Distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                    if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                    if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                    if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
                    
        # Commutativity of addition
        for a in elements:
            for b in elements:
                if R.add(a, b) != R.add(b, a): return False
                
        # Additive identity
        for a in elements:
            if R.add(a, zero) != a: return False
            if R.add(zero, a) != a: return False
            
        # Additive inverse
        for a in elements:
            has_inv = False
            for b in elements:
                if R.add(a, b) == zero and R.add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Multiplicative identity
        has_one = False
        for e in elements:
            is_one = True
            for a in elements:
                if R.mul(e, a) != a or R.mul(a, e) != a:
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return False
        
        return True
    except Exception:
        return False

def is_boolean_ring(R):
    if not is_ring(R): return False
    try:
        for a in R.elements:
            if R.mul(a, a) != a: return False
        return True
    except Exception:
        return False

def has_total_order(R):
    try:
        elements = []
        for i, e in enumerate(R.elements):
            if i > 100: return False
            elements.append(e)
            
        zero = R.zero
        
        # Find additive inverses
        neg = []
        for a in elements:
            found = False
            for b in elements:
                if R.add(a, b) == zero:
                    neg.append(b)
                    found = True
                    break
            if not found:
                return False
                
        pairs = []
        seen = [zero]
        for i, x in enumerate(elements):
            if x in seen: continue
            nx = neg[i]
            # In an ordered ring, if x != 0, we cannot have x = -x
            if nx == x:
                return False
            pairs.append((x, nx))
            seen.append(x)
            seen.append(nx)
            
        # Check all possible positive cones P
        for choice in itertools.product([0, 1], repeat=len(pairs)):
            P = [zero]
            for i, c in enumerate(choice):
                P.append(pairs[i][c])
                
            # Check P + P \subseteq P
            add_ok = True
            for a in P:
                for b in P:
                    if R.add(a, b) not in P:
                        add_ok = False
                        break
                if not add_ok: break
            if not add_ok: continue
            
            # Check P * P \subseteq P
            mul_ok = True
            for a in P:
                for b in P:
                    if R.mul(a, b) not in P:
                        mul_ok = False
                        break
                if not mul_ok: break
            if not mul_ok: continue
            
            return True
            
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = is_boolean_ring(witness)
    except Exception:
        h1 = False
        
    try:
        neg_q = has_total_order(witness)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: There exists a total order on R that makes R an ordered ring"
]

N_HYP = 1
NEG_Q_INDEX = 1