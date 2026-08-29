import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import math
import functools

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            elements, add, mul, zero, one = witness
            elements = list(elements)
        else:
            elements = list(witness.elements)
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
    except Exception:
        return [False, False, False]

    # H1: R is a unital ring
    try:
        h1 = True
        if zero not in elements or one not in elements:
            h1 = False
        else:
            # Check closure and identity
            for a in elements:
                if add(a, zero) != a or add(zero, a) != a:
                    h1 = False
                    break
                if mul(a, one) != a or mul(one, a) != a:
                    h1 = False
                    break
                
                # Additive inverse
                has_inv = False
                for b in elements:
                    if add(a, b) == zero and add(b, a) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
            
            if h1:
                # Check 2D combinations (closure and commutativity of addition)
                for a in elements:
                    for b in elements:
                        if add(a, b) not in elements: 
                            h1 = False
                            break
                        if mul(a, b) not in elements: 
                            h1 = False
                            break
                        if add(a, b) != add(b, a): 
                            h1 = False
                            break
                    if not h1: 
                        break
            
            if h1:
                # Check 3D combinations (associativity and distributivity)
                for a in elements:
                    for b in elements:
                        ab = mul(a, b)
                        a_plus_b = add(a, b)
                        for c in elements:
                            if add(a, add(b, c)) != add(a_plus_b, c): 
                                h1 = False
                                break
                            if mul(a, mul(b, c)) != mul(ab, c): 
                                h1 = False
                                break
                            if mul(a, add(b, c)) != add(ab, mul(a, c)): 
                                h1 = False
                                break
                            if mul(a_plus_b, c) != add(mul(a, c), mul(b, c)): 
                                h1 = False
                                break
                        if not h1: 
                            break
                    if not h1: 
                        break
    except Exception:
        h1 = False

    # H2: U(R) denotes the group of units of R (Definition)
    h2 = True

    # Conclusion: Z(U(R)) == U(Z(R))
    try:
        # Compute U(R)
        units = []
        for a in elements:
            is_unit = False
            for b in elements:
                if mul(a, b) == one and mul(b, a) == one:
                    is_unit = True
                    break
            if is_unit:
                units.append(a)
        
        # Compute Z(R)
        z_r = []
        for a in elements:
            is_center = True
            for b in elements:
                if mul(a, b) != mul(b, a):
                    is_center = False
                    break
            if is_center:
                z_r.append(a)
        
        # Compute Z(U(R))
        z_u = []
        for u in units:
            is_center = True
            for v in units:
                if mul(u, v) != mul(v, u):
                    is_center = False
                    break
            if is_center:
                z_u.append(u)
                
        # Compute U(Z(R))
        u_z_r = []
        for a in z_r:
            is_unit = False
            for b in z_r:
                if mul(a, b) == one and mul(b, a) == one:
                    is_unit = True
                    break
            if is_unit:
                u_z_r.append(a)
                
        def is_subset(l1, l2):
            for x in l1:
                if x not in l2: 
                    return False
            return True
            
        q = is_subset(z_u, u_z_r) and is_subset(u_z_r, z_u)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unital ring",
    "H_2: U(R) denotes the group of units of R",
    "¬Q: Z(U(R)) is not equal to U(Z(R))"
]

N_HYP = 2
NEG_Q_INDEX = 2