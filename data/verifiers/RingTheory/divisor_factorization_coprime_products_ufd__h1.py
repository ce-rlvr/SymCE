import math
from sympy import expand, radsimp, cancel, Dummy, Pow, Rational, Poly, sqrt, I, sympify
from sympy.abc import x, y, z

# Top-level setup
# No specific named bindings are required for this ring theory conjecture,
# but we provide common symbols.

def get_k(exprs):
    for expr in exprs:
        if hasattr(expr, 'atoms'):
            for atom in expr.atoms(Pow):
                if atom.exp == Rational(1, 2):
                    if atom.base.is_Integer and atom.base < 0:
                        return int(atom.base)
    return -5

def norm(val, k):
    try:
        val = sympify(val)
        val = expand(val)
        s = sqrt(k)
        val_conj = val.subs(s, -s)
        n = expand(val * val_conj)
        if n.is_Integer:
            return int(n)
        return None
    except Exception:
        return None

def get_elements_of_norm(m, k):
    if m < 0 or k >= 0:
        return []
    elements = []
    abs_k = -k
    max_v = int((m / abs_k)**0.5)
    s = sqrt(k)
    for v in range(max_v + 1):
        rem = m - abs_k * v**2
        if rem < 0:
            continue
        u = int(rem**0.5)
        if u**2 == rem:
            elements.append(u + v*s)
            if u != 0:
                elements.append(-u + v*s)
            if v != 0:
                elements.append(u - v*s)
                if u != 0:
                    elements.append(-u - v*s)
    return list(set(elements))

def divides(num_x, num_y):
    try:
        num_x = sympify(num_x)
        num_y = sympify(num_y)
        if num_x == 0:
            return bool(num_y == 0)
        q = expand(radsimp(cancel(num_y / num_x)))
        if q.is_Integer:
            return True
        
        subs_dict = {}
        for atom in q.atoms(Pow):
            if atom.exp == Rational(1, 2):
                subs_dict[atom] = Dummy()
        
        if not subs_dict:
            return False
            
        q_sub = q.subs(subs_dict)
        symbols = list(q_sub.free_symbols)
        if not symbols:
            return q_sub.is_Integer
            
        p = Poly(q_sub, *symbols)
        return all(c.is_Integer for c in p.coeffs())
    except Exception:
        return False

def is_coprime(a, b, k):
    na = norm(a, k)
    nb = norm(b, k)
    if na is None or nb is None:
        return False
    if na == 0 and nb == 0:
        return False
    g = math.gcd(na, nb)
    
    divisors = []
    for i in range(1, int(g**0.5) + 1):
        if g % i == 0:
            divisors.append(i)
            divisors.append(g // i)
    divisors = list(set(divisors))
    
    for m in divisors:
        if m == 1:
            continue
        cands = get_elements_of_norm(m, k)
        for c in cands:
            if divides(c, a) and divides(c, b):
                return False
    return True

def are_pairs_equivalent(p1, p2, units):
    d1, d2 = p1
    e1, e2 = p2
    for u in units:
        if expand(d1 * u) == expand(e1):
            if expand(e2 * u) == expand(d2):
                return True
    return False

def check_conclusion(a, b, d, k):
    na = norm(a, k)
    nb = norm(b, k)
    nd = norm(d, k)
    
    if na is None or nb is None or nd is None:
        return False
        
    divs_a = [i for i in range(1, na + 1) if na % i == 0]
    divs_b = [i for i in range(1, nb + 1) if nb % i == 0]
    
    valid_pairs = []
    
    for m1 in divs_a:
        for m2 in divs_b:
            if m1 * m2 == nd:
                cands1 = get_elements_of_norm(m1, k)
                cands2 = get_elements_of_norm(m2, k)
                for d1 in cands1:
                    if not divides(d1, a): continue
                    for d2 in cands2:
                        if not divides(d2, b): continue
                        if expand(d1 * d2) == expand(d):
                            valid_pairs.append((d1, d2))
                            
    if len(valid_pairs) == 0:
        return True
        
    units = get_elements_of_norm(1, k)
    unique_classes = []
    for pair in valid_pairs:
        is_new = True
        for eq_class in unique_classes:
            if are_pairs_equivalent(pair, eq_class[0], units):
                eq_class.append(pair)
                is_new = False
                break
        if is_new:
            unique_classes.append([pair])
            
    if len(unique_classes) == 1:
        return False
    else:
        return True

def conditions(witness):
    try:
        if len(witness) == 3:
            a, b, d = [sympify(w) for w in witness]
            k = get_k([a, b, d])
        elif len(witness) == 4:
            a, b, d, k = witness
            a, b, d = [sympify(w) for w in (a, b, d)]
            k = int(k)
        else:
            return [False, False, False]
            
        if k >= 0:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        a_nonzero = (expand(a) != 0)
        b_nonzero = (expand(b) != 0)
        coprime = is_coprime(a, b, k)
        h1 = bool(a_nonzero and b_nonzero and coprime)
    except Exception:
        h1 = False
        
    try:
        ab = expand(a * b)
        h2 = bool(divides(d, ab))
    except Exception:
        h2 = False
        
    try:
        neg_q = bool(check_conclusion(a, b, d, k))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are non-zero and gcd(a,b)=1",
    "H_2: d divides ab",
    "¬Q: d does not uniquely factor into d1*d2 with d1|a and d2|b"
]

N_HYP = 2
NEG_Q_INDEX = 2