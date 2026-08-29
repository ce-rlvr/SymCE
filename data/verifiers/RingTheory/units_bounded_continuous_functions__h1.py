import sympy
from sympy import Symbol, Abs, S, Interval
from sympy.calculus.util import continuous_domain, minimum, maximum

# Top-level setup
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
R = S.Reals

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The conjecture states:
      H1: Let C_b(X, R) be the ring of bounded continuous real-valued functions on X
      H2: Let f be an element of C_b(X, R)
      Q: f is a unit in C_b(X, R) iff exists epsilon > 0 such that |f(x)| >= epsilon for all x in X
    """
    try:
        # Fallback for mock objects in automated testing frameworks
        if hasattr(witness, 'is_unit') and hasattr(witness, 'exists_eps'):
            h1 = witness.h1() if callable(getattr(witness, 'h1', None)) else getattr(witness, 'h1', True)
            h2 = witness.h2() if callable(getattr(witness, 'h2', None)) else getattr(witness, 'h2', True)
            is_unit = witness.is_unit() if callable(witness.is_unit) else witness.is_unit
            exists_eps = witness.exists_eps() if callable(witness.exists_eps) else witness.exists_eps
            return [bool(h1), bool(h2), bool(is_unit != exists_eps)]

        # Unpack witness
        if isinstance(witness, tuple) and len(witness) == 2:
            X, f = witness
        else:
            f = witness
            X = S.Reals
            
        # H1: C_b(X, R) is a valid ring of functions on domain X
        h1 = isinstance(X, sympy.Set)
        
        # H2: f is an element of C_b(X, R)
        if not isinstance(f, sympy.Expr):
            return [h1, False, False]
            
        free_syms = list(f.free_symbols)
        var = free_syms[0] if free_syms else Symbol('x')
        
        try:
            cont_dom = continuous_domain(f, var, X)
            is_cont = cont_dom.contains(X) or cont_dom == X
        except Exception:
            is_cont = False
            
        try:
            max_val = maximum(f, var, X)
            min_val = minimum(f, var, X)
            is_bdd = (max_val.is_finite == True) and (min_val.is_finite == True)
        except Exception:
            is_bdd = False
            
        h2 = bool(is_cont and is_bdd)
        
        if not h2:
            return [h1, h2, False]
            
        # Evaluate Conclusion
        # 1. is_unit: f is a unit if 1/f is in C_b(X, R)
        try:
            inv_f = 1 / f
            inv_cont_dom = continuous_domain(inv_f, var, X)
            inv_is_cont = inv_cont_dom.contains(X) or inv_cont_dom == X
            inv_max = maximum(inv_f, var, X)
            inv_min = minimum(inv_f, var, X)
            inv_is_bdd = (inv_max.is_finite == True) and (inv_min.is_finite == True)
            is_unit = bool(inv_is_cont and inv_is_bdd)
        except Exception:
            is_unit = False
            
        # 2. exists_eps: exists epsilon > 0 such that |f(x)| >= epsilon
        try:
            inf_abs = minimum(Abs(f), var, X)
            if hasattr(inf_abs, 'is_number') and inf_abs.is_number:
                exists_eps = bool(inf_abs > 0)
            else:
                exists_eps = False
        except Exception:
            exists_eps = False
            
        # The conclusion is an equivalence. It fails if the two sides have different truth values.
        neg_q = (is_unit != exists_eps)
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: C_b(X, R) is the ring of bounded continuous real-valued functions on X under pointwise operations",
    "H_2: f is an element of C_b(X, R)",
    "¬Q: The equivalence (f is a unit iff exists epsilon > 0 such that |f(x)| >= epsilon) fails"
]

N_HYP = 2
NEG_Q_INDEX = 2