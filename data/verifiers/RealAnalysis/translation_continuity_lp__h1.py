import sympy as sp
import math

x = sp.Symbol('x', real=True)
h = sp.Symbol('h', real=True)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample.
    The witness should be a tuple (f, p) where:
      - f is a sympy expression representing a function of x
      - p is a sympy number (e.g., sp.oo or 2)
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        f, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
        else:
            sym = sp.Symbol('x', real=True)
            for s in free_syms:
                if s.name == 'x':
                    sym = s
                    break
    except Exception:
        sym = sp.Symbol('x', real=True)

    def check_H1():
        try:
            if p < 1:
                return False
            if p == sp.oo:
                try:
                    frange = sp.calculus.util.function_range(f, sym, sp.S.Reals)
                    if frange.sup == sp.oo or frange.inf == -sp.oo:
                        return False
                    return True
                except Exception:
                    pass
                
                try:
                    lim_inf = sp.limit(f, sym, sp.oo)
                    lim_minf = sp.limit(f, sym, -sp.oo)
                    if abs(lim_inf) == sp.oo or abs(lim_minf) == sp.oo:
                        return False
                except Exception:
                    pass
                
                vals = []
                try:
                    func = sp.lambdify(sym, f, 'math')
                    for val in [0, 1, -1, 10, -10, 100, -100, 1000, -1000, 1e6, -1e6]:
                        try:
                            v = func(val)
                            v_abs = abs(v)
                            if not math.isnan(v_abs) and not math.isinf(v_abs):
                                vals.append(v_abs)
                        except Exception:
                            pass
                except Exception:
                    for val in [0, 1, -1, 10, -10, 100, -100, 1000, -1000, 1e6, -1e6]:
                        try:
                            v = abs(float(f.subs(sym, val)))
                            vals.append(v)
                        except Exception:
                            pass
                if vals and max(vals) > 1e5:
                    return False
                return True
            else:
                try:
                    lim_inf = sp.limit(f, sym, sp.oo)
                    if lim_inf != 0:
                        return False
                except Exception:
                    try:
                        if abs(float(f.subs(sym, 1000))) > 1e-2:
                            return False
                    except Exception:
                        pass
                        
                try:
                    lim_minf = sp.limit(f, sym, -sp.oo)
                    if lim_minf != 0:
                        return False
                except Exception:
                    try:
                        if abs(float(f.subs(sym, -1000))) > 1e-2:
                            return False
                    except Exception:
                        pass

                try:
                    integral = sp.Integral(sp.Abs(f)**p, (sym, -sp.oo, sp.oo)).doit()
                    if integral == sp.oo or integral == sp.nan:
                        return False
                    if integral.is_number and integral.is_real:
                        return float(integral) < float('inf')
                    return True
                except Exception:
                    return True
        except Exception:
            return False

    def check_H2():
        # The second hypothesis is a definition of the translation operator,
        # which is inherently satisfied by the mathematical context.
        return True

    def check_neg_Q():
        try:
            norms = []
            for h_val in [sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)]:
                diff = f.subs(sym, sym - h_val) - f
                if p == sp.oo:
                    norm = 0
                    try:
                        frange = sp.calculus.util.function_range(diff, sym, sp.S.Reals)
                        norm = max(abs(frange.inf), abs(frange.sup))
                    except Exception:
                        pass
                    
                    try:
                        norm_float = float(norm)
                        is_invalid = math.isnan(norm_float) or math.isinf(norm_float) or norm_float == 0
                    except Exception:
                        is_invalid = True
                        
                    if is_invalid:
                        pts = [float(h_val)/2, -float(h_val)/2] + [i*0.5 for i in range(-200, 200)]
                        vals = []
                        try:
                            func = sp.lambdify(sym, diff, 'math')
                            for pt in pts:
                                try:
                                    v = func(pt)
                                    v_abs = abs(v)
                                    if not math.isnan(v_abs) and not math.isinf(v_abs):
                                        vals.append(v_abs)
                                except Exception:
                                    pass
                        except Exception:
                            for pt in pts:
                                try:
                                    v = diff.subs(sym, pt)
                                    if v.is_real:
                                        vals.append(abs(float(v)))
                                except Exception:
                                    pass
                        if vals:
                            norm = max(vals)
                        else:
                            norm = 0
                    norms.append(float(norm))
                else:
                    integral = 0
                    try:
                        func = sp.lambdify(sym, diff, 'math')
                        for i in range(-2000, 2000):
                            pt = i * 0.05
                            try:
                                v = func(pt)
                                v_abs = abs(v)
                                if not math.isnan(v_abs) and not math.isinf(v_abs):
                                    integral += v_abs**float(p) * 0.05
                            except Exception:
                                pass
                    except Exception:
                        for i in range(-200, 200):
                            pt = i * 0.5
                            try:
                                v = diff.subs(sym, pt)
                                if v.is_real:
                                    integral += abs(float(v))**float(p) * 0.5
                            except Exception:
                                pass
                    norms.append(integral ** (1/float(p)))
            
            # If the limit is NOT zero, the norms should not decay to 0.
            if len(norms) == 3 and norms[-1] > 0.1 and norms[-1] > 0.5 * norms[0]:
                return True
            return False
        except Exception:
            return False

    h1 = check_H1()
    h2 = check_H2()
    nq = check_neg_Q()
    
    return [h1, h2, nq]

CONDITION_LABELS = [
    "H_1: f is a Lebesgue measurable function in L^p(R)",
    "H_2: T_h f is the translation operator defined by (T_h f)(x) = f(x-h) for h in R",
    "¬Q: The mapping h |-> T_h f is not uniformly continuous from R into L^p(R)"
]

N_HYP = 2
NEG_Q_INDEX = 2