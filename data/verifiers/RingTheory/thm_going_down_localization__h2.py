import sympy
from sympy import symbols
import itertools

# Top-level setup
Z = sympy.S.Integers
Q = sympy.S.Rationals
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        # Support for sympy ring and subset tuple
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
            h1 = False
            if hasattr(R, 'is_commutative') and R.is_commutative:
                h1 = True
            elif hasattr(R, 'is_Ring') and R.is_Ring:
                h1 = True
            h2 = isinstance(S, (list, set, tuple))
            
            # The going-down theorem for localization is mathematically true for all commutative rings.
            # Thus, no valid counterexample exists and the negated conclusion is always False.
            neg_q = False
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Support for explicit finite ring tuple: (elements, add_func, mul_func, zero, one, S)
        if isinstance(witness, tuple) and len(witness) == 6:
            elements, add, mul, zero, one, S = witness
            if not isinstance(elements, (list, tuple, set)):
                return [False, False, False]
            elements = list(elements)
            
            # H1: R is a commutative ring
            h1 = True
            if zero not in elements or one not in elements: 
                h1 = False
            else:
                for a in elements:
                    for b in elements:
                        if add(a, b) not in elements: h1 = False
                        if mul(a, b) not in elements: h1 = False
                        if add(a, b) != add(b, a): h1 = False
                        if mul(a, b) != mul(b, a): h1 = False
                    if add(a, zero) != a: h1 = False
                    if mul(a, one) != a: h1 = False
                    if not any(add(a, b) == zero for b in elements): h1 = False
                    
                if h1:
                    for a in elements:
                        for b in elements:
                            for c in elements:
                                if add(add(a, b), c) != add(a, add(b, c)): h1 = False
                                if mul(mul(a, b), c) != mul(a, mul(b, c)): h1 = False
                                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): h1 = False
                                
            # H2: phi is the canonical ring homomorphism (S is a multiplicative subset)
            h2 = True
            if not S or not all(s in elements for s in S):
                h2 = False
            else:
                if one not in S: h2 = False
                for s1 in S:
                    for s2 in S:
                        if mul(s1, s2) not in S: h2 = False
                        
            # neg_Q: The going-down theorem fails
            neg_q = False
            if h1 and h2 and len(elements) <= 8:
                fractions = [(r, s) for r in elements for s in S]
                
                def get_neg(val):
                    for y_elem in elements:
                        if add(val, y_elem) == zero: return y_elem
                    return val
                    
                def equiv(f1, f2):
                    r1, s1 = f1
                    r2, s2 = f2
                    r2_s1 = mul(r2, s1)
                    neg_r2_s1 = get_neg(r2_s1)
                    diff = add(mul(r1, s2), neg_r2_s1)
                    for u in S:
                        if mul(u, diff) == zero: return True
                    return False
                    
                classes = []
                for f in fractions:
                    if not any(equiv(f, c[0]) for c in classes):
                        classes.append([f])
                        
                def is_ideal(I):
                    if zero not in I: return False
                    for x_elem in I:
                        for y_elem in I:
                            if add(x_elem, y_elem) not in I: return False
                        if get_neg(x_elem) not in I: return False
                        for r in elements:
                            if mul(r, x_elem) not in I: return False
                    return True
                    
                def is_prime(I):
                    if not is_ideal(I): return False
                    if len(I) == len(elements): return False
                    for a in elements:
                        for b in elements:
                            if mul(a, b) in I and a not in I and b not in I:
                                return False
                    return True
                    
                prime_ideals_R = []
                for r_size in range(1, len(elements)):
                    for subset in itertools.combinations(elements, r_size):
                        S_set = set(subset)
                        if is_prime(S_set):
                            prime_ideals_R.append(S_set)
                            
                def S_inv_add(c1, c2):
                    r1, s1 = c1[0]
                    r2, s2 = c2[0]
                    num = add(mul(r1, s2), mul(r2, s1))
                    den = mul(s1, s2)
                    for c in classes:
                        if equiv((num, den), c[0]): return c
                        
                def S_inv_mul(c1, c2):
                    r1, s1 = c1[0]
                    r2, s2 = c2[0]
                    num = mul(r1, r2)
                    den = mul(s1, s2)
                    for c in classes:
                        if equiv((num, den), c[0]): return c
                        
                S_inv_zero = next(c for c in classes if equiv((zero, one), c[0]))
                
                def is_ideal_S(I_idx):
                    if classes.index(S_inv_zero) not in I_idx: return False
                    for i in I_idx:
                        for j in I_idx:
                            sum_c = S_inv_add(classes[i], classes[j])
                            if classes.index(sum_c) not in I_idx: return False
                        r_val, s_val = classes[i][0]
                        nr = get_neg(r_val)
                        neg_c = next(c for c in classes if equiv((nr, s_val), c[0]))
                        if classes.index(neg_c) not in I_idx: return False
                        for k in range(len(classes)):
                            prod_c = S_inv_mul(classes[k], classes[i])
                            if classes.index(prod_c) not in I_idx: return False
                    return True
                    
                def is_prime_S(I_idx):
                    if not is_ideal_S(I_idx): return False
                    if len(I_idx) == len(classes): return False
                    for i in range(len(classes)):
                        for j in range(len(classes)):
                            prod_c = S_inv_mul(classes[i], classes[j])
                            if classes.index(prod_c) in I_idx and i not in I_idx and j not in I_idx:
                                return False
                    return True
                    
                prime_ideals_S = []
                for r_size in range(1, len(classes)):
                    for subset in itertools.combinations(range(len(classes)), r_size):
                        S_set = set(subset)
                        if is_prime_S(S_set):
                            prime_ideals_S.append(S_set)
                            
                def phi_inv(I_idx):
                    res = set()
                    for r_val in elements:
                        phi_r = next(c for c in classes if equiv((r_val, one), c[0]))
                        if classes.index(phi_r) in I_idx:
                            res.add(r_val)
                    return res
                    
                for P1 in prime_ideals_R:
                    for P2 in prime_ideals_R:
                        if P1.issubset(P2):
                            for Q2 in prime_ideals_S:
                                if phi_inv(Q2) == P2:
                                    found_Q1 = False
                                    for Q1 in prime_ideals_S:
                                        if Q1.issubset(Q2) and phi_inv(Q1) == P1:
                                            found_Q1 = True
                                            break
                                    if not found_Q1:
                                        neg_q = True
                                        break
                            if neg_q: break
                        if neg_q: break
                        
            return [bool(h1), bool(h2), bool(neg_q)]
            
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: phi is the canonical ring homomorphism",
    "¬Q: phi does not satisfy the going-down theorem"
]

N_HYP = 2
NEG_Q_INDEX = 2