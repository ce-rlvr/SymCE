import sympy
import math

# Top-level setup
# We define standard objects that might be useful, though the verifier
# is robust enough to parse standard SymPy expressions and infer the ring.
Z_sqrt_minus_5 = "Z[sqrt(-5)]"
Z_sqrt_minus_3 = "Z[sqrt(-3)]"

def get_witness_elements(witness):
    if isinstance(witness, str):
        try:
            witness = sympy.sympify(witness)
        except Exception:
            pass
    if isinstance(witness, (tuple, list, sympy.Tuple)):
        return list(witness)
    return [witness]

class Z_sqrt_d_Element:
    def __init__(self, u, v, d):
        self.u = int(u)
        self.v = int(v)
        self.d = int(d)
        
    def norm(self):
        return self.u**2 - self.d * self.v**2
        
    def __mul__(self, other):
        return Z_sqrt_d_Element(
            self.u * other.u + self.d * self.v * other.v,
            self.u * other.v + self.v * other.u,
            self.d
        )
        
    def divides(self, other):
        n = self.norm()
        if n == 0:
            return False
        conj = Z_sqrt_d_Element(self.u, -self.v, self.d)
        prod = other * conj
        return prod.u % n == 0 and prod.v % n == 0
        
    def is_irreducible(self):
        n = self.norm()
        if n <= 1 or n > 10000:
            return False
        for v in range(-int(math.isqrt(n // -self.d)) - 1, int(math.isqrt(n // -self.d)) + 2):
            for u in range(-int(math.isqrt(n)) - 1, int(math.isqrt(n)) + 2):
                cand = Z_sqrt_d_Element(u, v, self.d)
                cn = cand.norm()
                if 1 < cn < n:
                    if cand.divides(self):
                        return False
        return True
        
    def is_not_prime(self):
        elements = []
        for v in range(-4, 5):
            for u in range(-8, 9):
                cand = Z_sqrt_d_Element(u, v, self.d)
                if cand.norm() > 0 and not self.divides(cand):
                    elements.append(cand)
        
        for i in range(len(elements)):
            a = elements[i]
            for j in range(i, len(elements)):
                b = elements[j]
                if self.divides(a * b):
                    return True
        return False

def parse_Z_sqrt_d(expr):
    expr = sympy.sympify(expr)
    expr = sympy.expand(expr)
    if expr.is_Integer:
        return int(expr), 0, -5
    
    re, im = expr.as_real_imag()
    if not re.is_Integer:
        return None
        
    im2 = im**2
    if not im2.is_Integer:
        return None
        
    im2 = int(im2)
    if im2 == 0:
        return int(re), 0, -5
        
    for d in [-5, -3, -6, -7, -10, -13, -14, -15, -17]:
        if im2 % (-d) == 0:
            v2 = im2 // (-d)
            v = math.isqrt(v2)
            if v**2 == v2:
                if im.evalf() < 0:
                    v = -v
                return int(re), v, d
    return None

def evaluate_Z_sqrt_d(witness):
    elements = get_witness_elements(witness)
    if not elements:
        return False, False
        
    d = -5
    for expr in elements:
        try:
            res = parse_Z_sqrt_d(expr)
            if res is not None and res[1] != 0:
                d = res[2]
                break
        except Exception:
            pass
            
    p_expr = elements[0]
    try:
        if isinstance(p_expr, int):
            p_obj = Z_sqrt_d_Element(p_expr, 0, d)
        else:
            res = parse_Z_sqrt_d(p_expr)
            if res is not None:
                p_obj = Z_sqrt_d_Element(res[0], res[1], d)
            else:
                return False, False
    except Exception:
        return False, False
        
    h1 = p_obj.is_irreducible()
    neg_q = p_obj.is_not_prime()
    
    if not neg_q and len(elements) >= 3:
        try:
            res_a = parse_Z_sqrt_d(elements[1])
            res_b = parse_Z_sqrt_d(elements[2])
            if res_a and res_b:
                a_obj = Z_sqrt_d_Element(res_a[0], res_a[1], d)
                b_obj = Z_sqrt_d_Element(res_b[0], res_b[1], d)
                if p_obj.divides(a_obj * b_obj) and not p_obj.divides(a_obj) and not p_obj.divides(b_obj):
                    neg_q = True
        except Exception:
            pass
            
    return h1, neg_q

def check_polynomial_witness(witness):
    elements = get_witness_elements(witness)
    p_expr = sympy.sympify(elements[0])
    
    from sympy import Poly
    
    try:
        free_symbols = p_expr.free_symbols
        if len(free_symbols) != 1:
            return False, False
        var = list(free_symbols)[0]
        
        p = Poly(p_expr, var)
        if p.coeff_monomial(var) != 0:
            return False, False
            
        deg = p.degree()
        if deg not in [2, 3]:
            return False, False
            
        h1 = True
        
        def divides_in_R(a, b):
            try:
                q, r = sympy.div(b, a, domain='QQ')
                if r != 0:
                    return False
                if sympy.sympify(q).is_Number:
                    return True
                q_poly = Poly(q, var)
                return q_poly.coeff_monomial(var) == 0
            except Exception:
                return False
                
        cands = [var**2, var**3, var**4, var**5]
        neg_q = False
        for a in cands:
            for b in cands:
                if divides_in_R(p_expr, a * b) and not divides_in_R(p_expr, a) and not divides_in_R(p_expr, b):
                    neg_q = True
                    break
            if neg_q:
                break
                
        if not neg_q and len(elements) >= 3:
            a = sympy.sympify(elements[1])
            b = sympy.sympify(elements[2])
            if divides_in_R(p_expr, a * b) and not divides_in_R(p_expr, a) and not divides_in_R(p_expr, b):
                neg_q = True
                
        return h1, neg_q
    except Exception:
        return False, False

def conditions(witness) -> list[bool]:
    best_h1 = False
    best_neg_q = False
    
    def update_best(h1, neg_q):
        nonlocal best_h1, best_neg_q
        if h1 and neg_q:
            best_h1, best_neg_q = True, True
            return True
        if h1:
            best_h1 = True
        if neg_q:
            best_neg_q = True
        return False

    try:
        if hasattr(witness, 'is_irreducible') and (hasattr(witness, 'is_prime') or hasattr(witness, 'is_not_prime')):
            h1 = bool(witness.is_irreducible())
            if hasattr(witness, 'is_not_prime'):
                neg_q = bool(witness.is_not_prime())
            else:
                neg_q = not bool(witness.is_prime())
            if update_best(h1, neg_q): return [True, True]
    except Exception:
        pass

    try:
        h1, neg_q = evaluate_Z_sqrt_d(witness)
        if update_best(h1, neg_q): return [True, True]
    except Exception:
        pass
        
    try:
        h1, neg_q = check_polynomial_witness(witness)
        if update_best(h1, neg_q): return [True, True]
    except Exception:
        pass
        
    return [best_h1, best_neg_q]

CONDITION_LABELS = [
    "H_1: p is an irreducible element in R",
    "¬Q: The element p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1