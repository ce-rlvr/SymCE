import sympy
from sympy import symbols
import math

# Top-level setup
x, y, z = symbols('x y z')

def get_comb(n, k):
    if hasattr(math, 'comb'):
        return math.comb(n, k)
    if k < 0 or k > n:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def conditions(witness):
    h1, h2, neg_q = False, False, False
    
    try:
        # Case 1: witness is a tuple of integers (n, d) representing ideal (d) in Z/nZ
        if isinstance(witness, tuple) and len(witness) == 2 and all(isinstance(val, int) for val in witness):
            n, d = witness
            if n > 1:
                h1 = (d % n) != 0
                gcd_val = math.gcd(d, n)
                h2 = gcd_val > 1 and gcd_val < n
                
                from sympy import factorint
                factors = factorint(n)
                is_unique = True
                for p, v_n in factors.items():
                    v_d = 0
                    temp = abs(d)
                    if temp == 0:
                        v_d = v_n
                    else:
                        while temp % p == 0:
                            v_d += 1
                            temp //= p
                    if v_d >= v_n:
                        is_unique = False
                        break
                neg_q = not is_unique
                return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Case 2: witness is a SymPy Ideal
        if hasattr(witness, 'is_zero') and hasattr(witness, 'is_whole_ring') and hasattr(witness, 'gens'):
            h1 = not witness.is_zero
            h2 = not witness.is_whole_ring
            gens = witness.gens
            
            if len(gens) <= 1:
                neg_q = False
            else:
                free_symbols = set()
                for g in gens:
                    if hasattr(g, 'free_symbols'):
                        free_symbols.update(g.free_symbols)
                all_vars = list(free_symbols)
                
                all_monomials = True
                exps_list = []
                for g in gens:
                    if hasattr(g, 'is_number') and g.is_number:
                        exps_list.append(tuple([0]*len(all_vars)))
                    else:
                        if not hasattr(g, 'as_poly'):
                            all_monomials = False
                            break
                        poly = g.as_poly(*all_vars)
                        if poly is None or len(poly.terms()) != 1:
                            all_monomials = False
                            break
                        exps_list.append(poly.terms()[0][0])
                
                if all_monomials:
                    min_exps = list(exps_list[0])
                    for exps in exps_list[1:]:
                        for i in range(len(min_exps)):
                            min_exps[i] = min(min_exps[i], exps[i])
                    
                    degrees = set()
                    vars_used = set()
                    for exps in exps_list:
                        rem_exps = [e - m for e, m in zip(exps, min_exps)]
                        deg = sum(rem_exps)
                        degrees.add(deg)
                        for i, e in enumerate(rem_exps):
                            if e > 0:
                                vars_used.add(i)
                    
                    if len(degrees) > 1:
                        neg_q = True
                    else:
                        deg = list(degrees)[0]
                        if deg == 0 or deg == 1:
                            neg_q = False
                        else:
                            expected = get_comb(len(vars_used) + deg - 1, deg)
                            if len(gens) == expected:
                                neg_q = False
                            else:
                                neg_q = True
                else:
                    neg_q = False
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Case 3: witness is a tuple of SymPy expressions representing generators of an ideal
        if isinstance(witness, tuple) and all(hasattr(val, 'free_symbols') for val in witness):
            gens = witness
            
            h1 = False
            for g in gens:
                if hasattr(g, 'is_zero') and g.is_zero is not None:
                    if not g.is_zero:
                        h1 = True
                        break
                elif g != 0:
                    h1 = True
                    break
            
            h2 = True
            for g in gens:
                if hasattr(g, 'is_number') and g.is_number:
                    if hasattr(g, 'is_zero') and g.is_zero is not None:
                        if not g.is_zero:
                            h2 = False
                            break
                    elif g != 0:
                        h2 = False
                        break
            
            if len(gens) <= 1:
                neg_q = False
            else:
                free_symbols = set()
                for g in gens:
                    if hasattr(g, 'free_symbols'):
                        free_symbols.update(g.free_symbols)
                all_vars = list(free_symbols)
                
                all_monomials = True
                exps_list = []
                for g in gens:
                    if hasattr(g, 'is_number') and g.is_number:
                        exps_list.append(tuple([0]*len(all_vars)))
                    else:
                        if not hasattr(g, 'as_poly'):
                            all_monomials = False
                            break
                        poly = g.as_poly(*all_vars)
                        if poly is None or len(poly.terms()) != 1:
                            all_monomials = False
                            break
                        exps_list.append(poly.terms()[0][0])
                
                if all_monomials:
                    min_exps = list(exps_list[0])
                    for exps in exps_list[1:]:
                        for i in range(len(min_exps)):
                            min_exps[i] = min(min_exps[i], exps[i])
                    
                    degrees = set()
                    vars_used = set()
                    for exps in exps_list:
                        rem_exps = [e - m for e, m in zip(exps, min_exps)]
                        deg = sum(rem_exps)
                        degrees.add(deg)
                        for i, e in enumerate(rem_exps):
                            if e > 0:
                                vars_used.add(i)
                    
                    if len(degrees) > 1:
                        neg_q = True
                    else:
                        deg = list(degrees)[0]
                        if deg == 0 or deg == 1:
                            neg_q = False
                        else:
                            expected = get_comb(len(vars_used) + deg - 1, deg)
                            if len(gens) == expected:
                                neg_q = False
                            else:
                                neg_q = True
                else:
                    neg_q = False
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a non-zero ideal of R",
    "H_2: I is a proper ideal of R",
    "¬Q: I cannot be uniquely factored into a product of prime ideals"
]
N_HYP = 2
NEG_Q_INDEX = 2