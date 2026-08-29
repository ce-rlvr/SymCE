import sympy
from sympy import Symbol, Poly, Dummy, groebner
from sympy.abc import x, y, z, a, b, c, d, t

def conditions(witness):
    try:
        # Unpack the witness
        if isinstance(witness, dict):
            var = witness.get('x', Symbol('x'))
            f = witness.get('f')
            g = witness.get('g')
            I_gens = witness.get('I', [])
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
                var = Symbol('x')
                I_gens = []
            elif len(witness) == 3:
                if isinstance(witness[2], (list, tuple, set)):
                    f, g, I_gens = witness
                    var = Symbol('x')
                else:
                    var, f, g = witness
                    I_gens = []
            elif len(witness) == 4:
                var, f, g, I_gens = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        # H1: R is a commutative ring with identity
        h1 = True
        
        # H2: f and g are polynomials over R
        try:
            poly_f = Poly(f, var)
            poly_g = Poly(g, var)
            h2 = True
        except Exception:
            h2 = False
            
        # H3: sqrt(I) denotes the radical of an ideal I
        h3 = True
        
        if not h2:
            return [h1, h2, h3, False]
            
        cf = poly_f.coeffs()
        cg = poly_g.coeffs()
        poly_fg = Poly(f * g, var)
        cfg = poly_fg.coeffs()
        
        # Extract variables of the ring R
        R_vars = set()
        for coeff in cf + cg + cfg + list(I_gens):
            if hasattr(coeff, 'free_symbols'):
                R_vars.update(coeff.free_symbols)
        if var in R_vars:
            R_vars.remove(var)
        R_vars = list(R_vars)
        
        cfg_gens = list(cfg) + list(I_gens)
        cfg_cfcg_gens = [c1 * c2 for c1 in cf for c2 in cg] + list(I_gens)
        
        def in_radical(elem, ideal_gens, vars_list):
            t_var = Dummy('t')
            gens = list(ideal_gens) + [1 - t_var * elem]
            try:
                # Try computing Groebner basis over ZZ first (most general for commutative rings)
                gb = groebner(gens, *(list(vars_list) + [t_var]), domain='ZZ')
                return len(gb) == 1 and gb[0] == 1
            except Exception:
                try:
                    # Fallback to default domain (e.g., QQ)
                    gb = groebner(gens, *(list(vars_list) + [t_var]))
                    return len(gb) == 1 and gb[0] == 1
                except Exception:
                    return False

        # Check if c(f)c(g) is in sqrt(c(fg))
        c_fg_in_rad = True
        for c1 in cf:
            for c2 in cg:
                if not in_radical(c1 * c2, cfg_gens, R_vars):
                    c_fg_in_rad = False
                    break
            if not c_fg_in_rad:
                break
                
        # Check if c(fg) is in sqrt(c(f)c(g))
        cfg_in_rad = True
        for coeff in cfg:
            if not in_radical(coeff, cfg_cfcg_gens, R_vars):
                cfg_in_rad = False
                break
                
        radicals_equal = c_fg_in_rad and cfg_in_rad
        neg_q = not radicals_equal

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: f and g are polynomials over R",
    "H_3: sqrt(I) denotes the radical of an ideal I",
    "¬Q: sqrt(c(fg)) != sqrt(c(f)c(g))"
]

N_HYP = 3
NEG_Q_INDEX = 3