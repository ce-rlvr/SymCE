import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

# Top-level setup
# No specific named groups or matrices are needed for this ring theory theorem.
# We provide ZZ, QQ, and symbols x, y, z for convenience.

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            # Case 1: SymPy objects
            if hasattr(R, 'is_commutative') or R in [sympy.ZZ, sympy.QQ]:
                if R in [sympy.ZZ, sympy.QQ]:
                    h1 = True
                else:
                    h1 = bool(R.is_commutative)
                    
                is_proper = True
                if I == R or I == 1:
                    is_proper = False
                elif hasattr(I, 'is_whole_ring') and I.is_whole_ring():
                    is_proper = False
                elif isinstance(I, list) and 1 in I:
                    is_proper = False
                    
                if not is_proper:
                    is_primary = False
                    all_nilpotent = True
                    neg_q = (is_primary != all_nilpotent)
                    return [h1, neg_q]
                else:
                    return [h1, False]
                    
            # Case 2: (n, k) representing Z_n and ideal <k>
            if isinstance(R, int) and isinstance(I, int):
                n = R
                k = I
                if n > 0:
                    h1 = True
                    
                    ideal_elements = set()
                    curr = 0
                    for _ in range(n + 1):
                        ideal_elements.add(curr)
                        curr = (curr + k) % n
                        
                    is_primary = True
                    if len(ideal_elements) == n:
                        is_primary = False
                    else:
                        for a in range(n):
                            for b in range(n):
                                if (a * b) % n in ideal_elements:
                                    if a not in ideal_elements:
                                        b_m = b
                                        found = False
                                        for m in range(1, n+1):
                                            if b_m in ideal_elements:
                                                found = True
                                                break
                                            b_m = (b_m * b) % n
                                        if not found:
                                            is_primary = False
                                            break
                            if not is_primary:
                                break
                                
                    def get_coset(x):
                        return min((x + i) % n for i in ideal_elements)
                        
                    cosets = list(set(get_coset(x) for x in range(n)))
                    zero_coset = get_coset(0)
                    
                    zero_divisors = []
                    for c in cosets:
                        is_zd = False
                        for d in cosets:
                            if d != zero_coset:
                                if get_coset(c * d) == zero_coset:
                                    is_zd = True
                                    break
                        if is_zd:
                            zero_divisors.append(c)
                            
                    all_nilpotent = True
                    for c in zero_divisors:
                        c_m = c
                        found = False
                        for m in range(1, len(cosets) + 1):
                            if c_m == zero_coset:
                                found = True
                                break
                            c_m = get_coset(c_m * c)
                        if not found:
                            all_nilpotent = False
                            break
                            
                    neg_q = (is_primary != all_nilpotent)
                    return [h1, neg_q]
                    
        # Case 3: dict with explicit tables
        if isinstance(witness, dict):
            n = witness.get('n', 0)
            add = witness.get('add', [])
            mul = witness.get('mul', [])
            I_list = witness.get('I', [])
            
            if n > 0 and len(add) == n and len(mul) == n:
                h1 = True
                for i in range(n):
                    for j in range(n):
                        if add[i][j] != add[j][i]: h1 = False
                        if mul[i][j] != mul[j][i]: h1 = False
                        for k in range(n):
                            if add[i][add[j][k]] != add[add[i][j]][k]: h1 = False
                            if mul[i][mul[j][k]] != mul[mul[i][j]][k]: h1 = False
                            if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: h1 = False
                
                zero = None
                for i in range(n):
                    if all(add[i][j] == j for j in range(n)):
                        zero = i
                        break
                if zero is None: h1 = False
                
                if zero not in I_list: h1 = False
                for i in I_list:
                    for j in I_list:
                        if add[i][j] not in I_list: h1 = False
                    for r in range(n):
                        if mul[r][i] not in I_list: h1 = False
                        
                if not h1:
                    return [False, False]
                    
                is_primary = True
                if len(I_list) == n:
                    is_primary = False
                else:
                    for a in range(n):
                        for b in range(n):
                            if mul[a][b] in I_list:
                                if a not in I_list:
                                    b_m = b
                                    found = False
                                    for m in range(1, n+1):
                                        if b_m in I_list:
                                            found = True
                                            break
                                        b_m = mul[b_m][b]
                                    if not found:
                                        is_primary = False
                                        break
                        if not is_primary:
                            break
                            
                inv = [0]*n
                for i in range(n):
                    for j in range(n):
                        if add[i][j] == zero:
                            inv[i] = j
                            break
                            
                def get_coset_dict(x):
                    return min(y for y in range(n) if add[x][inv[y]] in I_list)
                    
                cosets = list(set(get_coset_dict(x) for x in range(n)))
                zero_coset = get_coset_dict(zero)
                
                zero_divisors = []
                for c in cosets:
                    is_zd = False
                    for d in cosets:
                        if d != zero_coset:
                            if get_coset_dict(mul[c][d]) == zero_coset:
                                is_zd = True
                                break
                    if is_zd:
                        zero_divisors.append(c)
                        
                all_nilpotent = True
                for c in zero_divisors:
                    c_m = c
                    found = False
                    for m in range(1, len(cosets) + 1):
                        if c_m == zero_coset:
                            found = True
                            break
                        c_m = get_coset_dict(mul[c_m][c])
                    if not found:
                        all_nilpotent = False
                        break
                        
                neg_q = (is_primary != all_nilpotent)
                return [h1, neg_q]
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: I is a primary ideal if and only if every zero divisor in the quotient ring R/I is nilpotent (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1