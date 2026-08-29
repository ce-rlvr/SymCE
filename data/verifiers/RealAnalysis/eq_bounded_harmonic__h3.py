import sympy
from sympy import Symbol, Interval, S
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = sympy.symbols('x y z', real=True)
k = sympy.Symbol('k', integer=True, positive=True)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary containing:
      - "vars": list of variables, e.g., [x] or [x, y]
      - "Omega": open set (SymPy set)
      - "K": compact subset of Omega (SymPy set)
      - "F": family of harmonic functions parameterized by k (SymPy expression)
      - "k": the parameter symbol (optional, defaults to top-level k)
    """
    try:
        vars_list = witness.get("vars", [x])
        Omega = witness.get("Omega")
        K = witness.get("K")
        F = witness.get("F")
        k_sym = witness.get("k", k)
    except Exception:
        return [False, False, False, False]

    # H1: \Omega is an open subset of \mathbb{R}^n.
    try:
        if isinstance(Omega, sympy.sets.sets.ProductSet):
            h1 = bool(all(s.is_open == True for s in Omega.sets))
        else:
            h1 = bool(Omega.is_open == True)
    except Exception:
        h1 = False

    # H2: \mathcal{F} is a family of harmonic functions on \Omega.
    try:
        laplacian = sum(sympy.diff(F, v, 2) for v in vars_list)
        lap_simp = sympy.simplify(laplacian)
        h2 = bool(lap_simp == 0 or lap_simp.is_zero)
    except Exception:
        h2 = False

    # H3: K is a compact subset of \Omega.
    try:
        if isinstance(K, sympy.sets.sets.ProductSet):
            is_compact = all(s.is_closed == True and s.is_bounded == True for s in K.sets)
        else:
            is_compact = (K.is_closed == True) and (K.is_bounded == True)
        is_subset = (K.is_subset(Omega) == True)
        h3 = bool(is_compact and is_subset)
    except Exception:
        h3 = False

    # ¬Q: The family \mathcal{F} is NOT uniformly equicontinuous on K.
    # We verify this by checking if the gradient of F with respect to the spatial variables
    # grows unbounded on K as the parameter k -> infinity.
    try:
        grad_norms = [sympy.diff(F, v) for v in vars_list]
        corners = []
        if isinstance(K, sympy.sets.sets.ProductSet):
            bounds = [(s.inf, s.sup) for s in K.sets]
            for pt in itertools.product(*bounds):
                corners.append(dict(zip(vars_list, pt)))
            center = [(s.inf + s.sup) / 2 for s in K.sets]
            corners.append(dict(zip(vars_list, center)))
        else:
            corners = [
                {vars_list[0]: K.inf}, 
                {vars_list[0]: K.sup}, 
                {vars_list[0]: (K.inf + K.sup) / 2}
            ]

        neg_q = False
        for g in grad_norms:
            for pt in corners:
                try:
                    val = g.subs(pt)
                except Exception:
                    continue
                
                # Check if the limit of the gradient magnitude is infinite
                try:
                    lim = sympy.limit(sympy.Abs(val), k_sym, sympy.oo)
                    if lim == sympy.oo:
                        neg_q = True
                        break
                except Exception:
                    pass
                
                # Fallback: check if the gradient magnitude grows significantly for large k
                try:
                    v1 = complex(val.subs(k_sym, 1).evalf())
                    v1000 = complex(val.subs(k_sym, 1000).evalf())
                    if abs(v1000) > abs(v1) + 100:
                        neg_q = True
                        break
                except Exception:
                    pass
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Omega is an open subset of R^n",
    "H_2: F is a family of harmonic functions on Omega",
    "H_3: K is a compact subset of Omega",
    "¬Q: F is not uniformly equicontinuous on K"
]

N_HYP = 3
NEG_Q_INDEX = 3