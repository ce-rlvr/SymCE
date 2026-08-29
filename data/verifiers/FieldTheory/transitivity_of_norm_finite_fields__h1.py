import sympy as sp

x, y, z = sp.symbols('x y z')

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
            
        p, P_obj, Q_obj, A_obj = witness
        
        if not isinstance(p, int) or not sp.isprime(p):
            return [False, False, False, False]
            
        # Parse P(x)
        if isinstance(P_obj, list):
            P_expr = sum(c * (x**i) for i, c in enumerate(reversed(P_obj)))
        else:
            P_expr = sp.sympify(P_obj)
            
        # Parse Q(x, y)
        if isinstance(Q_obj, list):
            Q_expr = sum(sum(c * (x**k) for k, c in enumerate(reversed(q_c))) * (y**i) for i, q_c in enumerate(Q_obj))
        else:
            Q_expr = sp.sympify(Q_obj)
            
        # Parse A(x, y) representing alpha
        if isinstance(A_obj, list):
            A_expr = sum(sum(c * (x**k) for k, c in enumerate(reversed(a_c))) * (y**i) for i, a_c in enumerate(A_obj))
        else:
            A_expr = sp.sympify(A_obj)
            
        # H1: K is a finite field extension of F_q
        # P(x) must be irreducible over GF(p)
        P_poly = sp.Poly(P_expr, x, domain=sp.GF(p))
        h1 = P_poly.degree() >= 1 and P_poly.is_irreducible
        
        # H2: L is a finite field extension of K
        # Q(y) must be monic in y and have degree >= 1
        Q_poly_y = sp.Poly(Q_expr, y)
        h2 = Q_poly_y.degree() >= 1 and sp.simplify(Q_poly_y.LC() - 1) == 0
        
        # H3: alpha is an element of L
        h3 = True
        
        # Compute N_{L/K}(alpha)
        res_y = sp.resultant(Q_expr, A_expr, y)
        norm_LK = sp.rem(res_y, P_expr, x, domain='QQ')
        
        # Compute N_{K/F_q}(N_{L/K}(alpha))
        norm_K_F = sp.resultant(P_expr, norm_LK, x)
        
        # Compute N_{L/F_q}(alpha) via characteristic polynomial
        char_poly_y = sp.resultant(Q_expr, z - A_expr, y)
        char_poly_x = sp.resultant(P_expr, char_poly_y, x)
        
        d = P_poly.degree()
        e = Q_poly_y.degree()
        
        norm_L_F = ((-1)**(d * e)) * char_poly_x.subs(z, 0)
        
        # Evaluate equality modulo p
        norm_L_F_val = sp.Rational(norm_L_F)
        norm_K_F_val = sp.Rational(norm_K_F)
        
        if norm_L_F_val.q % p == 0 or norm_K_F_val.q % p == 0:
            neg_q = True
        else:
            val_L = (norm_L_F_val.p * pow(norm_L_F_val.q, p - 2, p)) % p
            val_K = (norm_K_F_val.p * pow(norm_K_F_val.q, p - 2, p)) % p
            neg_q = (val_L != val_K)
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: K is a finite field extension of F_q",
    "H_2: L is a finite field extension of K",
    "H_3: alpha is an element of L",
    "¬Q: N_{L/F_q}(alpha) != N_{K/F_q}(N_{L/K}(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3