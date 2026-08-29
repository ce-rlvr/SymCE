import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        R_elements = witness['R_elements']
        S_elements = witness['S_elements']
        R_add = witness['R_add']
        R_mul = witness['R_mul']
        R_zero = witness['R_zero']
        R_one = witness['R_one']
        S_add = witness['S_add']
        S_mul = witness['S_mul']
        S_zero = witness['S_zero']
        S_one = witness['S_one']
        f = witness['f']
        M_contains = witness['M_contains']
        M_maximal_witness = witness['M_maximal_witness']
    except Exception:
        return [False, False, False]

    # H1: R and S are commutative rings with identity
    def check_ring(elements, add, mul, zero, one):
        try:
            if not elements: 
                return False
            if zero not in elements or one not in elements: 
                return False
            for a in elements:
                if add(a, zero) != a: return False
                if add(zero, a) != a: return False
                if mul(a, one) != a: return False
                if mul(one, a) != a: return False
            for a in elements:
                for b in elements:
                    if add(a, b) != add(b, a): return False
                    if mul(a, b) != mul(b, a): return False
            for a in elements:
                for b in elements:
                    for c in elements:
                        if add(add(a, b), c) != add(a, add(b, c)): return False
                        if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
            for a in elements:
                for b in elements:
                    for c in elements:
                        if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
            return True
        except Exception:
            return False

    h1 = False
    try:
        if check_ring(R_elements, R_add, R_mul, R_zero, R_one) and \
           check_ring(S_elements, S_add, S_mul, S_zero, S_one):
            h1 = True
    except Exception:
        pass

    # H2: M is a maximal ideal of S
    h2 = False
    try:
        is_ideal = True
        if not M_contains(S_zero): is_ideal = False
        if M_contains(S_one): is_ideal = False
        for a in S_elements:
            for b in S_elements:
                if M_contains(a) and M_contains(b):
                    if not M_contains(S_add(a, b)): is_ideal = False
                if M_contains(a):
                    if not M_contains(S_mul(b, a)): is_ideal = False
        
        is_maximal = True
        for x in S_elements:
            if not M_contains(x):
                y, m = M_maximal_witness(x)
                if not M_contains(m): is_maximal = False
                if S_add(S_mul(x, y), m) != S_one: is_maximal = False
        
        if is_ideal and is_maximal:
            h2 = True
    except Exception:
        pass

    # neg_Q: The preimage of M under f is not a maximal ideal of R
    neg_q = False
    try:
        is_hom = True
        for a in R_elements:
            for b in R_elements:
                if f(R_add(a, b)) != S_add(f(a), f(b)): is_hom = False
                if f(R_mul(a, b)) != S_mul(f(a), f(b)): is_hom = False
        
        pre_M_is_proper = not M_contains(f(R_one))
        
        if not pre_M_is_proper:
            # If pre_M contains 1_R, it is the whole ring R, hence not a proper/maximal ideal.
            if is_hom:
                neg_q = True
        else:
            # If pre_M is proper, we verify it's not maximal by checking an intermediate ideal I.
            I_contains = witness['I_contains']
            I_element = witness['I_element']
            R_minus_I_element = witness['R_minus_I_element']
            
            is_I_ideal = True
            if not I_contains(R_zero): is_I_ideal = False
            if I_contains(R_one): is_I_ideal = False
            for a in R_elements:
                for b in R_elements:
                    if I_contains(a) and I_contains(b):
                        if not I_contains(R_add(a, b)): is_I_ideal = False
                    if I_contains(a):
                        if not I_contains(R_mul(b, a)): is_I_ideal = False
            
            pre_M_sub_I = True
            for a in R_elements:
                if M_contains(f(a)):
                    if not I_contains(a): pre_M_sub_I = False
            
            pre_M_neq_I = False
            if I_contains(I_element) and not M_contains(f(I_element)):
                pre_M_neq_I = True
                
            I_neq_R = False
            if not I_contains(R_minus_I_element):
                I_neq_R = True
                
            if is_hom and is_I_ideal and pre_M_sub_I and pre_M_neq_I and I_neq_R:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: M is a maximal ideal of S",
    "¬Q: The preimage of M under f is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2