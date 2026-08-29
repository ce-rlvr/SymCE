import itertools
import sympy
from sympy import Rational, Integer

def make_callable(f):
    if isinstance(f, dict):
        return lambda x: f.get(x, None)
    return f

def make_op(op):
    if isinstance(op, dict):
        return lambda x, y: op.get((x, y), None)
    return op

def is_comm_ring_with_id(elements, add, mul, zero, one):
    elements = list(elements)
    if zero not in elements or one not in elements: return False
    for a in elements:
        for b in elements:
            if add(a, b) not in elements: return False
            if mul(a, b) not in elements: return False
    for a in elements:
        if add(a, zero) != a or add(zero, a) != a: return False
        for b in elements:
            if add(a, b) != add(b, a): return False
            for c in elements:
                if add(add(a, b), c) != add(a, add(b, c)): return False
    for a in elements:
        has_inv = False
        for b in elements:
            if add(a, b) == zero and add(b, a) == zero:
                has_inv = True
                break
        if not has_inv: return False
    for a in elements:
        if mul(a, one) != a or mul(one, a) != a: return False
        for b in elements:
            if mul(a, b) != mul(b, a): return False
            for c in elements:
                if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
                if mul(add(a, b), c) != add(mul(a, c), mul(b, c)): return False
    return True

def is_ring_hom(R, T, f, add_R, mul_R, one_R, add_T, mul_T, one_T):
    if f(one_R) != one_T: return False
    for a in R:
        if f(a) not in T: return False
        for b in R:
            if f(add_R(a, b)) != add_T(f(a), f(b)): return False
            if f(mul_R(a, b)) != mul_T(f(a), f(b)): return False
    return True

def is_unit(ring, elem, mul_op, one):
    for x in ring:
        if mul_op(elem, x) == one and mul_op(x, elem) == one:
            return True
    return False

def is_localization(R, S, S_inv_R, phi, add_R, mul_R, zero_R, one_R, add_S, mul_S, zero_S, one_S):
    if not is_comm_ring_with_id(S_inv_R, add_S, mul_S, zero_S, one_S): return False
    if not is_ring_hom(R, S_inv_R, phi, add_R, mul_R, one_R, add_S, mul_S, one_S): return False
    
    for s in S:
        if not is_unit(S_inv_R, phi(s), mul_S, one_S): return False
        
    for y in S_inv_R:
        found = False
        for a in R:
            for s in S:
                inv_phi_s = None
                for x in S_inv_R:
                    if mul_S(phi(s), x) == one_S and mul_S(x, phi(s)) == one_S:
                        inv_phi_s = x
                        break
                if inv_phi_s is not None and y == mul_S(phi(a), inv_phi_s):
                    found = True
                    break
            if found: break
        if not found: return False
        
    for a in R:
        in_ker = (phi(a) == zero_S)
        annihilated = any(mul_R(a, s) == zero_R for s in S)
        if in_ker != annihilated: return False
        
    return True

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False, False, False]
            
        w = witness
        R = list(w['R'])
        T = list(w['T'])
        S = list(w['S'])
        S_inv_R = list(w['S_inv_R'])
        
        add_R = make_op(w['add_R'])
        mul_R = make_op(w['mul_R'])
        add_T = make_op(w['add_T'])
        mul_T = make_op(w['mul_T'])
        add_S = make_op(w['add_S_inv_R'])
        mul_S = make_op(w['mul_S_inv_R'])
        
        zero_R = w['zero_R']
        one_R = w['one_R']
        zero_T = w['zero_T']
        one_T = w['one_T']
        zero_S = w['zero_S_inv_R']
        one_S = w['one_S_inv_R']
        
        f = make_callable(w['f'])
        phi = make_callable(w['phi'])
        
        # H1: R and T are commutative rings with identity
        try:
            h1 = is_comm_ring_with_id(R, add_R, mul_R, zero_R, one_R) and \
                 is_comm_ring_with_id(T, add_T, mul_T, zero_T, one_T)
        except Exception:
            h1 = False
            
        # H2: S is a multiplicatively closed subset of R
        try:
            h2 = True
            if not all(s in R for s in S): h2 = False
            if one_R not in S: h2 = False
            for s1 in S:
                for s2 in S:
                    if mul_R(s1, s2) not in S: h2 = False
        except Exception:
            h2 = False
            
        # H3: f(s) is a unit in T for all s \in S
        try:
            h3 = True
            for a in R:
                if f(a) not in T: h3 = False
            for s in S:
                if not is_unit(T, f(s), mul_T, one_T): h3 = False
        except Exception:
            h3 = False
            
        # H4: \phi: R \to S^{-1}R is the canonical localization map
        try:
            h4 = is_localization(R, S, S_inv_R, phi, add_R, mul_R, zero_R, one_R, add_S, mul_S, zero_S, one_S)
        except Exception:
            h4 = False
            
        # neg_Q: There does NOT exist a unique ring homomorphism g: S^{-1}R \to T such that f = g \circ \phi
        try:
            if len(S_inv_R) > 6 or len(T) > 6:
                neg_q = False
            else:
                valid_g_count = 0
                for g_values in itertools.product(T, repeat=len(S_inv_R)):
                    g_dict = dict(zip(S_inv_R, g_values))
                    g = lambda x: g_dict.get(x, None)
                    
                    if not is_ring_hom(S_inv_R, T, g, add_S, mul_S, one_S, add_T, mul_T, one_T):
                        continue
                        
                    satisfies_comp = True
                    for a in R:
                        if f(a) != g(phi(a)):
                            satisfies_comp = False
                            break
                    
                    if satisfies_comp:
                        valid_g_count += 1
                        if valid_g_count > 1:
                            break
                neg_q = (valid_g_count != 1)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R and T are commutative rings with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: f(s) is a unit in T for all s in S",
    "H_4: phi: R -> S^{-1}R is the canonical localization map",
    "¬Q: There does not exist a unique ring homomorphism g: S^{-1}R -> T such that f = g o phi"
]
N_HYP = 4
NEG_Q_INDEX = 4