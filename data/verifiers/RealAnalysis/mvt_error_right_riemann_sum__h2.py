import sympy

x = sympy.Symbol('x')

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = ['H_1: f is continuously differentiable', 'not Q: no c satisfies the equation']

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        f, a, b = witness
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        
        if isinstance(f, str):
            f = sympy.sympify(f)
            
        if hasattr(f, 'free_symbols'):
            free_syms = f.free_symbols
            if len(free_syms) == 1:
                var = list(free_syms)[0]
            elif len(free_syms) == 0:
                var = x
            else:
                return [False, False]
        else:
            f = sympy.sympify(f)
            var = x
            
        try:
            if a > b:
                h1 = False
            elif a == b:
                df = sympy.diff(f, var)
                v_f = f.subs(var, a)
                v_df = df.subs(var, a)
                h1 = (v_f.is_real is not False) and (v_df.is_real is not False)
            else:
                df = sympy.diff(f, var)
                dom_f = sympy.calculus.util.continuous_domain(f, var, sympy.Interval(a, b))
                dom_df = sympy.calculus.util.continuous_domain(df, var, sympy.Interval(a, b))
                h1 = (dom_f == sympy.Interval(a, b)) and (dom_df == sympy.Interval(a, b))
        except Exception:
            h1 = False
            
        try:
            if a >= b:
                neg_q = True
            else:
                L = sympy.integrate(f, (var, a, b)) - f.subs(var, b) * (b - a)
                target_df = -2 * L / (b - a)**2
                df = sympy.diff(f, var)
                sols = sympy.solveset(df - target_df, var, domain=sympy.Interval.open(a, b))
                
                if sols == sympy.S.EmptySet:
                    neg_q = True
                elif getattr(sols, 'is_empty', None) is False:
                    neg_q = False
                else:
                    neg_q = False
        except Exception:
            neg_q = False
            
    except Exception:
        return [False, False]
        
    return [bool(h1), bool(neg_q)]