import sympy
import itertools
import functools

# Top-level setup
Z = sympy.ZZ
Q = sympy.QQ

def evaluate_op(op, a, b, elements):
    if callable(op):
        return op(a, b)
    if isinstance(op, dict):
        if (a, b) in op: return op[(a, b)]
        if str((a, b)) in op: return op[str((a, b))]
    if isinstance(op, list):
        i = elements.index(a)
        j = elements.index(b)
        return op[i][j]
    raise ValueError("Unknown operation format")

def is_integral_domain(elements, add, mul):
    if not elements: 
        return False
    
    # Check closure
    for a in elements:
        for b in elements:
            try:
                sum_ab = evaluate_op(add, a, b, elements)
                prod_ab = evaluate_op(mul, a, b, elements)
            except Exception:
                return False
            if sum_ab not in elements: return False
            if prod_ab not in elements: return False

    # Commutativity of add and mul
    for a in elements:
        for b in elements:
            if evaluate_op(add, a, b, elements) != evaluate_op(add, b, a, elements): return False
            if evaluate_op(mul, a, b, elements) != evaluate_op(mul, b, a, elements): return False

    # Associativity and distributivity
    for a in elements:
        for b in elements:
            for c in elements:
                ab = evaluate_op(add, a, b, elements)
                bc = evaluate_op(add, b, c, elements)
                if evaluate_op(add, ab, c, elements) != evaluate_op(add, a, bc, elements): return False
                
                ab_m = evaluate_op(mul, a, b, elements)
                bc_m = evaluate_op(mul, b, c, elements)
                if evaluate_op(mul, ab_m, c, elements) != evaluate_op(mul, a, bc_m, elements): return False
                
                # Distributivity
                a_bc = evaluate_op(mul, a, bc, elements)
                ab_ac = evaluate_op(add, ab_m, evaluate_op(mul, a, c, elements), elements)
                if a_bc != ab_ac: return False

    # Find zero
    zeros = []
    for z in elements:
        if all(evaluate_op(add, z, a, elements) == a for a in elements):
            if z not in zeros:
                zeros.append(z)
    if len(zeros) != 1: return False
    zero = zeros[0]

    # Check additive inverses
    for a in elements:
        if not any(evaluate_op(add, a, b, elements) == zero for b in elements): return False

    # Find one
    ones = []
    for o in elements:
        if all(evaluate_op(mul, o, a, elements) == a for a in elements):
            if o not in ones:
                ones.append(o)
    if len(ones) != 1: return False
    one = ones[0]

    # Integral domain requires 1 != 0
    if one == zero: return False

    # Check no zero divisors
    for a in elements:
        for b in elements:
            if evaluate_op(mul, a, b, elements) == zero:
                if a != zero and b != zero:
                    return False

    return True

def is_subring(R_elements, add, mul, S_elements):
    if not S_elements: return False
    
    # S must be a subset of R
    for s in S_elements:
        if s not in R_elements: return False
    
    # Find zero of R
    zeros = []
    for z in R_elements:
        if all(evaluate_op(add, z, a, R_elements) == a for a in R_elements):
            if z not in zeros:
                zeros.append(z)
    if len(zeros) != 1: return False
    zero = zeros[0]

    # Subring must contain the zero element
    if zero not in S_elements: return False

    # Check closure under add, mul, and additive inverse
    for a in S_elements:
        for b in S_elements:
            if evaluate_op(add, a, b, R_elements) not in S_elements: return False
            if evaluate_op(mul, a, b, R_elements) not in S_elements: return False
        
        has_inv = False
        for b in S_elements:
            if evaluate_op(add, a, b, R_elements) == zero:
                has_inv = True
                break
        if not has_inv: return False

    return True

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        R_elements = witness.get("R_elements")
        R_add = witness.get("R_add")
        R_mul = witness.get("R_mul")
        S_elements = witness.get("S_elements")
    else:
        R_elements = getattr(witness, "R_elements", None)
        R_add = getattr(witness, "R_add", None)
        R_mul = getattr(witness, "R_mul", None)
        S_elements = getattr(witness, "S_elements", None)
        
    if R_elements is None or R_add is None or R_mul is None or S_elements is None:
        return [False, False, False]
        
    try:
        h1 = bool(is_integral_domain(R_elements, R_add, R_mul))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_subring(R_elements, R_add, R_mul, S_elements))
    except Exception:
        h2 = False
        
    try:
        def s_add(a, b):
            return evaluate_op(R_add, a, b, R_elements)
            
        def s_mul(a, b):
            return evaluate_op(R_mul, a, b, R_elements)
            
        q = bool(is_integral_domain(S_elements, s_add, s_mul))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: S is a subring of R",
    "¬Q: S is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2