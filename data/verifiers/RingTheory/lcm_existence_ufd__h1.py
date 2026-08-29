import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import itertools
import functools
import math
import z3

# Top-level setup for Ring Theory
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Expected witness format:
    witness = (elements, add_func, mul_func, zero, a, b)
    where:
      - elements: list or tuple of ring elements
      - add_func: callable f(x, y) returning x + y
      - mul_func: callable f(x, y) returning x * y
      - zero: the additive identity element
      - a, b: the non-zero elements to test
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 6:
            return [False, False]
            
        elements, add_func, mul_func, zero, a, b = witness
        elements = list(elements)
        n = len(elements)
        if n == 0 or n > 1000:
            return [False, False]
            
        try:
            elem_to_idx = {elements[i]: i for i in range(n)}
            fast_lookup = True
        except TypeError:
            fast_lookup = False

        def is_in_elements(val):
            if fast_lookup:
                return val in elem_to_idx
            else:
                return val in elements

        if not is_in_elements(a) or not is_in_elements(b):
            return [False, False]
        if a == zero or b == zero:
            return [False, False]
            
        # Check zero identity
        for e in elements:
            if add_func(e, zero) != e or add_func(zero, e) != e:
                return [False, False]
                
        # Check add commutativity and closure
        for i in range(n):
            e1 = elements[i]
            for j in range(i, n):
                e2 = elements[j]
                s1 = add_func(e1, e2)
                s2 = add_func(e2, e1)
                if s1 != s2: return [False, False]
                if not is_in_elements(s1): return [False, False]
                
        # Check add inverses
        for e1 in elements:
            has_inv = False
            for e2 in elements:
                if add_func(e1, e2) == zero:
                    has_inv = True
                    break
            if not has_inv: return [False, False]
            
        # Check mul closure and commutativity
        for i in range(n):
            e1 = elements[i]
            for j in range(i, n):
                e2 = elements[j]
                p1 = mul_func(e1, e2)
                p2 = mul_func(e2, e1)
                if p1 != p2: return [False, False]
                if not is_in_elements(p1): return [False, False]
                
        # Check multiplicative identity
        has_one = False
        for e in elements:
            is_one = True
            for e1 in elements:
                if mul_func(e, e1) != e1:
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return [False, False]
        
        # Check associativity and distributivity (subset if large)
        if n > 100:
            step = n // 50
            subset = elements[::step][:50]
        else:
            subset = elements
            
        for e1 in subset:
            for e2 in subset:
                for e3 in subset:
                    if add_func(add_func(e1, e2), e3) != add_func(e1, add_func(e2, e3)): return [False, False]
                    if mul_func(mul_func(e1, e2), e3) != mul_func(e1, mul_func(e2, e3)): return [False, False]
                    if mul_func(e1, add_func(e2, e3)) != add_func(mul_func(e1, e2), mul_func(e1, e3)): return [False, False]
                    
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            multiples = {i: set() for i in range(n)}
            for i in range(n):
                for j in range(n):
                    prod = mul_func(elements[i], elements[j])
                    if fast_lookup:
                        prod_idx = elem_to_idx[prod]
                    else:
                        prod_idx = elements.index(prod)
                    multiples[i].add(prod_idx)
                    
            if fast_lookup:
                a_idx = elem_to_idx[a]
                b_idx = elem_to_idx[b]
            else:
                a_idx = elements.index(a)
                b_idx = elements.index(b)
            
            def divides(idx_x, idx_y):
                return idx_y in multiples[idx_x]

            common_multiples = []
            for m in range(n):
                if divides(a_idx, m) and divides(b_idx, m):
                    common_multiples.append(m)
                    
            has_lcm = False
            for m in common_multiples:
                m_is_lcm = True
                for c in common_multiples:
                    if not divides(m, c):
                        m_is_lcm = False
                        break
                if m_is_lcm:
                    has_lcm = True
                    break
                    
            neg_q = not has_lcm
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "¬Q: a and b do not have a least common multiple in R"
]

N_HYP = 1
NEG_Q_INDEX = 1