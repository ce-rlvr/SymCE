import sympy
from sympy import Poly, Symbol
from sympy.polys.domains import QQ, ZZ
from sympy.abc import x

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys:
    'F', 'F_prime', 'phi', 'f', 'f_prime', 'E', 'E_prime'
    """
    # H_1: F and F_prime are fields
    try:
        F = witness['F']
        F_prime = witness['F_prime']
        h1 = F.is_Field and F_prime.is_Field
    except Exception:
        h1 = False

    # H_2: phi is a field isomorphism from F onto F_prime
    try:
        phi = witness['phi']
        h2 = callable(phi)
        if h2:
            if phi(F.zero) != F_prime.zero or phi(F.one) != F_prime.one:
                h2 = False
    except Exception:
        h2 = False

    # H_3: f is a polynomial over F
    try:
        f = witness['f']
        h3 = isinstance(f, Poly) and f.domain == F
    except Exception:
        h3 = False

    # H_4: f_prime is the polynomial over F_prime whose coefficients are the images of the coefficients of f under phi
    try:
        f_prime = witness['f_prime']
        h4 = isinstance(f_prime, Poly) and f_prime.domain == F_prime
        if h4:
            coeffs_f = f.all_coeffs()
            coeffs_f_prime = f_prime.all_coeffs()
            if len(coeffs_f) != len(coeffs_f_prime):
                h4 = False
            else:
                for c, c_prime in zip(coeffs_f, coeffs_f_prime):
                    if phi(c) != c_prime:
                        h4 = False
                        break
    except Exception:
        h4 = False

    # H_5: E_prime is a splitting field of f_prime over F_prime
    try:
        E_prime = witness['E_prime']
        h5 = E_prime.is_Field
        if h5 and f_prime.degree() < 1:
            h5 = False
    except Exception:
        h5 = False

    # neg_Q: There does NOT exist a field isomorphism tau from E onto E_prime extending phi
    try:
        E = witness['E']
        E_prime = witness['E_prime']
        
        def field_invariant(K):
            if K == QQ:
                return 1
            if hasattr(K, 'exts'):
                return tuple(K.exts)
            if hasattr(K, 'mod'):
                return K.mod
            return str(K)
        
        # If the invariants are different, they are likely not isomorphic
        neg_q = field_invariant(E) != field_invariant(E_prime)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F and F_prime are fields",
    "H_2: phi is a field isomorphism from F onto F_prime",
    "H_3: f is a polynomial over F",
    "H_4: f_prime is the polynomial over F_prime whose coefficients are the images of the coefficients of f under phi",
    "H_5: E_prime is a splitting field of f_prime over F_prime",
    "not_Q: There does not exist a field isomorphism tau from E onto E_prime extending phi"
]

N_HYP = 5
NEG_Q_INDEX = 5