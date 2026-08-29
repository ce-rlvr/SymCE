import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def parse_ring(ring_data):
    if isinstance(ring_data, int):
        n = ring_data
        if n < 1:
            raise ValueError("Ring modulus must be at least 1")
        elements = list(range(n))
        add = lambda x, y: (x + y) % n
        mul = lambda x, y: (x * y) % n
        zero = 0
        return elements, add, mul, zero
    else:
        elements, add_dict, mul_dict, zero = ring_data
        
        if callable(add_dict):
            add = add_dict
        else:
            add = lambda x, y: add_dict[(x, y)]
            
        if callable(mul_dict):
            mul = mul_dict
        else:
            mul = lambda x, y: mul_dict[(x, y)]
            
        return elements, add, mul, zero

def is_commutative_ring(elements, add, mul, zero):
    try:
        # Check closure and commutativity
        for a in elements:
            for b in elements:
                s = add(a, b)
                p = mul(a, b)
                if s not in elements: return False
                if p not in elements: return False
                if s != add(b, a): return False
                if p != mul(b, a): return False
        
        # Check associativity and distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
        
        # Check additive identity (zero)
        for a in elements:
            if add(a, zero) != a: return False
            
        # Check additive inverses
        for a in elements:
            has_inv = False
            for b in elements:
                if add(a, b) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Check multiplicative identity
        has_one = False
        for e in elements:
            is_one = True
            for a in elements:
                if mul(a, e) != a or mul(e, a) != a:
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return False
            
        return True
    except Exception:
        return False

def get_nilradical(elements, mul, zero):
    nilradical = []
    for x in elements:
        curr = x
        is_nil = False
        for _ in range(len(elements)):
            if curr == zero:
                is_nil = True
                break
            curr = mul(curr, x)
        if is_nil:
            nilradical.append(x)
    return nilradical

def evaluate_f(f, x):
    if callable(f):
        return f(x)
    else:
        return f[x]

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R_data = witness['R']
            S_data = witness['S']
            f = witness['f']
        else:
            R_data, S_data, f = witness
    except Exception:
        return [False, False, False]
        
    try:
        R_elements, R_add, R_mul, R_zero = parse_ring(R_data)
        S_elements, S_add, S_mul, S_zero = parse_ring(S_data)
        
        h1 = is_commutative_ring(R_elements, R_add, R_mul, R_zero) and \
             is_commutative_ring(S_elements, S_add, S_mul, S_zero)
    except Exception:
        h1 = False

    try:
        actual_Nil_R = get_nilradical(R_elements, R_mul, R_zero)
        actual_Nil_S = get_nilradical(S_elements, S_mul, S_zero)
        
        if isinstance(witness, dict) and 'Nil_R' in witness and 'Nil_S' in witness:
            h2 = (len(witness['Nil_R']) == len(actual_Nil_R) and all(x in actual_Nil_R for x in witness['Nil_R'])) and \
                 (len(witness['Nil_S']) == len(actual_Nil_S) and all(x in actual_Nil_S for x in witness['Nil_S']))
        else:
            h2 = True
    except Exception:
        h2 = False

    try:
        actual_Nil_R = get_nilradical(R_elements, R_mul, R_zero)
        actual_Nil_S = get_nilradical(S_elements, S_mul, S_zero)
        
        # Check if f is a well-defined function from R to S
        for x in R_elements:
            if evaluate_f(f, x) not in S_elements:
                raise ValueError("f is not a function from R to S")
                
        neg_q = False
        for x in actual_Nil_R:
            fx = evaluate_f(f, x)
            if fx not in actual_Nil_S:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings",
    "H_2: Nil(R) and Nil(S) denote the nilradicals of R and S, respectively",
    "¬Q: f(Nil(R)) is not a subset of Nil(S)"
]

N_HYP = 2
NEG_Q_INDEX = 2