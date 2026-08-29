import sympy
from sympy import Rational, Integer
import itertools
import functools
import math

# Top-level setup
Z = sympy.S.Integers
Q = sympy.S.Rationals

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: S' is the image of S under the canonical projection from R to R/I",
    "¬Q: The localized quotient ring (S^{-1}R)/(S^{-1}I) is not isomorphic to (S')^{-1}(R/I)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def check_H1(n, I_list, S, S_prime):
    if not (isinstance(n, int) and n >= 2): return False
    if not isinstance(S, (list, set, tuple)): return False
    if not all(isinstance(s, int) and 0 <= s < n for s in S): return False
    return True

def check_H2(n, I_list, S, S_prime):
    if not isinstance(I_list, (list, set, tuple)): return False
    I_set = set(I_list)
    if len(I_set) == 0: return False
    if not all(isinstance(x, int) and 0 <= x < n for x in I_set): return False
    if 0 not in I_set: return False
    for a in I_set:
        for b in I_set:
            if (a + b) % n not in I_set:
                return False
        for r in range(n):
            if (a * r) % n not in I_set:
                return False
    return True

def construct_R_mod_I(n, I_list):
    I_set = set(I_list)
    def sub(a, b):
        return (a - b) % n
        
    visited = set()
    classes = []
    for e in range(n):
        if e not in visited:
            comp = []
            for x in range(n):
                if sub(e, x) in I_set:
                    comp.append(x)
                    visited.add(x)
            classes.append(comp)
            
    if sum(len(c) for c in classes) != n:
        return None
        
    class_reps = [min(comp) for comp in classes]
    
    class_of = {}
    for i, comp in enumerate(classes):
        rep = class_reps[i]
        for x in comp:
            class_of[x] = rep
            
    add_table = {}
    mul_table = {}
    for i, rep1 in enumerate(class_reps):
        for j, rep2 in enumerate(class_reps):
            s_add = (rep1 + rep2) % n
            if s_add not in class_of: return None
            add_table[(rep1, rep2)] = class_of[s_add]
            
            s_mul = (rep1 * rep2) % n
            if s_mul not in class_of: return None
            mul_table[(rep1, rep2)] = class_of[s_mul]
            
    return class_reps, class_of, add_table, mul_table

def check_H3(n, I_list, S, S_prime):
    if not isinstance(S_prime, (list, set, tuple)): return False
    R_mod_I = construct_R_mod_I(n, I_list)
    if R_mod_I is None: return False
    class_reps, class_of, add_table, mul_table = R_mod_I
    
    true_S_prime = set(class_of[s] for s in S)
    return set(S_prime) == true_S_prime

def construct_localization(n, S):
    if not S:
        return None
    
    RxS = [(r, s) for r in range(n) for s in S]
    
    def sim(a, b):
        r1, s1 = a
        r2, s2 = b
        for t in S:
            if (t * (r1 * s2 - r2 * s1)) % n == 0:
                return True
        return False

    adj = {a: [] for a in RxS}
    for i, a in enumerate(RxS):
        for b in RxS[i:]:
            if sim(a, b):
                adj[a].append(b)
                if a != b:
                    adj[b].append(a)
                    
    classes = []
    visited = set()
    for a in RxS:
        if a not in visited:
            comp = [a]
            visited.add(a)
            q = [a]
            while q:
                curr = q.pop(0)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        comp.append(neighbor)
                        q.append(neighbor)
            classes.append(comp)
            
    for comp in classes:
        for a in comp:
            if len(adj[a]) != len(comp):
                return None
                
    class_of = {}
    for i, comp in enumerate(classes):
        for a in comp:
            class_of[a] = i
            
    for s1 in S:
        for s2 in S:
            if (s1 * s2) % n not in S:
                return None
                
    add_table = {}
    mul_table = {}
    for i, comp1 in enumerate(classes):
        for j, comp2 in enumerate(classes):
            r1, s1 = comp1[0]
            r2, s2 = comp2[0]
            
            r_add = (r1 * s2 + r2 * s1) % n
            s_add = (s1 * s2) % n
            if (r_add, s_add) not in class_of: return None
            add_table[(i, j)] = class_of[(r_add, s_add)]
            
            r_mul = (r1 * r2) % n
            s_mul = (s1 * s2) % n
            if (r_mul, s_mul) not in class_of: return None
            mul_table[(i, j)] = class_of[(r_mul, s_mul)]
            
    return classes, add_table, mul_table

