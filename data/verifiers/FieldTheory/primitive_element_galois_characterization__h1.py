import sympy
from sympy import Poly, factor, RootOf, Mul, Pow, sympify, minpoly
from sympy.abc import x, y
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def count_roots_in_extension(f_expr):
    """
    Counts the number of roots of f_expr in the field Q[x]/(f_expr).
    This is exactly the size of the automorphism group Aut(L/Q).
    """
    r = RootOf(f_expr, 0)
    f_y = f_expr.subs(x, y)
    factored = factor(f_y, extension=r)
    
    if isinstance(factored, Mul):
        factors = factored.args
    else:
        factors = [factored]
        
    count = 0
    for f in factors:
        if f.has(y):
            base = f.base if isinstance(f, Pow) else f
            exp = f.exp if isinstance(f, Pow) else 1
            if Poly(base, y).degree() == 1:
                count += exp
    return count

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple: (f_expr, G_exprs, alpha_expr)
    where:
      - f_expr is a SymPy expression in x representing the minimal polynomial of L/Q.
      - G_exprs is a list of SymPy expressions in x representing the automorphisms in G.
      - alpha_expr is a SymPy expression in x representing alpha in L.
    """
    try:
        f_expr, G_exprs, alpha_expr = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is the Galois group of L/K (where K = Q and L = Q[x]/(f_expr))
    try:
        poly_f = Poly(f_expr, x, domain='QQ')
        if not poly_f.is_irreducible:
            h1_ok = False
        else:
            expected_len = count_roots_in_extension(f_expr)
            if len(G_exprs) != expected_len:
                h1_ok = False
            else:
                h1_ok = True
                seen = []
                for g in G_exprs:
                    g = sympify(g)
                    g_sub = f_expr.subs(x, g).expand()
                    # Check if g is a valid automorphism (root of f_expr)
                    if not Poly(g_sub, x, domain='QQ').rem(poly_f).is_zero:
                        h1_ok = False
                        break
                    # Check that all provided automorphisms are distinct
                    g_rem = Poly(g.expand(), x, domain='QQ').rem(poly_f).as_expr()
                    if g_rem in seen:
                        h1_ok = False
                        break
                    seen.append(g_rem)
    except Exception:
        h1_ok = False

    # H_2: alpha is an element of L
    try:
        alpha_expr = sympify(alpha_expr)
        # Any polynomial in x with rational coefficients represents an element in Q[x]/(f_expr)
        poly_alpha = Poly(alpha_expr, x, domain='QQ')
        h2_ok = True
    except Exception:
        h2_ok = False

    # Negated Conclusion: L = K(alpha) iff stabilizer of alpha in G is trivial
    try:
        # Check if L = K(alpha)
        alpha_val = alpha_expr.subs(x, RootOf(f_expr, 0))
        mp = minpoly(alpha_val)
        deg_alpha = Poly(mp).degree()
        deg_L = poly_f.degree()
        
        L_equals_K_alpha = (deg_alpha == deg_L)
        
        # Find the stabilizer of alpha in G
        stabilizer = []
        for g in G_exprs:
            g = sympify(g)
            diff = (alpha_expr.subs(x, g) - alpha_expr).expand()
            if Poly(diff, x, domain='QQ').rem(poly_f).is_zero:
                stabilizer.append(g)
                
        # Check if the stabilizer contains ONLY the identity element
        is_stabilizer_trivial = True
        for g in stabilizer:
            diff_id = (g - x).expand()
            if not Poly(diff_id, x, domain='QQ').rem(poly_f).is_zero:
                is_stabilizer_trivial = False
                break
                
        # The conclusion states: L == K(alpha) iff stabilizer is trivial
        # We want the negation of the conclusion to be True
        Q_holds = (L_equals_K_alpha == is_stabilizer_trivial)
        neg_Q_ok = not Q_holds
    except Exception:
        neg_Q_ok = False

    return [h1_ok, h2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: G is the Galois group of L/K",
    "H_2: alpha is an element of L",
    "¬Q: The equivalence (L = K(alpha) iff stabilizer of alpha is trivial) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2