import sympy as sp

S3 = sp.combinatorics.named_groups.SymmetricGroup(3)
S4 = sp.combinatorics.named_groups.SymmetricGroup(4)
A4 = sp.combinatorics.named_groups.AlternatingGroup(4)
D4 = sp.combinatorics.named_groups.DihedralGroup(4)
C4 = sp.combinatorics.named_groups.CyclicGroup(4)
V4 = sp.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sp.combinatorics.named_groups.CyclicGroup(2)
Z3 = sp.combinatorics.named_groups.CyclicGroup(3)
Z4 = sp.combinatorics.named_groups.CyclicGroup(4)
Z6 = sp.combinatorics.named_groups.CyclicGroup(6)
trivial = sp.combinatorics.named_groups.CyclicGroup(1)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the necessary structure to evaluate the hypotheses
    and the negated conclusion. It can be a tuple (F, K, alpha, m) or a custom object
    that implements the required evaluation methods.
    """
    h1_ok = False
    h2_ok = False
    h3_ok = False
    neg_q_ok = False

    try:
        # If the witness is a custom object that encapsulates the algebraic structures
        if hasattr(witness, 'check_H1'):
            h1_val = witness.check_H1
            h1_ok = bool(h1_val() if callable(h1_val) else h1_val)
            
            h2_val = witness.check_H2
            h2_ok = bool(h2_val() if callable(h2_val) else h2_val)
            
            h3_val = witness.check_H3
            h3_ok = bool(h3_val() if callable(h3_val) else h3_val)
            
            neg_q_val = witness.check_neg_Q
            neg_q_ok = bool(neg_q_val() if callable(neg_q_val) else neg_q_val)
            
            return [h1_ok, h2_ok, h3_ok, neg_q_ok]
            
        elif hasattr(witness, 'H1'):
            h1_val = witness.H1
            h1_ok = bool(h1_val() if callable(h1_val) else h1_val)
            
            h2_val = witness.H2
            h2_ok = bool(h2_val() if callable(h2_val) else h2_val)
            
            h3_val = witness.H3
            h3_ok = bool(h3_val() if callable(h3_val) else h3_val)
            
            neg_q_val = getattr(witness, 'neg_Q', getattr(witness, 'neg_q', False))
            neg_q_ok = bool(neg_q_val() if callable(neg_q_val) else neg_q_val)
            
            return [h1_ok, h2_ok, h3_ok, neg_q_ok]
        
        # Standard tuple unpacking for SymPy domains
        if isinstance(witness, tuple) and len(witness) == 4:
            F, K, alpha, m = witness
            
            # H1: K is an extension field of F
            try:
                h1_ok = True
                if hasattr(F, 'is_subset') and hasattr(K, 'is_Field'):
                    h1_ok = bool(F.is_subset(K))
            except Exception:
                h1_ok = False

            # H2: alpha is an element of K that is algebraic over F
            try:
                in_K = True
                if hasattr(K, '__contains__'):
                    in_K = alpha in K
                
                is_alg = False
                try:
                    mp = sp.minpoly(alpha, domain=F)
                    is_alg = (mp is not None)
                except Exception:
                    pass
                
                if not is_alg:
                    x = sp.Symbol('x')
                    m_expr = m.as_expr() if hasattr(m, 'as_expr') else m
                    free_vars = m_expr.free_symbols
                    if free_vars:
                        x = list(free_vars)[0]
                    m_val = m_expr.subs(x, alpha)
                    if hasattr(m_val, 'expand'):
                        m_val = m_val.expand()
                    if m_val == 0:
                        is_alg = True

                h2_ok = bool(in_K and is_alg)
            except Exception:
                h2_ok = False

            # H3: m(x) in F[x] is the monic polynomial of least positive degree such that m(alpha) = 0
            try:
                x = sp.Symbol('x')
                m_expr = m.as_expr() if hasattr(m, 'as_expr') else m
                free_vars = m_expr.free_symbols
                if free_vars:
                    x = list(free_vars)[0]
                
                m_poly = sp.Poly(m_expr, x)
                m_monic = (m_poly.LC() == 1)
                m_deg = m_poly.degree()
                m_deg_pos = (m_deg > 0)
                
                m_val = m_expr.subs(x, alpha)
                if hasattr(m_val, 'expand'):
                    m_val = m_val.expand()
                is_root = (m_val == 0)
                
                coeffs_in_F = True
                if hasattr(F, '__contains__'):
                    for c in m_poly.coeffs():
                        if c not in F:
                            coeffs_in_F = False
                            
                is_least_deg = True
                try:
                    mp = sp.minpoly(alpha, x, domain=F)
                    mp_poly = sp.Poly(mp, x)
                    if m_deg > mp_poly.degree():
                        is_least_deg = False
                except Exception:
                    pass
                        
                h3_ok = bool(m_monic and m_deg_pos and coeffs_in_F and is_least_deg and is_root)
            except Exception:
                h3_ok = False

            # ¬Q: m(x) is NOT irreducible in F[x]
            try:
                x = sp.Symbol('x')
                m_expr = m.as_expr() if hasattr(m, 'as_expr') else m
                free_vars = m_expr.free_symbols
                if free_vars:
                    x = list(free_vars)[0]
                
                domain_str = None
                if F == sp.S.Complexes:
                    domain_str = 'CC'
                elif F == sp.S.Reals:
                    domain_str = 'RR'
                elif F == sp.S.Rationals:
                    domain_str = 'QQ'
                elif F == sp.S.Integers:
                    domain_str = 'ZZ'
                    
                if domain_str == 'CC':
                    m_poly = sp.Poly(m_expr, x)
                    neg_q_ok = (m_poly.degree() > 1)
                else:
                    if domain_str:
                        m_poly_check = sp.Poly(m_expr, x, domain=domain_str)
                    else:
                        m_poly_check = sp.Poly(m_expr, x)
                        
                    neg_q_ok = not bool(m_poly_check.is_irreducible)
            except Exception:
                neg_q_ok = False

    except Exception:
        pass

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an extension field of F",
    "H_2: alpha is an element of K that is algebraic over F",
    "H_3: m(x) is the monic polynomial over F of least positive degree with m(alpha) = 0",
    "¬Q: m(x) is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3