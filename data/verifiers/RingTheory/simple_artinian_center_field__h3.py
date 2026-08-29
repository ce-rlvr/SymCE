import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: Standard finite rings provided as (n, add_table, mul_table)
# These can be used directly as witnesses.
ZeroRing = (1, [[0]], [[0]])

Z2_add = [[0, 1], [1, 0]]
Z2_mul = [[0, 0], [0, 1]]
Z2 = (2, Z2_add, Z2_mul)

Z2_zero_mul = (2, Z2_add, [[0, 0], [0, 0]])

Z3_add = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
Z3_mul = [[0, 0, 0], [0, 1, 2], [0, 2, 1]]
Z3 = (3, Z3_add, Z3_mul)

Z3_zero_mul = (3, Z3_add, [[0, 0, 0], [0, 0, 0], [0, 0, 0]])

def get_ring(witness):
    class FastRing:
        pass
    R = FastRing()
    
    def safe_eq(x, y):
        try:
            res = (x == y)
            if isinstance(res, bool): return res
            if hasattr(res, 'all'): return bool(res.all())
            return bool(res)
        except Exception:
            return False

    if isinstance(witness, tuple) and len(witness) == 3 and isinstance(witness[0], int):
        n, add_t, mul_t = witness
        if n > 1000: raise ValueError("Ring too large")
        R.elements = list(range(n))
        R.add = lambda x, y: add_t[x][y]
        R.mul = lambda x, y: mul_t[x][y]
        R.zero = 0
        R.eq = lambda x, y: x == y
        return R

    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        elems = list(witness.elements)
        if len(elems) > 1000: raise ValueError("Ring too large")
        n = len(elems)
        
        eq_func = witness.eq if hasattr(witness, 'eq') else safe_eq
        
        add_t = [[0]*n for _ in range(n)]
        mul_t = [[0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                s = witness.add(elems[i], elems[j])
                p = witness.mul(elems[i], elems[j])
                
                s_idx = -1
                for k in range(n):
                    if eq_func(s, elems[k]):
                        s_idx = k
                        break
                if s_idx == -1: raise ValueError("Not closed under addition")
                add_t[i][j] = s_idx
                
                p_idx = -1
                for k in range(n):
                    if eq_func(p, elems[k]):
                        p_idx = k
                        break
                if p_idx == -1: raise ValueError("Not closed under multiplication")
                mul_t[i][j] = p_idx
                
        R.elements = list(range(n))
        R.add = lambda x, y: add_t[x][y]
        R.mul = lambda x, y: mul_t[x][y]
        R.eq = lambda x, y: x == y
        
        if hasattr(witness, 'zero'):
            z_idx = -1
            for k in range(n):
                if eq_func(witness.zero, elems[k]):
                    z_idx = k
                    break
            R.zero = z_idx if z_idx != -1 else 0
        else:
            R.zero = 0
            
        return R

    if isinstance(witness, (list, set, tuple)) and len(witness) > 0:
        elems = list(witness)
        if len(elems) > 1000: raise ValueError("Ring too large")
        n = len(elems)
        
        add_t = [[0]*n for _ in range(n)]
        mul_t = [[0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                try:
                    s = elems[i] + elems[j]
                except Exception:
                    raise ValueError("Addition failed")
                try:
                    p = elems[i] * elems[j]
                except Exception:
                    raise ValueError("Multiplication failed")
                    
                s_idx = -1
                for k in range(n):
                    if safe_eq(s, elems[k]):
                        s_idx = k
                        break
                if s_idx == -1: raise ValueError("Not closed under addition")
                add_t[i][j] = s_idx
                
                p_idx = -1
                for k in range(n):
                    if safe_eq(p, elems[k]):
                        p_idx = k
                        break
                if p_idx == -1: raise ValueError("Not closed under multiplication")
                mul_t[i][j] = p_idx
                
        R.elements = list(range(n))
        R.add = lambda x, y: add_t[x][y]
        R.mul = lambda x, y: mul_t[x][y]
        R.eq = lambda x, y: x == y
        
        for i in range(n):
            is_z = True
            for j in range(n):
                if R.add(i, j) != j:
                    is_z = False
                    break
            if is_z:
                R.zero = i
                break
        if not hasattr(R, 'zero'):
            R.zero = 0
            
        return R

    raise ValueError("Cannot parse witness as a finite ring")

def is_ring(R):
    elems = R.elements
    chk_elems = elems[:30] if len(elems) > 30 else elems
        
    for a in chk_elems:
        if R.add(a, R.zero) != a: return False
        if R.add(R.zero, a) != a: return False
        
    for a in chk_elems:
        has_inv = False
        for b in elems:
            if R.add(a, b) == R.zero and R.add(b, a) == R.zero:
                has_inv = True
                break
        if not has_inv: return False
        
    for a in chk_elems:
        for b in chk_elems:
            if R.add(a, b) != R.add(b, a): return False
            
    for a in chk_elems:
        for b in chk_elems:
            for c in chk_elems:
                if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)): return False
                
    for a in chk_elems:
        for b in chk_elems:
            for c in chk_elems:
                if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)): return False
                if R.mul(R.add(a, b), c) != R.add(R.mul(a, c), R.mul(b, c)): return False
                
    for a in chk_elems:
        for b in chk_elems:
            for c in chk_elems:
                if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)): return False
                
    return True

def is_simple(R):
    if not is_ring(R):
        return False
        
    n_elems = len(R.elements)
    for x in R.elements:
        if x == R.zero: continue
        
        ideal_list = [x]
        ideal_set = {x}
        processed = 0
        
        while processed < len(ideal_list):
            current = ideal_list[processed]
            processed += 1
            
            for e in ideal_list:
                s1 = R.add(current, e)
                if s1 not in ideal_set:
                    ideal_set.add(s1)
                    ideal_list.append(s1)
                    
                s2 = R.add(e, current)
                if s2 not in ideal_set:
                    ideal_set.add(s2)
                    ideal_list.append(s2)
                    
            for r in R.elements:
                p1 = R.mul(r, current)
                if p1 not in ideal_set:
                    ideal_set.add(p1)
                    ideal_list.append(p1)
                    
                p2 = R.mul(current, r)
                if p2 not in ideal_set:
                    ideal_set.add(p2)
                    ideal_list.append(p2)
                    
        if len(ideal_set) < n_elems:
            return False
            
    return True

def is_right_artinian(R):
    return len(R.elements) > 0

def get_center(R):
    center = []
    for x in R.elements:
        is_central = True
        for y in R.elements:
            if R.mul(x, y) != R.mul(y, x):
                is_central = False
                break
        if is_central:
            center.append(x)
    return center

def is_field(R, subset):
    if len(subset) < 2:
        return False
    
    for x in subset:
        for y in subset:
            if R.mul(x, y) != R.mul(y, x):
                return False
                
    identity = None
    for e in subset:
        is_id = True
        for x in subset:
            if R.mul(e, x) != x:
                is_id = False
                break
        if is_id:
            identity = e
            break
            
    if identity is None or identity == R.zero:
        return False
        
    for x in subset:
        if x == R.zero: continue
        has_inv = False
        for y in subset:
            if R.mul(x, y) == identity:
                has_inv = True
                break
        if not has_inv:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        R = get_ring(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_simple(R)
    except Exception:
        h1 = False
        
    try:
        h2 = is_right_artinian(R)
    except Exception:
        h2 = False
        
    try:
        center = get_center(R)
        neg_q = not is_field(R, center)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a simple ring",
    "H_2: R is a right Artinian ring",
    "¬Q: Z(R) is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2