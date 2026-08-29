import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness elements
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

def is_ideal(R, S):
    if not S: 
        return False
    
    try:
        zero = R.zero
        elements = list(R.elements)
    except (AttributeError, TypeError):
        return False
        
    if zero not in S: 
        return False
    
    S_list = []
    for x in S:
        if x not in S_list:
            S_list.append(x)
            
    # Check closure under addition
    for x in S_list:
        for y in S_list:
            if R.add(x, y) not in S_list: 
                return False
            
    # Check closure under multiplication with ring elements
    for x in S_list:
        for r in elements:
            if R.mul(r, x) not in S_list: 
                return False
            if R.mul(x, r) not in S_list: 
                return False
            
    # Check existence of additive inverses
    for x in S_list:
        has_inv = False
        for y in S_list:
            if R.add(x, y) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        
    return True

def product_ideal(R, I, J):
    products = []
    for i in I:
        for j in J:
            p = R.mul(i, j)
            if p not in products:
                products.append(p)
                
    gen = list(products)
    elements = list(R.elements)
    
    # Generate the ideal from the products
    for p in products:
        for r in elements:
            rp = R.mul(r, p)
            if rp not in gen: gen.append(rp)
            pr = R.mul(p, r)
            if pr not in gen: gen.append(pr)
            for s in elements:
                rps = R.mul(rp, s)
                if rps not in gen: gen.append(rps)
                
    closure = list(gen)
    if not closure:
        closure.append(R.zero)
        
    # Close under addition
    changed = True
    while changed:
        changed = False
        new_elements = []
        for x in closure:
            for y in closure:
                s = R.add(x, y)
                if s not in closure and s not in new_elements:
                    new_elements.append(s)
        if new_elements:
            closure.extend(new_elements)
            changed = True
            
    return closure

def is_nilpotent_ideal(R, I):
    if not is_ideal(R, I): 
        return False
    
    current_power = []
    for x in I:
        if x not in current_power:
            current_power.append(x)
            
    if not current_power:
        return True
        
    elements = list(R.elements)
    max_power = len(elements) + 1
    
    for _ in range(max_power):
        if all(x == R.zero for x in current_power):
            return True
            
        products = []
        for i in I:
            for x in current_power:
                p = R.mul(i, x)
                if p not in products:
                    products.append(p)
                    
        gen = list(products)
        for p in products:
            for r in elements:
                rp = R.mul(r, p)
                if rp not in gen: gen.append(rp)
                pr = R.mul(p, r)
                if pr not in gen: gen.append(pr)
                for s in elements:
                    rps = R.mul(rp, s)
                    if rps not in gen: gen.append(rps)
                    
        closure = list(gen)
        if not closure:
            closure.append(R.zero)
            
        changed = True
        while changed:
            changed = False
            new_elements = []
            for x in closure:
                for y in closure:
                    s = R.add(x, y)
                    if s not in closure and s not in new_elements:
                        new_elements.append(s)
            if new_elements:
                closure.extend(new_elements)
                changed = True
                
        current_power = closure
        
    return all(x == R.zero for x in current_power)

def is_commutative_ring(R):
    try:
        elements = list(R.elements)
        zero = R.zero
    except (AttributeError, TypeError):
        return False
        
    if len(elements) > 100:
        return False
        
    if zero not in elements: 
        return False
    
    for a in elements:
        if R.add(a, zero) != a: return False
        if R.add(zero, a) != a: return False
        
    for a in elements:
        for b in elements:
            ab_add = R.add(a, b)
            if ab_add not in elements: return False
            if ab_add != R.add(b, a): return False
            
            ab_mul = R.mul(a, b)
            if ab_mul not in elements: return False
            if ab_mul != R.mul(b, a): return False
            
            for c in elements:
                if R.add(ab_add, c) != R.add(a, R.add(b, c)): return False
                if R.mul(ab_mul, c) != R.mul(a, R.mul(b, c)): return False
                if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                
    for a in elements:
        has_inv = False
        for b in elements:
            if R.add(a, b) == zero:
                has_inv = True
                break
        if not has_inv: 
            return False
        
    return True

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            J = witness['J']
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_nilpotent_ideal(R, I)
    except Exception:
        h2 = False
        
    try:
        IJ = product_ideal(R, I, J)
        neg_q = not is_nilpotent_ideal(R, IJ)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a nilpotent ideal of R",
    "¬Q: The product ideal IJ is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2