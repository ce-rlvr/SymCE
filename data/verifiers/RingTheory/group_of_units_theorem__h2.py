import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # H1: R is a ring
    h1_ok = False
    try:
        elements = list(witness.elements)
        add = witness.add
        mul = witness.mul
        
        is_ring = True
        if not elements:
            is_ring = False
        else:
            # Check for duplicates in elements
            for i, x in enumerate(elements):
                if x in elements[:i]:
                    is_ring = False
            
            if is_ring:
                # Closure under addition and multiplication
                for x in elements:
                    for y in elements:
                        if add(x, y) not in elements: is_ring = False
                        if mul(x, y) not in elements: is_ring = False
            
            if is_ring:
                # Commutativity of addition
                for x in elements:
                    for y in elements:
                        if add(x, y) != add(y, x): is_ring = False
                        
            if is_ring:
                # Associativity of addition and multiplication
                for x, y, z in itertools.product(elements, repeat=3):
                    if add(add(x, y), z) != add(x, add(y, z)): is_ring = False
                    if mul(mul(x, y), z) != mul(x, mul(y, z)): is_ring = False
                    
            if is_ring:
                # Additive identity
                zero = None
                for e in elements:
                    if all(add(e, x) == x for x in elements):
                        zero = e
                        break
                if zero is None:
                    is_ring = False
                else:
                    # Additive inverses
                    for x in elements:
                        if not any(add(x, y) == zero for y in elements):
                            is_ring = False
                            
            if is_ring:
                # Distributivity
                for x, y, z in itertools.product(elements, repeat=3):
                    if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): is_ring = False
                    if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): is_ring = False
                    
        h1_ok = is_ring
    except Exception:
        h1_ok = False

    # H2: U(R) is the set of all elements in R that have a two-sided multiplicative inverse
    h2_ok = False
    try:
        elements = list(witness.elements)
        mul = witness.mul
        
        # Find multiplicative identity of R (if it exists)
        id_R = None
        for e in elements:
            if all(mul(e, x) == x and mul(x, e) == x for x in elements):
                id_R = e
                break
                
        expected_U_R = []
        if id_R is not None:
            for x in elements:
                has_inv = False
                for y in elements:
                    if mul(x, y) == id_R and mul(y, x) == id_R:
                        has_inv = True
                        break
                if has_inv:
                    if x not in expected_U_R:
                        expected_U_R.append(x)
                    
        U_R = list(witness.U_R)
        
        u_r_valid = True
        for x in U_R:
            if x not in expected_U_R:
                u_r_valid = False
        for x in expected_U_R:
            if x not in U_R:
                u_r_valid = False
        for i, x in enumerate(U_R):
            if x in U_R[:i]:
                u_r_valid = False
                
        if u_r_valid:
            h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: U(R) does NOT form a group under ring multiplication
    neg_q_ok = False
    try:
        U_R = list(witness.U_R)
        mul = witness.mul
        
        is_group = True
        if not U_R:
            is_group = False
        else:
            # Closure
            for x in U_R:
                for y in U_R:
                    if mul(x, y) not in U_R:
                        is_group = False
            
            if is_group:
                # Associativity
                for x, y, z in itertools.product(U_R, repeat=3):
                    if mul(mul(x, y), z) != mul(x, mul(y, z)):
                        is_group = False
                        
            if is_group:
                # Identity in U(R)
                id_U = None
                for e in U_R:
                    if all(mul(e, x) == x and mul(x, e) == x for x in U_R):
                        id_U = e
                        break
                if id_U is None:
                    is_group = False
                else:
                    # Inverses in U(R)
                    for x in U_R:
                        has_inv = False
                        for y in U_R:
                            if mul(x, y) == id_U and mul(y, x) == id_U:
                                has_inv = True
                                break
                        if not has_inv:
                            is_group = False
                            
        neg_q_ok = not is_group
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: U(R) is the set of all elements in R that have a two-sided multiplicative inverse",
    "¬Q: U(R) does not form a group under ring multiplication"
]

N_HYP = 2
NEG_Q_INDEX = 2