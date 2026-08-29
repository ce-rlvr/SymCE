import sympy
from sympy import Poly, QQ
from sympy.abc import x

def is_splitting_field(E, f, F):
    try:
        if not getattr(E, 'is_Field', False): 
            return False
        
        f_E = Poly(f.as_expr(), *f.gens, domain=E)
        roots = f_E.ground_roots()
        if sum(roots.values()) != f.degree(): 
            return False
        
        if hasattr(E, 'mod') or E == QQ:
            expr_roots = list(roots.keys())
            F_exprs = []
            if hasattr(F, 'gen'):
                F_exprs.append(F.to_sympy(F.gen))
            expected_E = QQ.algebraic_field(*(F_exprs + expr_roots))
            return E == expected_E
            
        if hasattr(E, 'order') and hasattr(F, 'order'):
            if E.characteristic != F.characteristic: 
                return False
            return True
            
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        F = witness['F']
        F_prime = witness['F_prime']
        h1 = bool(getattr(F, 'is_Field', False) and getattr(F_prime, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        f = witness['f']
        F = witness['F']
        h2 = bool(isinstance(f, Poly) and f.domain == F)
    except Exception:
        h2 = False

    try:
        f = witness['f']
        f_prime = witness['f_prime']
        F_prime = witness['F_prime']
        phi = witness['phi']
        
        if isinstance(f_prime, Poly) and f_prime.domain == F_prime:
            expected_coeffs = [phi(c) for c in f.all_coeffs()]
            actual_coeffs = f_prime.all_coeffs()
            h3 = bool((len(expected_coeffs) == len(actual_coeffs)) and all(e == a for e, a in zip(expected_coeffs, actual_coeffs)))
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        E = witness['E']
        f = witness['f']
        F = witness['F']
        h4 = bool(is_splitting_field(E, f, F))
    except Exception:
        h4 = False

    try:
        E_prime = witness['E_prime']
        f_prime = witness['f_prime']
        F_prime = witness['F_prime']
        h5 = bool(is_splitting_field(E_prime, f_prime, F_prime))
    except Exception:
        h5 = False

    try:
        E = witness['E']
        E_prime = witness['E_prime']
        
        neg_q = False
        if (hasattr(E, 'mod') or E == QQ) and (hasattr(E_prime, 'mod') or E_prime == QQ):
            deg_E = E.mod.degree() if hasattr(E, 'mod') else 1
            deg_E_prime = E_prime.mod.degree() if hasattr(E_prime, 'mod') else 1
            
            if deg_E != deg_E_prime:
                neg_q = True
            else:
                if deg_E > 1:
                    mod_E = E.mod
                    mod_E_prime = Poly(mod_E.as_expr(), *mod_E.gens, domain=E_prime)
                    roots = mod_E_prime.ground_roots()
                    if not roots:
                        neg_q = True
        elif hasattr(E, 'order') and hasattr(E_prime, 'order'):
            if E.order != E_prime.order:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: F and F_prime are fields",
    "H_2: f(x) is a polynomial over F",
    "H_3: f_prime(x) is the polynomial over F_prime whose coefficients are the images of the coefficients of f(x) under phi",
    "H_4: E is a splitting field of f(x) over F",
    "H_5: E_prime is a splitting field of f_prime(x) over F_prime",
    "¬Q: There does not exist a field isomorphism tau from E onto E_prime extending phi"
]

N_HYP = 5
NEG_Q_INDEX = 5