def construct_quotient(elements, add_table, mul_table, ideal_elements):
    zero = None
    for e in elements:
        if all(add_table[(e, x)] == x for x in elements):
            zero = e
            break
    if zero is None: return None
    
    neg = {}
    for e in elements:
        for x in elements:
            if add_table[(e, x)] == zero:
                neg[e] = x
                break
    if len(neg) != len(elements): return None
                
    if zero not in ideal_elements: return None
    for a in ideal_elements:
        for b in ideal_elements:
            if add_table[(a, b)] not in ideal_elements: return None
        for r in elements:
            if mul_table[(a, r)] not in ideal_elements: return None
            if mul_table[(r, a)] not in ideal_elements: return None
            
    def sub(a, b):
        return add_table[(a, neg[b])]
        
    visited = set()
    q_classes = []
    for e in elements:
        if e not in visited:
            comp = []
            for x in elements:
                if sub(e, x) in ideal_elements:
                    comp.append(x)
                    visited.add(x)
            q_classes.append(comp)
            
    if sum(len(c) for c in q_classes) != len(elements):
        return None
            
    q_class_of = {}
    for i, comp in enumerate(q_classes):
        for x in comp:
            q_class_of[x] = i
            
    q_add = {}
    q_mul = {}
    for i, comp1 in enumerate(q_classes):
        for j, comp2 in enumerate(q_classes):
            e1 = comp1[0]
            e2 = comp2[0]
            
            s_add = add_table[(e1, e2)]
            if s_add not in q_class_of: return None
            q_add[(i, j)] = q_class_of[s_add]
            
            s_mul = mul_table[(e1, e2)]
            if s_mul not in q_class_of: return None
            q_mul[(i, j)] = q_class_of[s_mul]
            
    return q_classes, q_add, q_mul

def construct_localization_general(elements, add_table, mul_table, S):
    if not S:
        return None
        
    zero = None
    for e in elements:
        if all(add_table[(e, x)] == x for x in elements):
            zero = e
            break
    if zero is None: return None
            
    neg = {}
    for e in elements:
        for x in elements:
            if add_table[(e, x)] == zero:
                neg[e] = x
                break
    if len(neg) != len(elements): return None
                
    def sub(a, b):
        return add_table[(a, neg[b])]
                
    RxS = [(r, s) for r in elements for s in S]
    
    def sim(a, b):
        r1, s1 = a
        r2, s2 = b
        for t in S:
            term1 = mul_table[(r1, s2)]
            term2 = mul_table[(r2, s1)]
            diff = sub(term1, term2)
            if mul_table[(t, diff)] == zero:
                return True
        return False

    adj = {a: [] for a in RxS}
    for i, a in enumerate(RxS):
        for b in RxS[i:]:
            if sim(a, b):
                adj[a].append(b)
                if a != b:
                    adj[b].append(a)
                    
    classes = []
    visited = set()
    for a in RxS:
        if a not in visited:
            comp = [a]
            visited.add(a)
            q = [a]
            while q:
                curr = q.pop(0)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        comp.append(neighbor)
                        q.append(neighbor)
            classes.append(comp)
            
    for comp in classes:
        for a in comp:
            if len(adj[a]) != len(comp):
                return None
                
    class_of = {}
    for i, comp in enumerate(classes):
        for a in comp:
            class_of[a] = i
            
    for s1 in S:
        for s2 in S:
            if mul_table[(s1, s2)] not in S:
                return None
                
    l_add = {}
    l_mul = {}
    for i, comp1 in enumerate(classes):
        for j, comp2 in enumerate(classes):
            r1, s1 = comp1[0]
            r2, s2 = comp2[0]
            
            term1 = mul_table[(r1, s2)]
            term2 = mul_table[(r2, s1)]
            r_add = add_table[(term1, term2)]
            s_add = mul_table[(s1, s2)]
            if (r_add, s_add) not in class_of: return None
            l_add[(i, j)] = class_of[(r_add, s_add)]
            
            r_mul = mul_table[(r1, r2)]
            s_mul = mul_table[(s1, s2)]
            if (r_mul, s_mul) not in class_of: return None
            l_mul[(i, j)] = class_of[(r_mul, s_mul)]
            
    return classes, l_add, l_mul

