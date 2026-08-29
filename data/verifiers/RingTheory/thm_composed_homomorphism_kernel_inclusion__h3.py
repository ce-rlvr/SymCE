import sympy
import itertools
import functools

# Top-level setup
# (No specific named objects required for this domain; integers are used for Z_n)

def apply_map(m, x):
    if callable(m):
        return m(x)
    else:
        return m[x]

def get_ring(ring):
    if isinstance(ring, int):
        if ring <= 0:
            raise ValueError("Ring integer must be positive")
        elements = list(range(ring))
        zero = 0
        add = lambda x, y: (x + y) % ring
        mul = lambda x, y: (x * y) % ring
        return elements, zero, add, mul
    else:
        elements, zero, add_dict, mul_dict = ring
        add = lambda x, y: add_dict[(x, y)]
        mul = lambda x, y: mul_dict[(x, y)]
        return elements, zero, add, mul

def is_ring(ring):
    if isinstance(ring, int):
        return ring > 0
    try:
        elements, zero, add_dict, mul_dict = ring
        if zero not in elements: return False
        # check closure
        for x in elements:
            for y in elements:
                if (x, y) not in add_dict or add_dict[(x, y)] not in elements: return False
                if (x, y) not in mul_dict or mul_dict[(x, y)] not in elements: return False
        # check axioms
        for x in elements:
            if add_dict[(x, zero)] != x or add_dict[(zero, x)] != x: return False
            has_inv = False
            for y in elements:
                if add_dict[(x, y)] == zero and add_dict[(y, x)] == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for y in elements:
                if add_dict[(x, y)] != add_dict[(y, x)]: return False
                for z in elements:
                    if add_dict[(add_dict[(x, y)], z)] != add_dict[(x, add_dict[(y, z)])]: return False
                    if mul_dict[(mul_dict[(x, y)], z)] != mul_dict[(x, mul_dict[(y, z)])]: return False
                    if mul_dict[(x, add_dict[(y, z)])] != add_dict[(mul_dict[(x, y)], mul_dict[(x, z)])]: return False
                    if mul_dict[(add_dict[(x, y)], z)] != add_dict[(mul_dict[(x, z)], mul_dict[(y, z)])]: return False
        return True
    except Exception:
        return False

def is_homomorphism(f, R, S):
    try:
        R_elems, R_zero, R_add, R_mul = get_ring(R)
        S_elems, S_zero, S_add, S_mul = get_ring(S)
        
        for x in R_elems:
            fx = apply_map(f, x)
            if fx not in S_elems: return False
            
        for x in R_elems:
            for y in R_elems:
                fx = apply_map(f, x)
                fy = apply_map(f, y)
                fxy_add = apply_map(f, R_add(x, y))
                fxy_mul = apply_map(f, R_mul(x, y))
                if fxy_add != S_add(fx, fy): return False
                if fxy_mul != S_mul(fx, fy): return False
        return True
    except Exception:
        return False

def neg_Q_check(witness):
    R, S, T, f, g = witness
    R_elems, R_zero, R_add, R_mul = get_ring(R)
    S_elems, S_zero, S_add, S_mul = get_ring(S)
    T_elems, T_zero, T_add, T_mul = get_ring(T)
    
    # g must be a valid function from S to T
    for y in S_elems:
        gy = apply_map(g, y)
        if gy not in T_elems:
            return False
            
    ker_f = set()
    for x in R_elems:
        if apply_map(f, x) == S_zero:
            ker_f.add(x)
            
    ker_gf = set()
    for x in R_elems:
        fx = apply_map(f, x)
        gfx = apply_map(g, fx)
        if gfx == T_zero:
            ker_gf.add(x)
            
    return not ker_f.issubset(ker_gf)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 5:
            return [False, False, False]
        R, S, T, f, g = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_ring(R) and is_ring(S) and is_ring(T)
    except Exception:
        h1 = False
        
    try:
        h2 = is_homomorphism(f, R, S)
    except Exception:
        h2 = False
        
    try:
        nq = neg_Q_check(witness)
    except Exception:
        nq = False
        
    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: R, S, and T are rings",
    "H_2: f is a ring homomorphism from R to S",
    "¬Q: The kernel of f is not a subset of the kernel of g \\circ f"
]

N_HYP = 2
NEG_Q_INDEX = 2