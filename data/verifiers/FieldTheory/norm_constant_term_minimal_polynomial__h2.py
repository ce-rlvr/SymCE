import sympy

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple (f, g, m) where:
      - f is an irreducible polynomial in x over QQ defining the field extension E = QQ[x]/(f(x))
      - g is a polynomial in x representing the element alpha in E
      - m is the minimal polynomial of alpha over QQ
    """
    try:
        f, g, m = witness
        
        # H1: F is a field (we use F = QQ, which is a field).
        # We also verify that E is a valid field extension of F by checking if f is irreducible.
        f_poly = sympy.Poly(f, x, domain='QQ')
        h1 = bool(f_poly.is_irreducible and f_poly.degree() > 0)
        
        # H2: m(x) is the minimal polynomial of alpha over F
        m_poly = sympy.Poly(m, x, domain='QQ')
        is_monic = (m_poly.LC() == 1)
        is_irred = m_poly.is_irreducible
        
        m_expr = sympy.sympify(m)
        g_expr = sympy.sympify(g)
        f_expr = sympy.sympify(f)
        
        # Check if m(alpha) = 0 in E
        m_g = m_expr.subs(x, g_expr)
        rem = sympy.rem(m_g, f_expr, x)
        is_root = (sympy.simplify(rem) == 0)
        
        h2 = bool(is_monic and is_irred and is_root)
        
        # Conclusion: N_{E/F}(alpha) == (-1)^d * a_0
        d = m_poly.degree()
        a_0 = m_poly.nth(0)
        
        # Compute the field norm N_{E/F}(alpha) as the determinant of the multiplication map
        n = f_poly.degree()
        M = sympy.zeros(n, n)
        for i in range(n):
            prod = sympy.rem(x**i * g_expr, f_expr, x)
            prod_poly = sympy.Poly(prod, x, domain='QQ')
            coeffs = prod_poly.all_coeffs()
            # Pad with zeros to match the degree n
            coeffs = [0] * (n - len(coeffs)) + coeffs
            # Reverse to align with the basis 1, x, ..., x^{n-1}
            coeffs = coeffs[::-1]
            for j in range(n):
                M[j, i] = coeffs[j]
                
        norm_val = M.det()
        expected = ((-1)**d) * a_0
        
        q = (norm_val == expected)
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: m(x) is the minimal polynomial of alpha over F",
    "¬Q: The field norm N_{E/F}(alpha) is not equal to (-1)^d a_0"
]

N_HYP = 2
NEG_Q_INDEX = 2