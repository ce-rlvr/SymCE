import sympy
from sympy.matrices import eye, zeros

# Standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def default_add(a, b): return a + b
def default_mul(a, b): return a * b

def get_ops(witness, prefix):
    add = getattr(witness, f'add_{prefix}', default_add)
    mul = getattr(witness, f'mul_{prefix}', default_mul)
    return add, mul

def get_elements(witness, prefix):
    ring = getattr(witness, prefix, None)
    if isinstance(ring, (list, tuple, set)):
        return list(ring)
    if hasattr(witness, f'{prefix}_elements'):
        return list(getattr(witness, f'{prefix}_elements'))
    if hasattr(ring, 'elements'):
        try:
            return list(ring.elements)
        except Exception:
            pass
    if ring in (sympy.ZZ, sympy.QQ):
        return list(range(-5, 6))
    return None

def check_finite_comm_ring(elements, add, mul):
    if not elements: return False
    
    # closure
    for a in elements:
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
            
    # commutativity
    for a in elements:
        for b in elements:
            if add(a, b) != add(b, a): return False
            if mul(a, b) != mul(b, a): return False
            
    # associativity
    for a in elements:
        for b in elements:
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                
    # distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                
    # zero
    zeros_list = []
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zeros_list.append(z)
    if len(zeros_list) != 1: return False
    z = zeros_list[0]
    
    # inverses
    for a in elements:
        if not any(add(a, b) == z for b in elements): return False
        
    return True

def is_comm_ring(witness, prefix):
    try:
        ring = getattr(witness, prefix, None)
        
        if ring in (sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC):
            return True
        if hasattr(ring, 'is_commutative') and hasattr(ring, 'is_Ring'):
            if ring.is_commutative and ring.is_Ring:
                return True
                
        elements = get_elements(witness, prefix)
        if elements is None:
            return False
            
        add, mul = get_ops(witness, prefix)
        return check_finite_comm_ring(elements, add, mul)
    except Exception:
        return False

def check_homomorphism(witness):
    try:
        phi = witness.phi
        R_elements = get_elements(witness, 'R')
        S_elements = get_elements(witness, 'S')
        ring_S = getattr(witness, 'S', None)
        
        add_R, mul_R = get_ops(witness, 'R')
        add_S, mul_S = get_ops(witness, 'S')
        
        if R_elements is None:
            R_elements = list(range(-5, 6))
            
        for a in R_elements:
            pa = phi(a)
            
            if ring_S is not None and hasattr(ring_S, '__contains__'):
                if pa not in ring_S: return False
            elif S_elements is not None:
                if pa not in S_elements: return False
                
            for b in R_elements:
                v1 = phi(add_R(a, b))
                v2 = add_S(pa, phi(b))
                if v1 != v2:
                    if isinstance(v1, sympy.Expr) or isinstance(v2, sympy.Expr):
                        if sympy.simplify(v1 - v2) != 0: return False
                    else:
                        return False
                        
                v3 = phi(mul_R(a, b))
                v4 = mul_S(pa, phi(b))
                if v3 != v4:
                    if isinstance(v3, sympy.Expr) or isinstance(v4, sympy.Expr):
                        if sympy.simplify(v3 - v4) != 0: return False
                    else:
                        return False
        return True
    except Exception:
        return False

def get_identity(elements, mul):
    for e in elements:
        try:
            if all(mul(e, a) == a and mul(a, e) == a for a in elements):
                return e
        except Exception:
            continue
    return None

def conclusion_fails(witness):
    try:
        R_elements = get_elements(witness, 'R')
        S_elements = get_elements(witness, 'S')
        ring_S = getattr(witness, 'S', None)
        
        add_R, mul_R = get_ops(witness, 'R')
        add_S, mul_S = get_ops(witness, 'S')
        phi = witness.phi
        s = witness.s
        
        # Check if s is in S
        if ring_S is not None and hasattr(ring_S, '__contains__'):
            if s not in ring_S: return True
        elif S_elements is not None:
            if s not in S_elements: return True
            
        if R_elements is not None:
            id_R = get_identity(R_elements, mul_R)
        else:
            id_R = 1
            
        if id_R is None:
            return True
            
        phi_1 = phi(id_R)
        expected_s = mul_S(phi_1, s)
        
        if expected_s != s:
            if isinstance(expected_s, sympy.Expr) or isinstance(s, sympy.Expr):
                try:
                    if sympy.simplify(expected_s - s) != 0:
                        return True
                    else:
                        return False
                except Exception:
                    pass
            return True
            
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_comm_ring(witness, 'R') and is_comm_ring(witness, 'S')
    except Exception:
        h1 = False
        
    try:
        h2 = check_homomorphism(witness)
    except Exception:
        h2 = False
        
    try:
        neg_q = conclusion_fails(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: phi is a ring homomorphism from R to S",
    "¬Q: There does not exist a unique ring homomorphism Phi from the polynomial ring over R to S such that Phi(r) = phi(r) for all r in R and Phi(x) = s"
]

N_HYP = 2
NEG_Q_INDEX = 2