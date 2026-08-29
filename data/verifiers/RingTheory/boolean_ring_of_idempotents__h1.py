import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

CONDITION_LABELS = [
    "H_1: Let B be the set of all idempotent elements of R",
    "H_2: Let addition on B be defined as x (+) y = x + y - 2xy",
    "H_3: Let multiplication on B be the standard multiplication inherited from R",
    "¬Q: B does not form a Boolean ring under (+) and standard multiplication"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = True
    except Exception:
        h2 = False
        
    try:
        h3 = True
    except Exception:
        h3 = False
        
    try:
        R = witness
        B = []
        for x in R:
            if x * x == x:
                B.append(x)
                
        is_ring = True
        
        # 1. Closure under (+)
        for x in B:
            for y in B:
                s = x + y - x*y - x*y
                if not any(s == b for b in B):
                    is_ring = False
                    break
            if not is_ring:
                break
                
        # 2. Closure under (*)
        if is_ring:
            for x in B:
                for y in B:
                    p = x * y
                    if not any(p == b for b in B):
                        is_ring = False
                        break
                if not is_ring:
                    break
                    
        # 3. Associativity of (+)
        if is_ring:
            for x in B:
                for y in B:
                    for z in B:
                        xy = x + y - x*y - x*y
                        xy_z = xy + z - xy*z - xy*z
                        
                        yz = y + z - y*z - y*z
                        x_yz = x + yz - x*yz - x*yz
                        
                        if xy_z != x_yz:
                            is_ring = False
                            break
                    if not is_ring:
                        break
                if not is_ring:
                    break
                    
        # 4. Commutativity of (+)
        if is_ring:
            for x in B:
                for y in B:
                    xy = x + y - x*y - x*y
                    yx = y + x - y*x - y*x
                    if xy != yx:
                        is_ring = False
                        break
                if not is_ring:
                    break
                    
        # 5. Identity for (+)
        identity = None
        if is_ring:
            for e in B:
                is_id = True
                for x in B:
                    ex = e + x - e*x - e*x
                    xe = x + e - x*e - x*e
                    if ex != x or xe != x:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
            if identity is None:
                is_ring = False
                
        # 6. Inverses for (+)
        if is_ring:
            for x in B:
                has_inv = False
                for y in B:
                    xy = x + y - x*y - x*y
                    yx = y + x - y*x - y*x
                    if xy == identity and yx == identity:
                        has_inv = True
                        break
                if not has_inv:
                    is_ring = False
                    break
                        
        # 7. Associativity of (*)
        if is_ring:
            for x in B:
                for y in B:
                    for z in B:
                        if (x*y)*z != x*(y*z):
                            is_ring = False
                            break
                    if not is_ring:
                        break
                if not is_ring:
                    break
                    
        # 8. Distributivity
        if is_ring:
            for x in B:
                for y in B:
                    for z in B:
                        yz = y + z - y*z - y*z
                        lhs1 = x * yz
                        xy = x * y
                        xz = x * z
                        rhs1 = xy + xz - xy*xz - xy*xz
                        if lhs1 != rhs1:
                            is_ring = False
                            break
                            
                        xy_plus = x + y - x*y - x*y
                        lhs2 = xy_plus * z
                        xz = x * z
                        yz_mul = y * z
                        rhs2 = xz + yz_mul - xz*yz_mul - xz*yz_mul
                        if lhs2 != rhs2:
                            is_ring = False
                            break
                    if not is_ring:
                        break
                if not is_ring:
                    break
                    
        neg_q = not is_ring
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]