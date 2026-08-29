import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def get_field(witness, field):
    if isinstance(witness, dict):
        return witness[field]
    else:
        return getattr(witness, field)

def evaluate_op(op, a, b):
    if callable(op):
        return op(a, b)
    elif isinstance(op, dict):
        return op[(a, b)]
    else:
        return op[a][b]

def evaluate_unary(f, a):
    if callable(f):
        return f(a)
    elif isinstance(f, dict):
        return f[a]
    else:
        return f[a]

def is_comm_ring_with_id(elements, add, mul, zero, one):
    try:
        elements = list(elements)
        if zero not in elements or one not in elements: return False
        for a in elements:
            if evaluate_op(add, a, zero) != a or evaluate_op(add, zero, a) != a: return False
            if evaluate_op(mul, a, one) != a or evaluate_op(mul, one, a) != a: return False
            has_inv = False
            for b in elements:
                if evaluate_op(add, a, b) == zero and evaluate_op(add, b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elements:
                ab_add = evaluate_op(add, a, b)
                ba_add = evaluate_op(add, b, a)
                if ab_add != ba_add: return False
                if ab_add not in elements: return False
                
                ab_mul = evaluate_op(mul, a, b)
                ba_mul = evaluate_op(mul, b, a)
                if ab_mul != ba_mul: return False
                if ab_mul not in elements: return False
                
                for c in elements:
                    if evaluate_op(add, ab_add, c) != evaluate_op(add, a, evaluate_op(add, b, c)): return False
                    if evaluate_op(mul, ab_mul, c) != evaluate_op(mul, a, evaluate_op(mul, b, c)): return False
                    
                    bc_add = evaluate_op(add, b, c)
                    if evaluate_op(mul, a, bc_add) != evaluate_op(add, ab_mul, evaluate_op(mul, a, c)): return False
        return True
    except Exception:
        return False

def is_prime_ideal(elements, add, mul, zero, one, P):
    try:
        P = list(P)
        if zero not in P: return False
        if one in P: return False # Proper ideal
        
        # Additive subgroup
        for a in P:
            for b in P:
                if evaluate_op(add, a, b) not in P: return False
            has_inv = False
            for b in P:
                if evaluate_op(add, a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Ideal property
        for r in elements:
            for a in P:
                if evaluate_op(mul, r, a) not in P: return False
                if evaluate_op(mul, a, r) not in P: return False
                
        # Prime property
        for a in elements:
            for b in elements:
                if evaluate_op(mul, a, b) in P:
                    if a not in P and b not in P:
                        return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    """
    Expected witness format:
    A dictionary or object with the following keys/attributes:
    'R_elements', 'R_add', 'R_mul', 'R_zero', 'R_one'
    'S_elements', 'S_add', 'S_mul', 'S_zero', 'S_one'
    'P' (list of elements in S)
    'f' (callable, dict, or list mapping R_elements to S_elements)
    """
    try:
        R_elements = get_field(witness, 'R_elements')
        R_add = get_field(witness, 'R_add')
        R_mul = get_field(witness, 'R_mul')
        R_zero = get_field(witness, 'R_zero')
        R_one = get_field(witness, 'R_one')
        
        S_elements = get_field(witness, 'S_elements')
        S_add = get_field(witness, 'S_add')
        S_mul = get_field(witness, 'S_mul')
        S_zero = get_field(witness, 'S_zero')
        S_one = get_field(witness, 'S_one')
        
        P = get_field(witness, 'P')
        f = get_field(witness, 'f')
    except Exception:
        return [False, False, False]

    # H_1: R and S are commutative rings with identity
    try:
        h1 = is_comm_ring_with_id(R_elements, R_add, R_mul, R_zero, R_one) and \
             is_comm_ring_with_id(S_elements, S_add, S_mul, S_zero, S_one)
    except Exception:
        h1 = False

    # H_2: P is a prime ideal of S
    try:
        h2 = is_prime_ideal(S_elements, S_add, S_mul, S_zero, S_one, P)
    except Exception:
        h2 = False

    # ¬Q: The preimage f^{-1}(P) is not a prime ideal of R
    try:
        preimage = []
        for r in R_elements:
            if evaluate_unary(f, r) in P:
                preimage.append(r)
        
        q = is_prime_ideal(R_elements, R_add, R_mul, R_zero, R_one, preimage)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: P is a prime ideal of S",
    "¬Q: The preimage f^{-1}(P) is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2