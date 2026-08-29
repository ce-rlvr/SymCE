import sympy
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a local ring with maximal ideal m and residue field k = R/m",
    "H_2: R is complete with respect to the m-adic topology",
    "H_3: f is a monic polynomial over R",
    "H_4: The reduction f_bar factors as g_0 h_0, where g_0, h_0 are monic and coprime polynomials over k",
    "¬Q: There do NOT exist monic polynomials g, h over R such that f = g h, where g reduces to g_0 and h reduces to h_0 modulo m"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False] * 5
            
        R = witness.get('R', [])
        m = witness.get('m', [])
        f = witness.get('f', [])
        g0 = witness.get('g0', [])
        h0 = witness.get('h0', [])
        p = witness.get('p', 0)
        
        if not R or not m or not f or not g0 or not h0:
            return [False] * 5
            
        first_elem = R[0]
        is_matrix = hasattr(first_elem, 'rows')
        
        if is_matrix:
            I = sympy.eye(first_elem.rows)
            Z_elem = sympy.zeros(first_elem.rows, first_elem.cols)
        else:
            I = 1
            Z_elem = 0

        def eq(A, B):
            if is_matrix:
                if p:
                    return all((a - b) % p == 0 for a, b in zip(A, B))
                return A == B
            else:
                return (A - B) % p == 0 if p else A == B

        def add(A, B):
            if is_matrix:
                return (A + B).applyfunc(lambda x: x % p) if p else A + B
            return (A + B) % p if p else A + B

        def mul(A, B):
            if is_matrix:
                return (A * B).applyfunc(lambda x: x % p) if p else A * B
            return (A * B) % p if p else A * B

        def sub(A, B):
            if is_matrix:
                return (A - B).applyfunc(lambda x: x % p) if p else A - B
            return (A - B) % p if p else A - B

        def is_in(A, S):
            return any(eq(A, X) for X in S)

        # H_1: R is a local ring with maximal ideal m
        h1 = True
        if not is_in(I, R) or not is_in(Z_elem, R) or eq(I, Z_elem):
            h1 = False
            
        if h1:
            for A in R:
                for B in R:
                    if not is_in(add(A, B), R): h1 = False
                    if not is_in(mul(A, B), R): h1 = False
                    if not is_in(sub(A, B), R): h1 = False
                    
        if h1:
            for A in m:
                if not is_in(A, R): h1 = False
                for B in R:
                    if not is_in(mul(A, B), m): h1 = False
                    if not is_in(mul(B, A), m): h1 = False
            for A in m:
                for B in m:
                    if not is_in(add(A, B), m): h1 = False
                    
        if h1:
            for A in R:
                if not is_in(A, m):
                    is_unit = False
                    for B in R:
                        if eq(mul(A, B), I) and eq(mul(B, A), I):
                            is_unit = True
                            break
                    if not is_unit:
                        h1 = False
                        break

        # H_2: R is complete with respect to the m-adic topology
        h2 = False
        if h1:
            current_ideal = list(m)
            for _ in range(len(R) + 1):
                if all(eq(X, Z_elem) for X in current_ideal):
                    h2 = True
                    break
                generators = [mul(x, y) for x in current_ideal for y in m]
                closure = [Z_elem]
                for g in generators:
                    if is_in(g, closure): continue
                    cosets = []
                    curr_g = g
                    while not is_in(curr_g, closure):
                        cosets.append(curr_g)
                        curr_g = add(curr_g, g)
                    
                    new_elems = []
                    for c in closure:
                        for cg in cosets:
                            s = add(c, cg)
                            if not is_in(s, closure) and not is_in(s, new_elems):
                                new_elems.append(s)
                    closure.extend(cosets)
                    closure.extend(new_elems)
                current_ideal = closure

        # H_3: f is a monic polynomial over R
        h3 = False
        if f and len(f) > 0:
            if eq(f[-1], I):
                h3 = all(is_in(c, R) for c in f)

        def poly_mul(p1, p2):
            res = [Z_elem] * (len(p1) + len(p2) - 1)
            for i, c1 in enumerate(p1):
                for j, c2 in enumerate(p2):
                    res[i+j] = add(res[i+j], mul(c1, c2))
            return res

        def poly_eq_mod_m(p1, p2):
            n = max(len(p1), len(p2))
            for i in range(n):
                c1 = p1[i] if i < len(p1) else Z_elem
                c2 = p2[i] if i < len(p2) else Z_elem
                if not is_in(sub(c1, c2), m):
                    return False
            return True

        # H_4: f_bar = g_0 h_0 in k[x], g_0, h_0 monic and coprime
        h4 = False
        if h1 and g0 and h0 and len(g0) > 0 and len(h0) > 0:
            if eq(g0[-1], I) and eq(h0[-1], I):
                if all(is_in(c, R) for c in g0) and all(is_in(c, R) for c in h0):
                    prod = poly_mul(g0, h0)
                    if poly_eq_mod_m(f, prod):
                        k_elems = []
                        for A in R:
                            if not any(is_in(sub(A, B), m) for B in k_elems):
                                k_elems.append(A)
                        
                        deg_a = len(h0) - 1
                        deg_b = len(g0) - 1
                        
                        def gen_polys(deg):
                            if deg <= 0:
                                yield [Z_elem]
                                return
                            for coeffs in itertools.product(k_elems, repeat=deg):
                                yield list(coeffs)
                        
                        coprime = False
                        for a_poly in gen_polys(deg_a):
                            for b_poly in gen_polys(deg_b):
                                ag = poly_mul(a_poly, g0)
                                bh = poly_mul(b_poly, h0)
                                sum_ab = [add(c1, c2) for c1, c2 in itertools.zip_longest(ag, bh, fillvalue=Z_elem)]
                                if poly_eq_mod_m(sum_ab, [I]):
                                    coprime = True
                                    break
                            if coprime:
                                break
                        h4 = coprime

        # neg_Q: There do NOT exist monic g, h over R such that f = g h, g = g0 mod m, h = h0 mod m
        neg_q = True
        if h1 and h3 and h4:
            def gen_lifts(poly):
                lifts = []
                m_tuples = list(itertools.product(m, repeat=len(poly)-1))
                for mt in m_tuples:
                    lift = []
                    for i in range(len(poly)-1):
                        lift.append(add(poly[i], mt[i]))
                    lift.append(poly[-1])
                    lifts.append(lift)
                return lifts
            
            g_lifts = gen_lifts(g0)
            h_lifts = gen_lifts(h0)
            
            for g in g_lifts:
                for h in h_lifts:
                    prod = poly_mul(g, h)
                    n = max(len(f), len(prod))
                    exact_eq = True
                    for i in range(n):
                        c1 = f[i] if i < len(f) else Z_elem
                        c2 = prod[i] if i < len(prod) else Z_elem
                        if not eq(c1, c2):
                            exact_eq = False
                            break
                    if exact_eq:
                        neg_q = False
                        break
                if not neg_q:
                    break

        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False] * 5