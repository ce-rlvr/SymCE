import sympy
from sympy import ZZ, QQ, Poly
from sympy.abc import x, y, z

def conditions(witness):
    try:
        R = witness['R']
        S = witness['S']
        phi = witness['phi']
        f = witness['f']
        Phi_f = witness['Phi_f']
        c = witness['c']
    except Exception:
        return [False, False, False, False, False]

    def divides(domain, a, b):
        if a == domain.zero:
            return b == domain.zero
        try:
            domain.exquo(b, a)
            return True
        except Exception:
            return False

    def is_assoc(domain, a, b):
        return divides(domain, a, b) and divides(domain, b, a)

    try:
        h1 = bool(R.is_UFD and S.is_UFD)
    except Exception:
        h1 = False

    try:
        h2 = True
        f_coeffs = [R.convert(a) for a in f.all_coeffs()]
        Phi_f_coeffs = [S.convert(a) for a in Phi_f.all_coeffs()]
        c_R = R.convert(c)
        
        coeffs = f_coeffs + [c_R, R.one, R.zero]
        for a in coeffs:
            phi_a = S.convert(phi(a))
            for b in coeffs:
                phi_b = S.convert(phi(b))
                
                sum_ab = R.add(a, b)
                phi_sum = S.convert(phi(sum_ab))
                sum_phi = S.add(phi_a, phi_b)
                if phi_sum != sum_phi:
                    h2 = False
                
                mul_ab = R.mul(a, b)
                phi_mul = S.convert(phi(mul_ab))
                mul_phi = S.mul(phi_a, phi_b)
                if phi_mul != mul_phi:
                    h2 = False
                    
        if S.convert(phi(R.one)) != S.one:
            h2 = False
        if S.convert(phi(R.zero)) != S.zero:
            h2 = False
            
        phi_inv = witness.get('phi_inv', None)
        if phi_inv is not None:
            for a in coeffs:
                if R.convert(phi_inv(S.convert(phi(a)))) != a:
                    h2 = False
            for b in Phi_f_coeffs + [S.convert(phi(c_R)), S.one, S.zero]:
                if S.convert(phi(R.convert(phi_inv(b)))) != b:
                    h2 = False
    except Exception:
        h2 = False

    try:
        f_coeffs = [R.convert(a) for a in f.all_coeffs()]
        Phi_f_coeffs = [S.convert(a) for a in Phi_f.all_coeffs()]
        expected_coeffs = [S.convert(phi(a)) for a in f_coeffs]
        h3 = (Phi_f_coeffs == expected_coeffs)
    except Exception:
        h3 = False

    try:
        f_coeffs = [R.convert(a) for a in f.all_coeffs()]
        c_R = R.convert(c)
        content_f = f_coeffs[0]
        for a in f_coeffs[1:]:
            content_f = R.gcd(content_f, a)
        h4 = is_assoc(R, c_R, content_f)
    except Exception:
        h4 = False

    try:
        Phi_f_coeffs = [S.convert(a) for a in Phi_f.all_coeffs()]
        c_R = R.convert(c)
        content_Phi_f = Phi_f_coeffs[0]
        for a in Phi_f_coeffs[1:]:
            content_Phi_f = S.gcd(content_Phi_f, a)
        neg_Q = not is_assoc(S, content_Phi_f, S.convert(phi(c_R)))
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, neg_Q]

CONDITION_LABELS = [
    "H_1: R and S are Unique Factorization Domains",
    "H_2: phi is a ring isomorphism",
    "H_3: Phi is the polynomial ring isomorphism induced by phi",
    "H_4: c is the content of f",
    "¬Q: The content of Phi(f) is not associate to phi(c) in S"
]

N_HYP = 4
NEG_Q_INDEX = 4