def are_isomorphic(elems1, add1, mul1, elems2, add2, mul2):
    if len(elems1) != len(elems2):
        return False
    if len(elems1) == 0:
        return True
        
    def find_zero(elems, add):
        for e in elems:
            if all(add[(e, x)] == x for x in elems):
                return e
        return None
        
    def find_one(elems, mul):
        for e in elems:
            if all(mul[(e, x)] == x and mul[(x, e)] == x for x in elems):
                return e
        return None
        
    z1 = find_zero(elems1, add1)
    z2 = find_zero(elems2, add2)
    o1 = find_one(elems1, mul1)
    o2 = find_one(elems2, mul2)
    
    if z1 is None or z2 is None:
        return False
        
    if (o1 is None) != (o2 is None):
        return False
        
    n_elems = len(elems1)
    mapping = {}
    used = set()
    
    ordered_elems = []
    if z1 is not None: ordered_elems.append(z1)
    if o1 is not None and o1 != z1: ordered_elems.append(o1)
    for e in elems1:
        if e not in (z1, o1):
            ordered_elems.append(e)
            
    def solve(idx):
        if idx == n_elems:
            return True
            
        u = ordered_elems[idx]
        
        if u == z1:
            candidates = [z2]
        elif u == o1:
            candidates = [o2]
        else:
            candidates = elems2
            
        for v in candidates:
            if v in used:
                continue
                
            ok = True
            for mapped_u, mapped_v in mapping.items():
                s_add1 = add1[(u, mapped_u)]
                if s_add1 in mapping and mapping[s_add1] != add2[(v, mapped_v)]:
                    ok = False; break
                s_add2 = add1[(mapped_u, u)]
                if s_add2 in mapping and mapping[s_add2] != add2[(mapped_v, v)]:
                    ok = False; break
                    
                s_mul1 = mul1[(u, mapped_u)]
                if s_mul1 in mapping and mapping[s_mul1] != mul2[(v, mapped_v)]:
                    ok = False; break
                s_mul2 = mul1[(mapped_u, u)]
                if s_mul2 in mapping and mapping[s_mul2] != mul2[(mapped_v, v)]:
                    ok = False; break
            if not ok:
                continue
                
            s_add_self = add1[(u, u)]
            if s_add_self in mapping and mapping[s_add_self] != add2[(v, v)]:
                continue
            s_mul_self = mul1[(u, u)]
            if s_mul_self in mapping and mapping[s_mul_self] != mul2[(v, v)]:
                continue
                
            mapping[u] = v
            used.add(v)
            if solve(idx + 1):
                return True
            del mapping[u]
            used.remove(v)
            
    return solve(0)

def check_neg_Q(n, I_list, S, S_prime):
    loc_R = construct_localization(n, S)
    if loc_R is None:
        return True
        
    classes_R, add_R, mul_R = loc_R
    class_of_R = {}
    for i, comp in enumerate(classes_R):
        for a in comp:
            class_of_R[a] = i
            
    ideal_classes = set()
    for i in I_list:
        for s in S:
            if (i, s) in class_of_R:
                ideal_classes.add(class_of_R[(i, s)])
            
    elements_R = list(range(len(classes_R)))
    quotient = construct_quotient(elements_R, add_R, mul_R, ideal_classes)
    if quotient is None:
        return True
        
    q_classes, q_add, q_mul = quotient
    elems1 = list(range(len(q_classes)))
    
    R_mod_I = construct_R_mod_I(n, I_list)
    if R_mod_I is None:
        return True
    class_reps, class_of, mod_add, mod_mul = R_mod_I
    
    true_S_prime = list(set(class_of[s] for s in S))
    
    loc_mod = construct_localization_general(class_reps, mod_add, mod_mul, true_S_prime)
    if loc_mod is None:
        return True
        
    l_classes, l_add, l_mul = loc_mod
    elems2 = list(range(len(l_classes)))
    
    is_iso = are_isomorphic(elems1, q_add, q_mul, elems2, l_add, l_mul)
    
    return not is_iso

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        n, I_list, S, S_prime = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = check_H1(n, I_list, S, S_prime)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(n, I_list, S, S_prime)
    except Exception:
        h2 = False
        
    try:
        h3 = check_H3(n, I_list, S, S_prime)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(n, I_list, S, S_prime)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]