import sympy
from sympy import QQ, Poly, minpoly, Rational, Integer, sqrt, cbrt, I, pi, E, symbols, Symbol
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the conjecture.
    The witness should be a tuple: (K_gens, E_gens, L_gens, alpha, m_E)
    where:
      - K_gens: list of generators for field K over QQ
      - E_gens: list of generators for field E over QQ
      - L_gens: list of generators for field L over QQ
      - alpha: an element of L
      - m_E: the minimal polynomial of alpha over E (as a SymPy expression)
    """
    if not isinstance(witness, (list, tuple)) or len(witness) != 5:
        return [False, False, False, False]
        
    K_gens, E_gens, L_gens, alpha, m_E = witness

    try:
        K_field = QQ.algebraic_field(*K_gens) if K_gens else QQ
    except Exception:
        K_field = None

    try:
        E_field = QQ.algebraic_field(*E_gens) if E_gens else QQ
    except Exception:
        E_field = None

    try:
        L_field = QQ.algebraic_field(*L_gens) if L_gens else QQ
    except Exception:
        L_field = None

    def is_in_field(elem, field):
        if field is None: 
            return False
        try:
            field.from_sympy(sympy.simplify(elem))
            return True
        except Exception:
            try:
                p = minpoly(elem, x, domain=field)
                return p.degree() == 1
            except Exception:
                return False

    # H1: E is an intermediate field such that K <= E <= L
    try:
        k_in_e = all(is_in_field(k, E_field) for k in K_gens)
        e_in_l = all(is_in_field(e, L_field) for e in E_gens)
        h1 = bool(k_in_e and e_in_l)
    except Exception:
        h1 = False

    # H2: alpha is an element of L
    try:
        h2 = bool(is_in_field(alpha, L_field))
    except Exception:
        h2 = False

    # H3: m_E(x) is the minimal polynomial of alpha over E
    try:
        free_syms = m_E.free_symbols
        var = list(free_syms)[0] if len(free_syms) == 1 else x
        m_E_poly = Poly(m_E, var)
        
        is_monic = m_E_poly.LC() == 1
        coeffs_in_E = all(is_in_field(c, E_field) for c in m_E_poly.coeffs())
        
        val = m_E_poly.as_expr().subs(var, alpha)
        val_simp = sympy.simplify(val)
        try:
            is_root = (val_simp == 0) or (minpoly(val_simp, var) == var)
        except Exception:
            is_root = (val_simp == 0)
            
        m_E_E = Poly(m_E_poly.as_expr(), var, domain=E_field)
        factors = m_E_E.factor_list()[1]
        is_irreducible = len(factors) == 1 and factors[0][1] == 1
        
        h3 = bool(is_monic and coeffs_in_E and is_root and is_irreducible)
    except Exception:
        h3 = False

    # Negated Conclusion: The splitting field of m_E(x) over E is NOT a subfield of L
    # This is equivalent to saying m_E(x) does not split completely in L.
    try:
        free_syms = m_E.free_symbols
        var = list(free_syms)[0] if len(free_syms) == 1 else x
        m_E_poly = Poly(m_E, var)
        
        m_E_L = Poly(m_E_poly.as_expr(), var, domain=L_field)
        factors_L = m_E_L.factor_list()[1]
        splits_completely = all(f.degree() == 1 for f, mult in factors_L)
        neg_q = not splits_completely
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E is an intermediate field such that K <= E <= L",
    "H_2: alpha is an element of L",
    "H_3: m_E(x) is the minimal polynomial of alpha over E",
    "¬Q: The splitting field of m_E(x) over E is NOT a subfield of L"
]

N_HYP = 3
NEG_Q_INDEX = 3