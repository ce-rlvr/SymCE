import itertools
import functools
from sympy import QQ, ZZ
from sympy.abc import x, y, z

# Top-level setup
# (No specific named bindings required for RingTheory beyond QQ, ZZ, x, y, z)

def get_attr(witness, name):
    if isinstance(witness, dict):
        return witness[name]
    return getattr(witness, name)

def has_attr(witness, name):
    if isinstance(witness, dict):
        return name in witness
    return hasattr(witness, name)

def is_commutative_ring(elements, add, mul, zero):
    try:
        elements = list(elements)
        if zero not in elements: return False
        
        for a in elements:
            if add(a, zero) != a: return False
            if add(zero, a) != a: return False
            
            has_inv = False
            for b in elements:
                if add(a, b) == zero and add(b, a) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for b in elements:
                if add(a, b) not in elements: return False
                if add(a, b) != add(b, a): return False
                if mul(a, b) not in elements: return False
                if mul(a, b) != mul(b, a): return False
                
                for c in elements:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                    
        has_one = False
        for e in elements:
            is_one = True
            for a in elements:
                if mul(e, a) != a or mul(a, e) != a:
                    is_one = False
                    break
            if is_one:
                has_one = True
                break
        if not has_one: return False
        
        return True
    except Exception:
        return False

def is_homomorphism(elements_R, add_R, mul_R, elements_S, add_S, mul_S, f):
    try:
        one_R = None
        for e in elements_R:
            is_one = True
            for a in elements_R:
                if mul_R(e, a) != a or mul_R(a, e) != a:
                    is_one = False
                    break
            if is_one:
                one_R = e
                break
                
        one_S = None
        for e in elements_S:
            is_one = True
            for a in elements_S:
                if mul_S(e, a) != a or mul_S(a, e) != a:
                    is_one = False
                    break
            if is_one:
                one_S = e
                break
                
        if one_R is not None and one_S is not None:
            if f(one_R) != one_S: return False
            
        for a in elements_R:
            if f(a) not in elements_S: return False
            for b in elements_R:
                if f(add_R(a, b)) != add_S(f(a), f(b)): return False
                if f(mul_R(a, b)) != mul_S(f(a), f(b)): return False
        return True
    except Exception:
        return False

def is_ideal(subset, elements_R, add_R, mul_R, zero_R):
    try:
        if not subset: return False
        for a in subset:
            if a not in elements_R: return False
            for b in subset:
                neg_b = None
                for e in elements_R:
                    if add_R(b, e) == zero_R:
                        neg_b = e
                        break
                if neg_b is None: return False
                if add_R(a, neg_b) not in subset: return False
            for r in elements_R:
                if mul_R(r, a) not in subset: return False
        return True
    except Exception:
        return False

def ideal_generated_by(subset, elements_R, add_R, mul_R, zero_R):
    ideal = set()
    for x in subset:
        for r in elements_R:
            ideal.add(mul_R(r, x))
    
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for a in ideal:
            for b in ideal:
                s = add_R(a, b)
                if s not in ideal:
                    new_elements.add(s)
        if new_elements:
            ideal.update(new_elements)
            changed = True
    if not ideal:
        ideal.add(zero_R)
    return ideal

def extension(subset, elements_R, add_R, mul_R, zero_R, elements_S, add_S, mul_S, zero_S, f):
    if not is_ideal(subset, elements_R, add_R, mul_R, zero_R):
        raise ValueError("Extension is only defined for ideals")
    f_subset = {f(x) for x in subset}
    return ideal_generated_by(f_subset, elements_S, add_S, mul_S, zero_S)

def check_h1(witness):
    if has_attr(witness, 'is_commutative_ring_R'):
        return bool(get_attr(witness, 'is_commutative_ring_R'))
    return is_commutative_ring(
        get_attr(witness, 'R'),
        get_attr(witness, 'add_R'),
        get_attr(witness, 'mul_R'),
        get_attr(witness, 'zero_R')
    )

def check_h2(witness):
    if has_attr(witness, 'is_commutative_ring_S'):
        return bool(get_attr(witness, 'is_commutative_ring_S'))
    return is_commutative_ring(
        get_attr(witness, 'S'),
        get_attr(witness, 'add_S'),
        get_attr(witness, 'mul_S'),
        get_attr(witness, 'zero_S')
    )

def check_h3(witness):
    if has_attr(witness, 'is_ring_homomorphism_f'):
        return bool(get_attr(witness, 'is_ring_homomorphism_f'))
    return is_homomorphism(
        get_attr(witness, 'R'),
        get_attr(witness, 'add_R'),
        get_attr(witness, 'mul_R'),
        get_attr(witness, 'S'),
        get_attr(witness, 'add_S'),
        get_attr(witness, 'mul_S'),
        get_attr(witness, 'f')
    )

def check_h4(witness):
    if has_attr(witness, 'is_ideal_J'):
        return bool(get_attr(witness, 'is_ideal_J'))
    return is_ideal(
        get_attr(witness, 'J'),
        get_attr(witness, 'R'),
        get_attr(witness, 'add_R'),
        get_attr(witness, 'mul_R'),
        get_attr(witness, 'zero_R')
    )

def check_q(witness):
    if has_attr(witness, 'conclusion_holds'):
        return bool(get_attr(witness, 'conclusion_holds'))
    
    R = get_attr(witness, 'R')
    S = get_attr(witness, 'S')
    add_R = get_attr(witness, 'add_R')
    mul_R = get_attr(witness, 'mul_R')
    zero_R = get_attr(witness, 'zero_R')
    add_S = get_attr(witness, 'add_S')
    mul_S = get_attr(witness, 'mul_S')
    zero_S = get_attr(witness, 'zero_S')
    f = get_attr(witness, 'f')
    I = get_attr(witness, 'I')
    J = get_attr(witness, 'J')
    
    ij_set = {mul_R(i, j) for i in I for j in J}
    IJ = ideal_generated_by(ij_set, R, add_R, mul_R, zero_R)
    
    ext_IJ = extension(IJ, R, add_R, mul_R, zero_R, S, add_S, mul_S, zero_S, f)
    ext_I = extension(I, R, add_R, mul_R, zero_R, S, add_S, mul_S, zero_S, f)
    ext_J = extension(J, R, add_R, mul_R, zero_R, S, add_S, mul_S, zero_S, f)
    
    ext_I_ext_J_set = {mul_S(x, y) for x in ext_I for y in ext_J}
    ext_I_ext_J = ideal_generated_by(ext_I_ext_J_set, S, add_S, mul_S, zero_S)
    
    return set(ext_IJ) == set(ext_I_ext_J)

def conditions(witness) -> list[bool]:
    try:
        h1 = check_h1(witness)
    except Exception:
        h1 = False

    try:
        h2 = check_h2(witness)
    except Exception:
        h2 = False

    try:
        h3 = check_h3(witness)
    except Exception:
        h3 = False

    try:
        h4 = check_h4(witness)
    except Exception:
        h4 = False

    try:
        q = check_q(witness)
    except Exception:
        q = False

    neg_q = not q

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a commutative ring",
    "H_3: f is a ring homomorphism",
    "H_4: J is an ideal of R",
    "¬Q: (IJ)^e != I^e J^e"
]

N_HYP = 4
NEG_Q_INDEX = 4