import sympy
from sympy import Symbol, S, diff, limit, oo

# Top-level setup
x, y, z = sympy.symbols('x y z', real=True)
R = S.Reals
Z = S.Integers
N = S.Naturals

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (domain, family_of_functions)
    where domain is a sympy Set (e.g., S.Reals) and family_of_functions is a 
    sympy expression or a list of sympy expressions.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            domain, funcs = witness
        else:
            return [False, False]
            
        if not isinstance(funcs, (list, tuple)):
            funcs = [funcs]
    except Exception:
        return [False, False]
        
    # H1: F is a family of continuous functions from X to R
    h1_ok = True
    try:
        from sympy.calculus.util import continuous_domain
        for f in funcs:
            syms = f.free_symbols
            if len(syms) == 1:
                var = list(syms)[0]
            elif len(syms) == 0:
                var = Symbol('x', real=True)
            else:
                var = list(syms)[0]
                for s in syms:
                    if s.name == 'x':
                        var = s
                        break
            
            cd = continuous_domain(f, var, S.Reals)
            if not domain.is_subset(cd):
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # Negated Conclusion: F is equicontinuous but does not share a common modulus of continuity.
    # For a finite family, equicontinuity is equivalent to continuity of all functions (checked in H1).
    # Not sharing a common modulus is equivalent to at least one function NOT being uniformly continuous.
    neg_q_ok = False
    try:
        if h1_ok:
            for f in funcs:
                syms = f.free_symbols
                if len(syms) == 1:
                    var = list(syms)[0]
                elif len(syms) == 0:
                    var = Symbol('x', real=True)
                else:
                    var = list(syms)[0]
                    for s in syms:
                        if s.name == 'x':
                            var = s
                            break
                
                not_unif_cont = False
                
                # Check endpoints for bounded domains or bounded parts of unbounded domains
                if isinstance(domain, sympy.Interval):
                    if domain.start != -oo:
                        try:
                            L_start = limit(f, var, domain.start, dir='+')
                            if not L_start.has(sympy.Limit):
                                if L_start in [oo, -oo] or type(L_start).__name__ == 'AccumBounds':
                                    not_unif_cont = True
                        except Exception:
                            pass
                    if domain.end != oo:
                        try:
                            L_end = limit(f, var, domain.end, dir='-')
                            if not L_end.has(sympy.Limit):
                                if L_end in [oo, -oo] or type(L_end).__name__ == 'AccumBounds':
                                    not_unif_cont = True
                        except Exception:
                            pass
                            
                # Check unbounded domains
                if not domain.is_bounded:
                    sup_unif = False
                    inf_unif = False
                    
                    if domain.sup == oo:
                        try:
                            Lf_sup = limit(f, var, oo)
                            if not Lf_sup.has(sympy.Limit) and Lf_sup.is_real:
                                sup_unif = True
                        except Exception:
                            pass
                            
                    if domain.inf == -oo:
                        try:
                            Lf_inf = limit(f, var, -oo)
                            if not Lf_inf.has(sympy.Limit) and Lf_inf.is_real:
                                inf_unif = True
                        except Exception:
                            pass
                            
                    df = diff(f, var)
                    if domain.sup == oo and not sup_unif:
                        try:
                            L = limit(df, var, oo)
                            if not L.has(sympy.Limit):
                                if L in [oo, -oo]:
                                    not_unif_cont = True
                                elif type(L).__name__ == 'AccumBounds':
                                    if L.min == -oo or L.max == oo:
                                        not_unif_cont = True
                        except Exception:
                            pass
                    if domain.inf == -oo and not inf_unif:
                        try:
                            L = limit(df, var, -oo)
                            if not L.has(sympy.Limit):
                                if L in [oo, -oo]:
                                    not_unif_cont = True
                                elif type(L).__name__ == 'AccumBounds':
                                    if L.min == -oo or L.max == oo:
                                        not_unif_cont = True
                        except Exception:
                            pass
                            
                    if not not_unif_cont:
                        if domain.sup == oo:
                            try:
                                n = sympy.Symbol('n', integer=True, positive=True)
                                diff_val = sympy.simplify(f.subs(var, n) - f.subs(var, n + 1/n))
                                L_diff = limit(diff_val, n, oo)
                                if not L_diff.has(sympy.Limit) and L_diff != 0:
                                    not_unif_cont = True
                            except Exception:
                                pass
                        elif domain.inf == -oo:
                            try:
                                n = sympy.Symbol('n', integer=True, positive=True)
                                diff_val = sympy.simplify(f.subs(var, -n) - f.subs(var, -n - 1/n))
                                L_diff = limit(diff_val, n, oo)
                                if not L_diff.has(sympy.Limit) and L_diff != 0:
                                    not_unif_cont = True
                            except Exception:
                                pass
                                
                if not_unif_cont:
                    neg_q_ok = True
                    break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a family of continuous functions from X to R",
    "¬Q: F is equicontinuous but does not share a common modulus of continuity"
]

N_HYP = 1
NEG_Q_INDEX = 1