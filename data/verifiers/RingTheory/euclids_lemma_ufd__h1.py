import sympy as sp
import sympy.combinatorics.named_groups
import sympy.matrices
import math

# Top-level setup
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def get_D(exprs):
    for expr in exprs:
        if not isinstance(expr, sp.Basic):
            expr = sp.sympify(expr)
        if expr.has(sp.I):
            pows = [arg for arg in expr.atoms(sp.Pow) if arg.exp == sp.S.Half and arg.base.is_integer]
            if pows:
                return -int(pows[0].base)
            else:
                return -1
        else:
            pows = [arg for arg in expr.atoms(sp.Pow) if arg.exp == sp.S.Half and arg.base.is_integer]
            if pows:
                return int(pows[0].base)
    return 1

def get_coeffs(expr, D):
    if D == 1:
        return sp.sympify(expr), sp.S(0)
    expr = sp.expand(sp.sympify(expr))
    if D < 0:
        rad = sp.I * sp.sqrt(-D)
    else:
        rad = sp.sqrt(D)
    
    expr_conj = expr.subs(rad, -rad)
    A = sp.simplify((expr + expr_conj) / 2)
    B = sp.simplify((expr - expr_conj) / (2 * rad))
    return A, B

def get_ring_type(exprs, D):
    for expr in exprs:
        A, B = get_coeffs(expr, D)
        try:
            A = sp.Rational(A)
            B = sp.Rational(B)
            if not (A.is_integer and B.is_integer):
                return 'half'
        except TypeError:
            pass
    return 'int'

def is_in_ring(A, B, ring_type):
    try:
        A = sp.Rational(A)
        B = sp.Rational(B)
    except TypeError:
        return False
    if ring_type == 'half':
        u = 2 * A
        v = 2 * B
        return u.is_integer and v.is_integer and (u - v) % 2 == 0
    else:
        return A.is_integer and B.is_integer

def divides(x, y, D, ring_type):
    A1, B1 = get_coeffs(x, D)
    if A1 == 0 and B1 == 0:
        A2, B2 = get_coeffs(y, D)
        return A2 == 0 and B2 == 0
    
    norm_x = A1**2 - D * B1**2
    if norm_x == 0:
        return False
    
    if D < 0:
        rad = sp.I * sp.sqrt(-D)
    else:
        rad = sp.sqrt(D)
        
    conj_x = A1 - B1 * rad
    q = sp.expand(y * conj_x)
    Aq, Bq = get_coeffs(q, D)
    
    A_div = Aq / norm_x
    B_div = Bq / norm_x
    
    return is_in_ring(A_div, B_div, ring_type)

def norm(x, D):
    A, B = get_coeffs(x, D)
    return A**2 - D * B**2

def get_elements_of_norm(k, D, ring_type):
    elements = []
    if D == 1:
        target_k = [k, -k]
        for tk in target_k:
            if tk < 0: continue
            A = int(math.isqrt(tk))
            if A**2 == tk:
                elements.append((A, 0))
                if A != 0:
                    elements.append((-A, 0))
        return elements

    if D < 0:
        target = 4 * k if ring_type == 'half' else k
        max_B = int(math.isqrt(target // (-D))) if target >= 0 else 0
        for B in range(-max_B, max_B + 1):
            rem = target + D * B**2
            if rem < 0:
                continue
            A = int(math.isqrt(rem))
            if A**2 == rem:
                if ring_type == 'half':
                    if (A - B) % 2 == 0:
                        elements.append((sp.Rational(A, 2), sp.Rational(B, 2)))
                        if A != 0:
                            elements.append((sp.Rational(-A, 2), sp.Rational(B, 2)))
                else:
                    elements.append((A, B))
                    if A != 0:
                        elements.append((-A, B))
    else:
        target_k = [k, -k]
        for tk in target_k:
            target = 4 * tk if ring_type == 'half' else tk
            for B in range(-1000, 1001):
                rem = target + D * B**2
                if rem < 0:
                    continue
                A = int(math.isqrt(rem))
                if A**2 == rem:
                    if ring_type == 'half':
                        if (A - B) % 2 == 0:
                            elements.append((sp.Rational(A, 2), sp.Rational(B, 2)))
                            if A != 0:
                                elements.append((sp.Rational(-A, 2), sp.Rational(B, 2)))
                    else:
                        elements.append((A, B))
                        if A != 0:
                            elements.append((-A, B))
    return elements

def coprime(a, b, D, ring_type):
    n_a = abs(norm(a, D))
    n_b = abs(norm(b, D))
    if n_a == 0 or n_b == 0:
        return False
    
    try:
        n_a = int(n_a)
        n_b = int(n_b)
    except TypeError:
        return False
        
    g = math.gcd(n_a, n_b)
    
    divs = []
    for i in range(1, int(math.isqrt(g)) + 1):
        if g % i == 0:
            divs.append(i)
            if i * i != g:
                divs.append(g // i)
                
    if D < 0:
        rad = sp.I * sp.sqrt(-D)
    else:
        rad = sp.sqrt(D)
        
    for d_norm in divs:
        if d_norm == 1:
            continue
        elems = get_elements_of_norm(d_norm, D, ring_type)
        for A, B in elems:
            d = A + B * rad
            if divides(d, a, D, ring_type) and divides(d, b, D, ring_type):
                return False
    return True

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
        a = sp.sympify(a)
        b = sp.sympify(b)
        c = sp.sympify(c)
    except Exception:
        return [False, False, False, False]
        
    try:
        D = get_D([a, b, c])
        ring_type = get_ring_type([a, b, c], D)
    except Exception:
        return [False, False, False, False]
        
    # H1: a, b, and c are non-zero elements of R
    try:
        A_a, B_a = get_coeffs(a, D)
        A_b, B_b = get_coeffs(b, D)
        A_c, B_c = get_coeffs(c, D)
        h1 = not (A_a == 0 and B_a == 0) and not (A_b == 0 and B_b == 0) and not (A_c == 0 and B_c == 0)
    except Exception:
        h1 = False
        
    # H2: a divides the product bc
    try:
        bc = sp.expand(b * c)
        h2 = divides(a, bc, D, ring_type)
    except Exception:
        h2 = False
        
    # H3: a and b are coprime
    try:
        h3 = coprime(a, b, D, ring_type)
    except Exception:
        h3 = False
        
    # neg_Q: a does not divide c
    try:
        q = divides(a, c, D, ring_type)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are non-zero elements of R",
    "H_2: a divides the product bc",
    "H_3: a and b are coprime",
    "¬Q: a does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3