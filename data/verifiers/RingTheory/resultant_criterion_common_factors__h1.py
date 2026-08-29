import sympy
from sympy import Matrix
import itertools

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
            
        f_coeffs, g_coeffs, m = witness
        
        if not isinstance(m, int) or m < 2:
            return [False, False]
            
        if not isinstance(f_coeffs, (list, tuple)) or not isinstance(g_coeffs, (list, tuple)):
            return [False, False]
            
        f_coeffs = [int(c) % m for c in f_coeffs]
        g_coeffs = [int(c) % m for c in g_coeffs]
        
        while f_coeffs and f_coeffs[0] == 0:
            f_coeffs.pop(0)
        while g_coeffs and g_coeffs[0] == 0:
            g_coeffs.pop(0)
            
        if len(f_coeffs) < 2 or len(g_coeffs) < 2:
            return [False, False]
            
        h1 = True
        
        deg_f = len(f_coeffs) - 1
        deg_g = len(g_coeffs) - 1
        
        sylvester = []
        for i in range(deg_g):
            row = [0] * i + f_coeffs + [0] * (deg_g - 1 - i)
            sylvester.append(row)
        for i in range(deg_f):
            row = [0] * i + g_coeffs + [0] * (deg_f - 1 - i)
            sylvester.append(row)
            
        M = Matrix(sylvester)
        res = int(M.det()) % m
        res_is_zero = (res == 0)
        
        f_asc = f_coeffs[::-1]
        g_asc = g_coeffs[::-1]
        
        max_deg = max(deg_f, deg_g)
        
        def divides(h_asc, target_asc):
            deg_q_max = len(target_asc) - 1
            for q_asc in itertools.product(range(m), repeat=deg_q_max + 1):
                prod = [0] * (len(h_asc) + len(q_asc) - 1)
                for i, hc in enumerate(h_asc):
                    if hc == 0: continue
                    for j, qc in enumerate(q_asc):
                        prod[i+j] = (prod[i+j] + hc * qc) % m
                
                while len(prod) > 1 and prod[-1] == 0:
                    prod.pop()
                    
                if prod == target_asc:
                    return True
            return False

        has_common_factor = False
        
        num_q = m ** (max_deg + 1)
        num_h = sum(m ** (d + 1) for d in range(1, max_deg + 1))
        if num_h * num_q > 5 * 10**6:
            return [h1, False]
            
        for d in range(1, max_deg + 1):
            if has_common_factor:
                break
            for h_coeffs in itertools.product(range(m), repeat=d + 1):
                h_asc = list(h_coeffs)
                while len(h_asc) > 1 and h_asc[-1] == 0:
                    h_asc.pop()
                if len(h_asc) - 1 != d:
                    continue
                
                if divides(h_asc, f_asc) and divides(h_asc, g_asc):
                    has_common_factor = True
                    break
                    
        iff_holds = (has_common_factor == res_is_zero)
        neg_q = not iff_holds
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: f and g are non-constant polynomials", "¬Q: common factor iff resultant is zero FAILS"]
N_HYP = 1
NEG_Q_INDEX = 1