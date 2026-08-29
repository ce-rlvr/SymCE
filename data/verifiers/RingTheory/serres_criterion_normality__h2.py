import sympy
from sympy import sympify, diff, Poly, groebner
from sympy.abc import x, y, z, t, u, v, w
from itertools import combinations

def ideal_dimension(F, vars):
    """
    Computes the Krull dimension of the affine variety defined by the ideal F.
    Returns -1 if the ideal is the unit ideal.
    """
    try:
        gb = groebner(F, *vars)
        polys = [Poly(p, *vars) for p in gb]
    except Exception:
        return -1
        
    if len(polys) == 1:
        if polys[0].is_zero:
            return len(vars)
        if polys[0].is_one:
            return -1
            
    try:
        lms = []
        for p in polys:
            if p.is_zero:
                continue
            lms.append(p.LM())
    except Exception:
        return -1
        
    n = len(vars)
    
    # The dimension is the maximum size of a subset of variables that are 
    # algebraically independent modulo the initial ideal.
    for d in range(n, -1, -1):
        for subset in combinations(range(n), d):
            independent = True
            for lm in lms:
                # Check if the leading monomial uses ONLY variables in `subset`
                if all(lm[i] == 0 for i in range(n) if i not in subset):
                    independent = False
                    break
            if independent:
                return d
                
    return -1

def conditions(witness):
    try:
        # Handle known string counterexamples
        if isinstance(witness, str):
            w_str = witness.replace(" ", "")
            if w_str.lower() in ["z[sqrt(-3)]", "z[i*sqrt(3)]", "z[sqrt(-5)]"]:
                # Z[sqrt(-5)] is a Dedekind domain, hence normal (neg_Q is False)
                if w_str.lower() == "z[sqrt(-5)]":
                    return [True, True, False]
                # Z[sqrt(-3)] is S2 but not normal
                return [True, True, True]
            
            # Extract polynomial from string like "k[x,y]/(y^2-x^3)"
            if "/(" in w_str and w_str.endswith(")"):
                start = w_str.find("/(") + 2
                end = len(w_str) - 1
                witness = w_str[start:end]
                
        if isinstance(witness, (list, tuple)):
            if len(witness) == 1:
                witness = witness[0]
            else:
                return [False, False, False]
                
        from sympy import Expr
        
        f = None
        vars = None
        
        # Extract from SymPy QuotientRing or Ideal objects
        if hasattr(witness, 'base_ring') and hasattr(witness, 'base_ideal'):
            try:
                I = witness.base_ideal.gens
                if len(I) == 1:
                    f = I[0].as_expr()
                    vars = [v.as_expr() for v in witness.base_ring.gens]
            except Exception:
                pass
        elif hasattr(witness, 'gens') and not isinstance(witness, Expr):
            try:
                I = witness.gens
                if len(I) == 1:
                    f = I[0]
                    if hasattr(f, 'as_expr'):
                        f = f.as_expr()
                    vars = list(f.free_symbols)
            except Exception:
                pass
                
        # Fallback to sympify
        if f is None:
            try:
                f = sympify(witness)
                if isinstance(f, Poly):
                    vars = list(f.gens)
                    f = f.as_expr()
                elif isinstance(f, Expr):
                    vars = list(f.free_symbols)
            except Exception:
                pass
                
        if f is None:
            return [False, False, False]
            
        if not vars:
            if hasattr(f, 'is_zero') and f.is_zero:
                return [True, True, False]
            return [False, False, False]
            
        if hasattr(f, 'is_constant') and f.is_constant():
            return [False, False, False]
            
        if hasattr(f, 'is_polynomial'):
            try:
                if not f.is_polynomial(*vars):
                    return [False, False, False]
            except Exception:
                return [False, False, False]
            
        if hasattr(f, 'is_zero') and f.is_zero:
            return [True, True, False]
            
        # H1: Commutative Noetherian ring
        # A hypersurface k[X]/(f) is an affine algebra, hence commutative Noetherian.
        h1 = True
        
        # H2: Satisfies Serre's condition (S2)
        # A hypersurface in a regular ring is Cohen-Macaulay, hence satisfies S2.
        h2 = True
        
        # neg_Q: Not a normal ring
        # For a ring satisfying S2, it is normal iff it satisfies R1 (regular in codimension 1).
        # This means the singular locus must have dimension <= dim(R) - 2.
        # dim(R) = n - 1. So we need dim(Sing) <= n - 3 for it to be normal.
        n = len(vars)
        J = [f] + [diff(f, v) for v in vars]
        
        dim_sing = ideal_dimension(J, vars)
        
        # neg_Q is True if it is NOT normal
        neg_q = dim_sing > n - 3
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R satisfies Serre's condition (S2)",
    "¬Q: R is not a normal ring"
]

N_HYP = 2
NEG_Q_INDEX = 2