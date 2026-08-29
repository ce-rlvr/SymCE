import sympy
from sympy import ZZ, QQ, symbols

x, y, z = symbols('x y z')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            phi = witness['phi']
            f_coeffs = witness['f_coeffs']
            c = witness['c']
        else:
            R, S, phi, f_coeffs, c = witness

        if hasattr(f_coeffs, 'all_coeffs'):
            f_coeffs = f_coeffs.all_coeffs()
        elif hasattr(f_coeffs, 'coeffs'):
            f_coeffs = f_coeffs.coeffs()
        else:
            f_coeffs = list(f_coeffs)
    except Exception:
        return [False] * 5

    def divides(dom, a, b):
        if a == dom.zero:
            return b == dom.zero
        try:
            q = dom.exquo(b, a)
            return q is not None
        except Exception:
            return False

    def is_associate(dom, a, b):
        return divides(dom, a, b) and divides(dom, b, a)

    try:
        h1 = bool(R.is_UFD and S.is_UFD)
    except Exception:
        h1 = False

    try:
        h2 = True
        test_elements = []
        for elem in list(f_coeffs) + [c, R.one, R.zero]:
            if elem not in test_elements:
                test_elements.append(elem)
                
        for a in test_elements:
            for b in test_elements:
                if phi(R.add(a, b)) != S.add(phi(a), phi(b)):
                    h2 = False
                if phi(R.mul(a, b)) != S.mul(phi(a), phi(b)):
                    h2 = False
        if phi(R.one) != S.one:
            h2 = False
        if phi(R.zero) != S.zero:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = any(coef != R.zero for coef in f_coeffs)
    except Exception:
        h3 = False

    try:
        if not f_coeffs:
            h4 = False
        else:
            actual_c = f_coeffs[0]
            for coef in f_coeffs[1:]:
                actual_c = R.gcd(actual_c, coef)
            h4 = is_associate(R, c, actual_c)
    except Exception:
        h4 = False

    try:
        if not f_coeffs:
            neg_q = False
        else:
            Phi_f_coeffs = [phi(coef) for coef in f_coeffs]
            Phi_c = Phi_f_coeffs[0]
            for coef in Phi_f_coeffs[1:]:
                Phi_c = S.gcd(Phi_c, coef)
            phi_c = phi(c)
            neg_q = not is_associate(S, Phi_c, phi_c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = ["H_1: R and S are Unique Factorization Domains", "H_2: phi is a ring isomorphism", "H_3: f is a non-zero polynomial", "H_4: c is the content of f", "¬Q: The content of Phi(f) is not associate to phi(c)"]

N_HYP = 4
NEG_Q_INDEX = 4