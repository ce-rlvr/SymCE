import itertools
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.ntheory import factorint

x = sympy.Symbol('x')

# Standard algebra objects
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def is_prime_power(q):
    if not isinstance(q, int) or q < 2:
        return False, 0, 0
    f = factorint(q)
    if len(f) != 1:
        return False, 0, 0
    p, k = list(f.items())[0]
    return True, p, k

def get_irreducible_poly(p, n):
    if n == 1:
        return (0, 1)
    for coeffs in itertools.product(range(p), repeat=n):
        c = list(coeffs) + [1]
        poly = sympy.Poly(list(reversed(c)), x, domain=f'GF({p})')
        if poly.is_irreducible:
            return tuple(c)
    return None

def add_ff(a, b, p):
    return tuple((x_i + y_i) % p for x_i, y_i in zip(a, b))

def mul_ff(a, b, p, irred_poly):
    n = len(a)
    res = [0] * (2 * n - 1)
    if n == 1:
        return ((a[0] * b[0]) % p,)
    for i in range(n):
        if a[i] == 0: continue
        for j in range(n):
            res[i+j] = (res[i+j] + a[i] * b[j]) % p
    for i in range(2 * n - 2, n - 1, -1):
        if res[i] != 0:
            lead = res[i]
            for j in range(n):
                res[i - n + j] = (res[i - n + j] - lead * irred_poly[j]) % p
    return tuple(res[:n])

def power_ff(a, exp, p, irred_poly):
    n = len(a)
    res = tuple([1] + [0]*(n-1))
    base = a
    while exp > 0:
        if exp % 2 == 1:
            res = mul_ff(res, base, p, irred_poly)
        base = mul_ff(base, base, p, irred_poly)
        exp //= 2
    return res

def poly_div_linear(coeffs, r, p, irred_poly):
    n = len(r)
    d = len(coeffs) - 1
    if d < 0:
        return [], tuple([0]*n)
    if d == 0:
        return [], coeffs[0]
    q_coeffs = [tuple([0]*n)] * d
    q_coeffs[d-1] = coeffs[d]
    for i in range(d-2, -1, -1):
        q_coeffs[i] = add_ff(coeffs[i+1], mul_ff(r, q_coeffs[i+1], p, irred_poly), p)
    rem = add_ff(coeffs[0], mul_ff(r, q_coeffs[0], p, irred_poly), p)
    return q_coeffs, rem

def strip_zeros(coeffs, zero):
    while len(coeffs) > 0 and coeffs[-1] == zero:
        coeffs = coeffs[:-1]
    return coeffs

def get_all_roots(coeffs, p, n, irred_poly):
    roots = []
    total_mult = 0
    zero = tuple([0]*n)
    elements = list(itertools.product(range(p), repeat=n))
    
    for elem in elements:
        val = tuple(elem)
        mult = 0
        current_coeffs = coeffs
        while len(current_coeffs) > 1:
            q_coeffs, rem = poly_div_linear(current_coeffs, val, p, irred_poly)
            if rem == zero:
                mult += 1
                current_coeffs = strip_zeros(q_coeffs, zero)
            else:
                break
        if mult > 0:
            roots.append(val)
            total_mult += mult
            
    return roots, total_mult

def get_Fq_elements(p, n, q, irred_poly):
    Fq = []
    for elem in itertools.product(range(p), repeat=n):
        val = tuple(elem)
        if power_ff(val, q, p, irred_poly) == val:
            Fq.append(val)
    return Fq

def is_vector_space(roots, Fq, p, irred_poly):
    zero = tuple([0]*len(irred_poly[:-1]))
    if zero not in roots:
        return False
    roots_set = set(roots)
    for u in roots:
        for v in roots:
            if add_ff(u, v, p) not in roots_set:
                return False
    for c in Fq:
        for u in roots:
            if mul_ff(c, u, p, irred_poly) not in roots_set:
                return False
    return True

def parse_coeff(c, p, n):
    if isinstance(c, int):
        res = [0]*n
        res[0] = c % p
        return tuple(res)
    elif isinstance(c, (list, tuple)):
        res = [0]*n
        for i in range(min(n, len(c))):
            res[i] = c[i] % p
        return tuple(res)
    else:
        raise ValueError("Invalid coefficient format")

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            m = witness.get('m')
            L_coeffs = witness.get('L_coeffs')
            E_deg = witness.get('E_deg', 1)
        elif isinstance(witness, (list, tuple)):
            q = witness[0]
            m = witness[1]
            L_coeffs = witness[2]
            E_deg = witness[3] if len(witness) > 3 else 1
        else:
            return [False, False, False]
            
        # H1: F_q is a finite field
        is_pp, p, k = is_prime_power(q)
        h1 = is_pp
        
        if not h1:
            return [False, False, False]
            
        # H2: E is an extension field of F_{q^m} containing all roots of L(x)
        if not isinstance(m, int) or m < 1:
            return [True, False, False]
        if not isinstance(E_deg, int) or E_deg < 1:
            return [True, False, False]
        if not isinstance(L_coeffs, (list, tuple)) or len(L_coeffs) > 100:
            return [True, False, False]
            
        n = k * m * E_deg
        
        if p**n > 1024:
            return [True, False, False]
            
        irred_poly = get_irreducible_poly(p, n)
        if irred_poly is None:
            return [True, False, False]
            
        zero_elem = tuple([0]*n)
        try:
            coeffs_ff = [parse_coeff(c, p, n) for c in L_coeffs]
        except Exception:
            return [True, False, False]
            
        coeffs_ff = strip_zeros(coeffs_ff, zero_elem)
        
        if len(coeffs_ff) == 0:
            h2 = True
            roots = [tuple(elem) for elem in itertools.product(range(p), repeat=n)]
        else:
            degree = len(coeffs_ff) - 1
            roots, total_mult = get_all_roots(coeffs_ff, p, n, irred_poly)
            h2 = (total_mult == degree)
            
        if not h2:
            return [True, False, False]
            
        # Conclusion: The set of roots of L(x) in E forms a vector space over F_q
        Fq = get_Fq_elements(p, n, q, irred_poly)
        is_vs = is_vector_space(roots, Fq, p, irred_poly)
        neg_q = not is_vs
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: E is an extension field of F_{q^m} containing all roots of L(x)",
    "¬Q: The roots of L(x) in E do not form a vector space over F_q"
]

N_HYP = 2
NEG_Q_INDEX = 2