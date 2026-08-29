import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def is_commutative_ring(add_table, mult_table):
    n = len(add_table)
    if n == 0: return False
    if len(mult_table) != n: return False
    for i in range(n):
        if len(add_table[i]) != n or len(mult_table[i]) != n: return False
        
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False
            if mult_table[i][j] != mult_table[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                if mult_table[mult_table[i][j]][k] != mult_table[i][mult_table[j][k]]: return False
                if mult_table[i][add_table[j][k]] != add_table[mult_table[i][j]][mult_table[i][k]]: return False
                
    has_zero = False
    for z_elem in range(n):
        if all(add_table[i][z_elem] == i for i in range(n)):
            has_zero = True
            has_inv = True
            for i in range(n):
                if not any(add_table[i][j] == z_elem for j in range(n)):
                    has_inv = False
                    break
            if has_inv:
                break
    if not has_zero: return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)):
            return [False, False, False]
            
        if len(witness) == 2:
            I_list, x_elem = witness
            if not isinstance(I_list, (list, tuple)) or not I_list:
                return [False, False, False]
            
            h1 = True
            h2 = all(isinstance(i, int) for i in I_list)
            if not h2:
                return [False, False, False]
                
            if isinstance(x_elem, int):
                x_val = x_elem
            elif isinstance(x_elem, (list, tuple, set)) and all(isinstance(j, int) for j in x_elem):
                x_val = 0
                for j in x_elem:
                    x_val = math.gcd(x_val, j)
            else:
                return [False, False, False]
                
            def z_ideal_quotient(a, x_v):
                a = abs(a)
                x_v = abs(x_v)
                if x_v == 0:
                    return 1 if a == 0 else 0
                if a == 0:
                    return 0
                return a // math.gcd(a, x_v)

            def z_ideal_intersect(a, b):
                return math.lcm(abs(a), abs(b))
                
            L = abs(I_list[0])
            for i in I_list[1:]:
                L = z_ideal_intersect(L, i)
            q1 = z_ideal_quotient(L, x_val)
            
            L2 = z_ideal_quotient(I_list[0], x_val)
            for i in I_list[1:]:
                qi = z_ideal_quotient(i, x_val)
                L2 = z_ideal_intersect(L2, qi)
                
            neg_q = (q1 != L2)
            return [h1, h2, neg_q]
            
        elif len(witness) == 3:
            n, I_list, x_elem = witness
            if not isinstance(n, int) or n < 2:
                return [False, False, False]
            if not isinstance(I_list, (list, tuple)) or not I_list:
                return [False, False, False]
            
            h1 = True
            h2 = True
            for I in I_list:
                if not isinstance(I, (list, tuple, set)):
                    h2 = False
                    break
                I_set = set(I)
                if not I_set:
                    h2 = False
                    break
                for a in I_set:
                    for b in I_set:
                        if (a + b) % n not in I_set:
                            h2 = False
                    for r in range(n):
                        if (a * r) % n not in I_set:
                            h2 = False
            if not h2:
                return [h1, h2, False]
                
            inter = set(I_list[0])
            for I in I_list[1:]:
                inter = inter.intersection(set(I))
                
            if isinstance(x_elem, int):
                x_list = [x_elem]
            elif isinstance(x_elem, (list, tuple, set)):
                x_list = list(x_elem)
            else:
                return [h1, h2, False]
                
            if any(not isinstance(j, int) or j < 0 or j >= n for j in x_list):
                return [h1, h2, False]
                
            def quotient(I_set, X_list):
                res = set()
                for r in range(n):
                    if all((r * j) % n in I_set for j in X_list):
                        res.add(r)
                return res
                
            q1 = quotient(inter, x_list)
            q2 = quotient(set(I_list[0]), x_list)
            for I in I_list[1:]:
                q2 = q2.intersection(quotient(set(I), x_list))
                
            neg_q = (q1 != q2)
            return [h1, h2, neg_q]
            
        elif len(witness) == 4:
            add_table, mult_table, I_list, x_elem = witness
            if not isinstance(add_table, (list, tuple)) or not isinstance(mult_table, (list, tuple)):
                return [False, False, False]
            
            h1 = is_commutative_ring(add_table, mult_table)
            if not h1:
                return [h1, False, False]
                
            n = len(add_table)
            h2 = True
            if not isinstance(I_list, (list, tuple)) or not I_list:
                h2 = False
            else:
                for I in I_list:
                    if not isinstance(I, (list, tuple, set)):
                        h2 = False
                        break
                    I_set = set(I)
                    if not I_set:
                        h2 = False
                        break
                    for a in I_set:
                        for b in I_set:
                            if add_table[a][b] not in I_set:
                                h2 = False
                        for r in range(n):
                            if mult_table[a][r] not in I_set:
                                h2 = False
            if not h2:
                return [h1, h2, False]
                
            inter = set(I_list[0])
            for I in I_list[1:]:
                inter = inter.intersection(set(I))
                
            if isinstance(x_elem, int):
                x_list = [x_elem]
            elif isinstance(x_elem, (list, tuple, set)):
                x_list = list(x_elem)
            else:
                return [h1, h2, False]
                
            if any(not isinstance(j, int) or j < 0 or j >= n for j in x_list):
                return [h1, h2, False]
                
            def quotient2(I_set, X_list):
                res = set()
                for r in range(n):
                    if all(mult_table[r][j] in I_set for j in X_list):
                        res.add(r)
                return res
                
            q1 = quotient2(inter, x_list)
            q2 = quotient2(set(I_list[0]), x_list)
            for I in I_list[1:]:
                q2 = q2.intersection(quotient2(set(I), x_list))
                
            neg_q = (q1 != q2)
            return [h1, h2, neg_q]
            
        else:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I_1, I_2, \\dots, I_n are ideals of R",
    "¬Q: The ideal quotient (\\bigcap_{i=1}^n I_i : x) is NOT equal to the intersection of the ideal quotients \\bigcap_{i=1}^n (I_i : x)"
]

N_HYP = 2
NEG_Q_INDEX = 2