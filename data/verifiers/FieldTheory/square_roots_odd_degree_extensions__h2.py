import sympy as sp

x, y = sp.symbols('x y')

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the false conjecture.
    The witness should be a tuple: (min_poly, a)
    where:
      - min_poly is a SymPy expression representing the minimal polynomial of L over K=QQ.
      - a is a rational number in K=QQ.
    """
    try:
        min_poly, a = witness
    except Exception:
        return [False, False, False]
    
    # H_1: L is a finite field extension of K
    # We interpret K = QQ, and L = QQ[x]/(min_poly)
    try:
        poly = sp.Poly(min_poly, domain='QQ')
        h1 = bool(poly.is_irreducible and poly.degree() >= 1)
    except Exception:
        h1 = False

    # H_2: a \in K is an element such that x^2 - a has no root in K
    try:
        a_val = sp.Rational(a)
        root_a = sp.sqrt(a_val)
        # x^2 - a has no root in QQ iff a is not a perfect square in QQ
        h2 = bool(not root_a.is_rational)
    except Exception:
        h2 = False

    # ¬Q: The polynomial x^2 - a HAS a root in L
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            alpha = sp.RootOf(poly, 0)
            Y = sp.Symbol('Y')
            # Factor Y^2 - a over the extension field L = QQ(alpha)
            factored = sp.factor(Y**2 - a_val, extension=alpha)
            
            has_linear_factor = False
            if factored.is_Mul:
                for arg in factored.args:
                    if arg.has(Y) and sp.degree(arg, Y) == 1:
                        has_linear_factor = True
                        break
            elif factored.is_Pow:
                base, exp = factored.args
                if base.has(Y) and sp.degree(base, Y) == 1:
                    has_linear_factor = True
            elif sp.degree(factored, Y) == 1:
                has_linear_factor = True
                
            neg_q = bool(has_linear_factor)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L is a finite field extension of K",
    "H_2: a in K such that x^2 - a has no root in K",
    "¬Q: x^2 - a has a root in L"
]

N_HYP = 2
NEG_Q_INDEX = 2