import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
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

def get_field(witness, field, default=None):
    if isinstance(witness, dict):
        return witness.get(field, default)
    else:
        return getattr(witness, field, default)

def safe_list(iterable, max_len=100):
    if iterable is None:
        return None
    lst = []
    for i, e in enumerate(iterable):
        if i >= max_len:
            return None
        lst.append(e)
    return lst

def is_local_ring(elements, add, mul, zero, one, m):
    try:
        if zero not in elements or one not in elements:
            return False
            
        if one == zero: 
            return False
            
        # 1. Abelian group
        for a in elements:
            if add(a, zero) != a or add(zero, a) != a: return False
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in elements:
                if add(a, b) != add(b, a): return False
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False

        # 2. Commutative monoid
        for a in elements:
            if mul(a, one) != a or mul(one, a) != a: return False
            for b in elements:
                if mul(a, b) != mul(b, a): return False
                for c in elements:
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False

        # 3. Distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False

        # Find units
        units = []
        for a in elements:
            is_unit = False
            for b in elements:
                if mul(a, b) == one:
                    is_unit = True
                    break
            if is_unit:
                units.append(a)
                
        non_units = [a for a in elements if a not in units]
        
        # Check if non_units form an ideal
        for a in non_units:
            for b in non_units:
                if add(a, b) not in non_units: return False
                
        for a in non_units:
            for r in elements:
                if mul(a, r) not in non_units: return False
                
        # Check if m is exactly the non_units
        for x in m:
            if x not in non_units: return False
        for x in non_units:
            if x not in m: return False
            
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        R_raw = get_field(witness, 'R')
        S_raw = get_field(witness, 'S')
        m_R_raw = get_field(witness, 'm_R')
        m_S_raw = get_field(witness, 'm_S')
        f = get_field(witness, 'f')
        
        R = safe_list(R_raw)
        S = safe_list(S_raw)
        m_R = safe_list(m_R_raw)
        m_S = safe_list(m_S_raw)
        
        if R is None or S is None or m_R is None or m_S is None or f is None:
            return [False, False]
            
        add_R = get_field(witness, 'add_R', lambda a, b: a + b)
        mul_R = get_field(witness, 'mul_R', lambda a, b: a * b)
        zero_R = get_field(witness, 'zero_R', 0)
        one_R = get_field(witness, 'one_R', 1)
        
        add_S = get_field(witness, 'add_S', lambda a, b: a + b)
        mul_S = get_field(witness, 'mul_S', lambda a, b: a * b)
        zero_S = get_field(witness, 'zero_S', 0)
        one_S = get_field(witness, 'one_S', 1)
        
    except Exception:
        return [False, False]
        
    # H1: R and S are local rings with maximal ideals m_R and m_S respectively.
    try:
        h1 = is_local_ring(R, add_R, mul_R, zero_R, one_R, m_R) and \
             is_local_ring(S, add_S, mul_S, zero_S, one_S, m_S)
             
        if h1:
            # check if f is a function from R to S
            for x in R:
                val = f[x] if isinstance(f, dict) else f(x)
                if val not in S:
                    h1 = False
                    break
    except Exception:
        h1 = False
        
    # neg_Q: f^{-1}(m_S) != m_R
    try:
        preimage = []
        for x in R:
            val = f[x] if isinstance(f, dict) else f(x)
            if val in m_S:
                preimage.append(x)
                
        # check if preimage == m_R
        is_equal = True
        for x in preimage:
            if x not in m_R:
                is_equal = False
                break
        for x in m_R:
            if x not in preimage:
                is_equal = False
                break
        neg_q = not is_equal
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are local rings with maximal ideals m_R and m_S respectively",
    "¬Q: The preimage f^{-1}(m_S) is not equal to m_R"
]

N_HYP = 1
NEG_Q_INDEX = 1