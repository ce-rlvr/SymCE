import sympy
import math

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    "If F_q is a finite field, f(x) has degree n >= 1, and gcd(n, m) = 1, 
    then f(x) is irreducible over F_{q^m}."
    (The dropped hypothesis was that f(x) is irreducible over F_q).
    
    Witness can be either (q, m, f) or (q, n, m, f).
    """
    try:
        if len(witness) == 3:
            q, m, f = witness
            n_wit = None
        elif len(witness) == 4:
            q, n_wit, m, f = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: F_q is a finite field with q elements
    h1 = False
    p = 1
    k = 1
    try:
        if hasattr(q, 'is_integer') and q.is_integer and q > 1:
            q_val = int(q)
        elif isinstance(q, int) and q > 1:
            q_val = q
        else:
            q_val = None
            
        if q_val is not None:
            factors = sympy.ntheory.factorint(q_val)
            if len(factors) == 1:
                p, k = list(factors.items())[0]
                h1 = True
    except Exception:
        pass

    # H2: The degree of f(x) is n >= 1
    h2 = False
    n = -1
    try:
        if n_wit is not None:
            if hasattr(n_wit, 'is_integer') and n_wit.is_integer:
                n_wit_val = int(n_wit)
            elif isinstance(n_wit, int):
                n_wit_val = n_wit
            else:
                n_wit_val = -1
        else:
            n_wit_val = None

        if isinstance(f, str):
            f = sympy.sympify(f)
        poly_f = sympy.Poly(f, x)
        
        # Allow polynomials over ZZ or the prime subfield GF(p)
        valid_domain = False
        if poly_f.domain == sympy.ZZ:
            valid_domain = True
        elif poly_f.domain.is_FiniteField and poly_f.domain.characteristic == p:
            valid_domain = True
            
        if valid_domain:
            coeffs = [int(c) % p for c in poly_f.all_coeffs()]
            deg = -1
            for i, c in enumerate(coeffs):
                if c != 0:
                    deg = len(coeffs) - 1 - i
                    break
            if deg >= 1:
                n = deg
                if n_wit_val is None or n == n_wit_val:
                    h2 = True
    except Exception:
        pass

    # H3: m >= 1 is an integer such that gcd(n, m) == 1
    h3 = False
    m_val = None
    try:
        if hasattr(m, 'is_integer') and m.is_integer:
            m_val = int(m)
        elif isinstance(m, int):
            m_val = m
            
        if m_val is not None and m_val >= 1 and math.gcd(n, m_val) == 1:
            h3 = True
    except Exception:
        pass

    # neg_Q: f(x) is NOT irreducible over F_{q^m}
    neg_q = False
    try:
        if h1 and h2 and m_val is not None and m_val >= 1:
            poly_f = sympy.Poly(f, x)
            coeffs = [int(c) % p for c in poly_f.all_coeffs()]
            for i, c in enumerate(coeffs):
                if c != 0:
                    deg = len(coeffs) - 1 - i
                    lc = c
                    start_idx = i
                    break
            
            # Make the polynomial monic over F_p for the irreducibility test
            inv_lc = sympy.mod_inverse(lc, p)
            monic_coeffs = [(c * inv_lc) % p for c in coeffs[start_idx:]]
            monic_f = sympy.Poly.from_list(monic_coeffs, gens=x)
            
            is_irred = sympy.polys.polytools.is_irreducible(monic_f, modulus=p)
            
            # A polynomial in F_p[x] is irreducible over F_{p^{k*m}} iff 
            # it is irreducible over F_p and gcd(deg(f), k*m) == 1.
            is_irred_qm = is_irred and (math.gcd(n, k * m_val) == 1)
            neg_q = not is_irred_qm
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: The degree of f(x) is n >= 1",
    "H_3: m >= 1 is an integer such that gcd(n, m) == 1",
    "¬Q: f(x) is NOT irreducible over the extension field F_{q^m}"
]

N_HYP = 3
NEG_Q_INDEX = 3