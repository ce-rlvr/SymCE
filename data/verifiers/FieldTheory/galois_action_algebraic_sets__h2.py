import sympy
from sympy import Poly, Symbol, factor_list, RootOf, Rational, Integer

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with:
      - 'minpoly': A sympy expression in `x` defining the finite extension L = Q[x]/(minpoly).
      - 'V_points': A list of points (each point is a list of coordinates, which are expressions in `x`)
                    defining the algebraic set V in L^n.
    """
    try:
        minpoly = witness['minpoly']
        raw_V_points = witness['V_points']
        # Remove duplicates to treat V as a set
        V_points = []
        for v in raw_V_points:
            if v not in V_points:
                V_points.append(v)
    except Exception:
        return [False, False]

    # H_1: L/K is a finite Galois extension
    # We fix K = Q. L/Q is Galois iff minpoly is irreducible and splits completely in L.
    h1 = False
    try:
        poly_min = Poly(minpoly, x, domain='QQ')
        if poly_min.is_irreducible and poly_min.degree() > 0:
            a = RootOf(minpoly, 0)
            coeff, factors = factor_list(minpoly, extension=a)
            is_galois = True
            for fac, mult in factors:
                if Poly(fac, x).degree() != 1:
                    is_galois = False
                    break
            if is_galois:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: The conclusion fails.
    # The conclusion is that G acts on V, and V^G == V \cap K^n.
    # If G acts on V, V^G == V \cap K^n is a tautology. Thus, the conclusion fails iff G does NOT act on V.
    # G acts on V iff the set of complex embeddings of V is independent of the chosen root of minpoly.
    neg_q = False
    try:
        if h1:
            # Find all complex roots of the minimal polynomial
            roots = [RootOf(minpoly, i).evalf(50) for i in range(poly_min.degree())]
            
            # Evaluate the points of V at each complex root
            V_evals = []
            for r in roots:
                V_r = []
                for v in V_points:
                    v_eval = []
                    for coord in v:
                        coord_expr = sympy.sympify(coord)
                        val = coord_expr.subs(x, r).evalf(50)
                        v_eval.append(complex(val))
                    V_r.append(v_eval)
                V_evals.append(V_r)
            
            # Check if the evaluated sets of points are identical for all roots
            g_acts = True
            for i in range(1, len(V_evals)):
                V1 = V_evals[0]
                V2 = V_evals[i]
                if len(V1) != len(V2):
                    g_acts = False
                    break
                
                matched = [False] * len(V2)
                for pt1 in V1:
                    found = False
                    for j, pt2 in enumerate(V2):
                        if matched[j]: 
                            continue
                        match_pt = True
                        for c1, c2 in zip(pt1, pt2):
                            if abs(c1 - c2) > 1e-10:
                                match_pt = False
                                break
                        if match_pt:
                            matched[j] = True
                            found = True
                            break
                    if not found:
                        g_acts = False
                        break
                if not g_acts:
                    break
            
            neg_q = not g_acts
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "¬Q: G does not act on V (or V^G != V \\cap K^n)"
]

N_HYP = 1
NEG_Q_INDEX = 1