import sympy as sp
import z3

# Top-level setup for potential witness expressions
x, y = sp.symbols('x y')

def conditions(witness):
    """
    witness is a tuple: (R_poly, f_poly)
    where R_poly is a monic irreducible quadratic in y over Z, e.g., y**2 + 5
    and f_poly is a polynomial in x with coefficients in Z[y], e.g., 3*x**2 + 4*x + 3
    """
    try:
        R_poly, f_poly = witness
        R_poly = sp.sympify(R_poly)
        f_poly = sp.sympify(f_poly)
    except Exception:
        return [False, False, False, False]

    # H1: F is the field of fractions of R.
    # We check that R_poly is a monic irreducible quadratic over Z.
    try:
        if sp.degree(R_poly, y) != 2:
            h1 = False
        elif sp.degree(R_poly, x) != 0:
            h1 = False
        elif sp.Poly(R_poly, y).nth(2) != 1:
            h1 = False
        else:
            h1 = sp.is_irreducible(R_poly, domain=sp.ZZ)
    except Exception:
        h1 = False

    # H2: f is a non-constant polynomial over R.
    try:
        deg_f = sp.degree(f_poly, x)
        if deg_f < 1:
            h2 = False
        else:
            h2 = True
            coeffs = sp.Poly(f_poly, x).all_coeffs()
            for c in coeffs:
                c_poly = sp.Poly(c, y, domain='ZZ')
                if sp.degree(c_poly, y) >= 2:
                    h2 = False
    except Exception:
        h2 = False

    # H3: f is reducible over F.
    try:
        theta = sp.RootOf(R_poly, 0)
        f_F = f_poly.subs(y, theta)
        factored = sp.factor_list(f_F, extension=theta)
        deg_sum = sum(mult for fac, mult in factored[1] if sp.degree(fac, x) >= 1)
        h3 = (deg_sum >= 2)
    except Exception:
        h3 = False

    # neg_Q: f is irreducible over R.
    try:
        R_poly_y = sp.Poly(R_poly, y)
        p = int(R_poly_y.nth(1))
        q = int(R_poly_y.nth(0))
        
        d = sp.degree(f_poly, x)
        coeffs_x = sp.Poly(f_poly, x).all_coeffs()[::-1]
        f_c = []
        for c in coeffs_x:
            c_rem = sp.rem(c, R_poly, y)
            c_poly = sp.Poly(c_rem, y)
            f_c.append([int(c_poly.nth(0)), int(c_poly.nth(1))])
            
        def norm(u0, u1):
            return u0**2 - p*u0*u1 + q*u1**2
            
        def is_unit(u0, u1):
            n = norm(u0, u1)
            return z3.Or(n == 1, n == -1)
            
        reducible = False
        for dA in range(d // 2 + 1):
            dB = d - dA
            solver = z3.Solver()
            A_vars = [[z3.Int(f'A_{dA}_{i}_0'), z3.Int(f'A_{dA}_{i}_1')] for i in range(dA + 1)]
            B_vars = [[z3.Int(f'B_{dA}_{i}_0'), z3.Int(f'B_{dA}_{i}_1')] for i in range(dB + 1)]
            
            solver.add(z3.Or(A_vars[dA][0] != 0, A_vars[dA][1] != 0))
            solver.add(z3.Or(B_vars[dB][0] != 0, B_vars[dB][1] != 0))
            
            for k in range(d + 1):
                C_k0 = 0
                C_k1 = 0
                for i in range(max(0, k - dB), min(dA, k) + 1):
                    j = k - i
                    u0, u1 = A_vars[i]
                    v0, v1 = B_vars[j]
                    
                    term00 = u0 * v0
                    term01 = u0 * v1
                    term10 = u1 * v0
                    term11 = u1 * v1
                    
                    C_k0 += term00 * 1 + term11 * (-q)
                    C_k1 += term01 * 1 + term10 * 1 + term11 * (-p)
                    
                solver.add(C_k0 == f_c[k][0])
                solver.add(C_k1 == f_c[k][1])
                
            if dA == 0:
                solver.add(z3.Not(is_unit(A_vars[0][0], A_vars[0][1])))
            else:
                if dB == 0:
                    solver.add(z3.Not(is_unit(B_vars[0][0], B_vars[0][1])))
                
            solver.set("timeout", 2000)
            if solver.check() == z3.sat:
                reducible = True
                break
                
        neg_q = not reducible
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is the field of fractions of R",
    "H_2: f is a non-constant polynomial over R",
    "H_3: f is reducible over F",
    "¬Q: f is irreducible over R"
]

N_HYP = 3
NEG_Q_INDEX = 3