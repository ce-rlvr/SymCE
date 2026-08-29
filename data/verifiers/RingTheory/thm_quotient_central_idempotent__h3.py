import sympy
from sympy import Matrix, eye, zeros
import itertools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def mod_elem(a, n):
    if n == 0:
        return a
    try:
        return a.applyfunc(lambda x: x % n)
    except AttributeError:
        return a % n

def is_zero(a, n):
    a_mod = mod_elem(a, n)
    if hasattr(a_mod, 'is_zero_matrix'):
        return a_mod.is_zero_matrix
    if hasattr(a_mod, 'is_zero'):
        return a_mod.is_zero
    return a_mod == 0 or a_mod == mod_elem(a - a, n)

def eq(a, b, n):
    return is_zero(a - b, n)

def elem_in(a, lst, n):
    return any(eq(a, x, n) for x in lst)

def get_elem_idx(a, lst, n):
    for i, x in enumerate(lst):
        if eq(a, x, n):
            return i
    return -1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, e, I, n = witness
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, e, I = witness
            n = 0
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def check_h1():
        if not R: return False
        for a in R:
            for b in R:
                if not elem_in(a + b, R, n): return False
                if not elem_in(a * b, R, n): return False
        has_zero = False
        for a in R:
            if is_zero(a, n):
                has_zero = True
                break
        if not has_zero: return False
        
        has_id = False
        for a in R:
            is_id = True
            for b in R:
                if not eq(a * b, b, n) or not eq(b * a, b, n):
                    is_id = False
                    break
            if is_id:
                has_id = True
                break
        if not has_id: return False
        return True

    try:
        h1 = check_h1()
    except Exception:
        h1 = False

    def check_h2():
        if not elem_in(e, R, n): return False
        if not eq(e * e, e, n): return False
        for a in R:
            if not eq(e * a, a * e, n): return False
        return True

    try:
        h2 = check_h2()
    except Exception:
        h2 = False

    def check_neg_q():
        if not I: return True
        for x in I:
            if not elem_in(x, R, n): return True
        for x in I:
            for y in I:
                if not elem_in(x + y, I, n): return True
                if not elem_in(-x, I, n): return True
        for x in I:
            for r in R:
                if not elem_in(x * r, I, n): return True
                if not elem_in(r * x, I, n): return True
                
        cosets = []
        for r in R:
            found = False
            for c in cosets:
                if elem_in(r - c[0], I, n):
                    c.append(r)
                    found = True
                    break
            if not found:
                cosets.append([r])
                
        id_R = None
        for a in R:
            is_id = True
            for b in R:
                if not eq(a * b, b, n) or not eq(b * a, b, n):
                    is_id = False
                    break
            if is_id:
                id_R = a
                break
        if id_R is None:
            return True
            
        f = id_R - e
        R_f = []
        for r in R:
            x = r * f
            if not elem_in(x, R_f, n):
                R_f.append(x)
                
        if len(cosets) != len(R_f):
            return True
            
        def get_coset_idx(a):
            for i, c in enumerate(cosets):
                if elem_in(a - c[0], I, n):
                    return i
            return -1
            
        size = len(cosets)
        add_RI = [[0]*size for _ in range(size)]
        mul_RI = [[0]*size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                idx_add = get_coset_idx(cosets[i][0] + cosets[j][0])
                idx_mul = get_coset_idx(cosets[i][0] * cosets[j][0])
                if idx_add == -1 or idx_mul == -1:
                    return True
                add_RI[i][j] = idx_add
                mul_RI[i][j] = idx_mul
                
        add_Rf = [[0]*size for _ in range(size)]
        mul_Rf = [[0]*size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                idx_add = get_elem_idx(R_f[i] + R_f[j], R_f, n)
                idx_mul = get_elem_idx(R_f[i] * R_f[j], R_f, n)
                if idx_add == -1 or idx_mul == -1:
                    return True
                add_Rf[i][j] = idx_add
                mul_Rf[i][j] = idx_mul
                
        zero_RI = -1
        for i, c in enumerate(cosets):
            if elem_in(c[0], I, n):
                zero_RI = i
                break
                
        zero_Rf = -1
        for i, x in enumerate(R_f):
            if is_zero(x, n):
                zero_Rf = i
                break
                
        if zero_RI == -1 or zero_Rf == -1:
            return True
            
        id_RI = -1
        for i in range(size):
            is_id = True
            for j in range(size):
                if mul_RI[i][j] != j or mul_RI[j][i] != j:
                    is_id = False
                    break
            if is_id:
                id_RI = i
                break
                
        id_Rf = -1
        for i in range(size):
            is_id = True
            for j in range(size):
                if mul_Rf[i][j] != j or mul_Rf[j][i] != j:
                    is_id = False
                    break
            if is_id:
                id_Rf = i
                break
                
        if id_RI == -1 or id_Rf == -1:
            return True
            
        rem_RI = [i for i in range(size) if i != zero_RI and i != id_RI]
        rem_Rf = [i for i in range(size) if i != zero_Rf and i != id_Rf]
        
        if len(rem_RI) != len(rem_Rf):
            return True
            
        if zero_RI == id_RI:
            if zero_Rf != id_Rf:
                return True
            for p_rem in itertools.permutations(rem_Rf):
                p = [0] * size
                p[zero_RI] = zero_Rf
                for i, val in zip(rem_RI, p_rem):
                    p[i] = val
                
                is_iso = True
                for i in range(size):
                    for j in range(size):
                        if p[add_RI[i][j]] != add_Rf[p[i]][p[j]]:
                            is_iso = False
                            break
                        if p[mul_RI[i][j]] != mul_Rf[p[i]][p[j]]:
                            is_iso = False
                            break
                    if not is_iso:
                        break
                if is_iso:
                    return False
        else:
            if zero_Rf == id_Rf:
                return True
            for p_rem in itertools.permutations(rem_Rf):
                p = [0] * size
                p[zero_RI] = zero_Rf
                p[id_RI] = id_Rf
                for i, val in zip(rem_RI, p_rem):
                    p[i] = val
                
                is_iso = True
                for i in range(size):
                    for j in range(size):
                        if p[add_RI[i][j]] != add_Rf[p[i]][p[j]]:
                            is_iso = False
                            break
                        if p[mul_RI[i][j]] != mul_Rf[p[i]][p[j]]:
                            is_iso = False
                            break
                    if not is_iso:
                        break
                if is_iso:
                    return False
                    
        return True

    try:
        neg_q = check_neg_q()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: e is a central idempotent element of R",
    "¬Q: The quotient ring R/I is not isomorphic to the ring R(1-e)"
]

N_HYP = 2
NEG_Q_INDEX = 2