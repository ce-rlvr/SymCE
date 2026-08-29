import sympy as sp
from sympy import Poly

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x')

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: E/F is a finite normal extension",
    "H_2: E/F is a separable extension",
    "¬Q: The trace condition is not equivalent to the existence of beta"
]

def conditions(witness):
    """
    Given a witness, checks whether it is a valid counterexample.
    The witness should be a tuple: (P_expr, G_exprs, sigma_expr, alpha_expr)
    where:
      - P_expr is the minimal polynomial of the extension E = Q(theta) over F = Q.
      - G_exprs is a list of polynomials representing the Galois group elements (automorphisms).
      - sigma_expr is a polynomial representing the automorphism sigma in G.
      - alpha_expr is a polynomial representing the element alpha in E.
    """
    try:
        P_expr, G_exprs, sigma_expr, alpha_expr = witness
    except Exception:
        return [False, False, False]
        
    # H_1: E/F is a finite normal extension
    try:
        P = Poly(P_expr, x, domain='QQ')
        if not P.is_irreducible:
            h1 = False
        else:
            n = P.degree()
            if len(G_exprs) != n:
                h1 = False
            else:
                h1 = True
                # Check if each g in G is a root of P (i.e., P(g(x)) == 0 mod P(x))
                for g in G_exprs:
                    g_poly = Poly(g, x, domain='QQ')
                    comp = P.compose(g_poly)
                    _, rem = comp.div(P)
                    if not rem.is_zero:
                        h1 = False
                        break
                
                # Check if all automorphisms are distinct modulo P
                if h1:
                    rem_G = []
                    for g in G_exprs:
                        _, r = Poly(g, x, domain='QQ').div(P)
                        rem_G.append(r.as_expr())
                    if len(set(rem_G)) != n:
                        h1 = False
                
                # Ensure sigma is actually one of the automorphisms in G
                if h1:
                    sigma_rem = Poly(sigma_expr, x, domain='QQ').div(P)[1].as_expr()
                    if sigma_rem not in set(rem_G):
                        h1 = False
    except Exception:
        h1 = False

    # H_2: E/F is a separable extension
    # Over Q, any irreducible polynomial is separable.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    # Conclusion: Tr(alpha) == 0 iff there exists beta such that alpha = beta - sigma(beta)
    try:
        alpha_poly = Poly(alpha_expr, x, domain='QQ')
        trace_poly = Poly(0, x, domain='QQ')
        
        # Compute Tr(alpha) = sum(g(alpha) for g in G)
        for g in G_exprs:
            g_poly = Poly(g, x, domain='QQ')
            comp = alpha_poly.compose(g_poly)
            _, r = comp.div(P)
            trace_poly = trace_poly.add(r)
        
        _, trace_rem = trace_poly.div(P)
        is_trace_zero = bool(trace_rem.is_zero)

        # Check if there exists beta such that alpha = beta - sigma(beta)
        # We construct the matrix for the linear transformation T(beta) = beta - sigma(beta)
        n = P.degree()
        sigma_poly = Poly(sigma_expr, x, domain='QQ')
        
        T_matrix = []
        for i in range(n):
            beta_poly = Poly(x**i, x, domain='QQ')
            comp = beta_poly.compose(sigma_poly)
            _, r = comp.div(P)
            t_poly = beta_poly.sub(r)
            
            coeffs = t_poly.all_coeffs()
            coeffs = [0] * (n - len(coeffs)) + coeffs
            coeffs.reverse()
            T_matrix.append(coeffs)
        
        # M is the matrix of T in the basis 1, x, ..., x^{n-1}
        M = sp.Matrix(T_matrix).T
        
        # Coordinate vector for alpha
        _, alpha_rem = alpha_poly.div(P)
        alpha_coeffs = alpha_rem.all_coeffs()
        alpha_coeffs = [0] * (n - len(alpha_coeffs)) + alpha_coeffs
        alpha_coeffs.reverse()
        v_alpha = sp.Matrix(alpha_coeffs)
        
        # beta exists iff v_alpha is in the column space of M
        M_aug = M.row_join(v_alpha)
        exists_beta = bool(M.rank() == M_aug.rank())
        
        # The conclusion fails if the two conditions are not equivalent
        neg_q = bool(is_trace_zero != exists_beta)
        
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]