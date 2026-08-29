import itertools

class FiniteRing:
    def __init__(self, elements, add, mul, zero, one):
        self.elements = elements
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one

def make_Zn(n):
    return FiniteRing(
        elements=list(range(n)),
        add=lambda x, y: (x + y) % n,
        mul=lambda x, y: (x * y) % n,
        zero=0,
        one=1 % n
    )

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)

# M2(F2): The ring of 2x2 matrices over the finite field of 2 elements.
# This is the standard counterexample for the false conjecture.
elements_M2_F2 = list(itertools.product([0, 1], repeat=4))

def add_M2_F2(x, y):
    return tuple((x[i] + y[i]) % 2 for i in range(4))

def mul_M2_F2(x, y):
    return (
        (x[0]*y[0] + x[1]*y[2]) % 2,
        (x[0]*y[1] + x[1]*y[3]) % 2,
        (x[2]*y[0] + x[3]*y[2]) % 2,
        (x[2]*y[1] + x[3]*y[3]) % 2
    )

M2_F2 = FiniteRing(
    elements=elements_M2_F2,
    add=add_M2_F2,
    mul=mul_M2_F2,
    zero=(0, 0, 0, 0),
    one=(1, 0, 0, 1)
)

def is_finite_ring(R):
    try:
        elements = R.elements
        if not elements: return False
        n = len(elements)
        if n > 100: return False  # Keep it fast
        
        zero = R.zero
        one = R.one
        add = R.add
        mul = R.mul
        
        if zero not in elements or one not in elements: return False
        
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
                ab_add = add(a, b)
                ab_mul = mul(a, b)
                if ab_add not in elements: return False
                if ab_mul not in elements: return False
                
                if ab_add != add(b, a): return False
                
                for c in elements:
                    if add(ab_add, c) != add(a, add(b, c)): return False
                    if mul(ab_mul, c) != mul(a, mul(b, c)): return False
                    
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
                    
        return True
    except Exception:
        return False

def is_direct_product_of_local_rings(R):
    try:
        elements = R.elements
        add = R.add
        mul = R.mul
        zero = R.zero
        one = R.one
        
        if zero == one:
            return True
            
        # Find all central idempotents
        central_idempotents = []
        for e in elements:
            if mul(e, e) == e:
                is_central = True
                for x in elements:
                    if mul(e, x) != mul(x, e):
                        is_central = False
                        break
                if is_central:
                    central_idempotents.append(e)
                    
        # Find primitive central idempotents
        primitive_central_idempotents = []
        for e in central_idempotents:
            if e == zero: continue
            is_primitive = True
            for f in central_idempotents:
                if f == zero or f == e: continue
                if mul(f, e) == f:
                    is_primitive = False
                    break
            if is_primitive:
                primitive_central_idempotents.append(e)
                
        # Check if each component R_e is a local ring
        for e in primitive_central_idempotents:
            Re_elements = []
            for x in elements:
                xe = mul(x, e)
                if xe not in Re_elements:
                    Re_elements.append(xe)
                    
            units = []
            non_units = []
            for y in Re_elements:
                is_unit = False
                for z in Re_elements:
                    if mul(y, z) == e and mul(z, y) == e:
                        is_unit = True
                        break
                if is_unit:
                    units.append(y)
                else:
                    non_units.append(y)
                    
            # A finite ring is local iff the set of non-units is closed under addition
            for a in non_units:
                for b in non_units:
                    if add(a, b) not in non_units:
                        return False
                        
        return True
    except Exception:
        return False

def conditions(witness):
    h1 = is_finite_ring(witness)
    
    if h1:
        neg_q = not is_direct_product_of_local_rings(witness)
    else:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a finite ring",
    "¬Q: R is not isomorphic to a finite direct product of finite local rings"
]

N_HYP = 1
NEG_Q_INDEX = 1