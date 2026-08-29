import sympy
from sympy import Symbol, Interval, solveset, Eq, integrate, sympify
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness.get('f', 0), witness.get('g', 1), witness.get('a', 0), witness.get('b', 0)
    elif isinstance(witness, (list, tuple)):
        return witness[0], witness[1], witness[2], witness[3]
    else:
        return getattr(witness, 'f', 0), getattr(witness, 'g', 1), getattr(witness, 'a', 0), getattr(witness, 'b', 0)

def conditions(witness) -> list[bool]:
    try:
        f_raw, g_raw, a_raw, b_raw = extract_witness(witness)
        f = sympify(f_raw, locals={'x': x})
        g = sympify(g_raw, locals={'x': x})
        a = sympify(a_raw, locals={'x': x})
        b = sympify(b_raw, locals={'x': x})

        # Unify the symbol 'x' in case the witness used a different instance of 'x'
        for sym in f.free_symbols | g.free_symbols | a.free_symbols | b.free_symbols:
            if sym.name == 'x' and sym != x:
                f = f.subs(sym, x)
                g = g.subs(sym, x)
                a = a.subs(sym, x)
                b = b.subs(sym, x)

        # The interval bounds must be constants
        if a.free_symbols or b.free_symbols:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    def check_h1():
        try:
            if bool(a > b):
                return True
            if bool(a == b):
                v_f = f.subs(x, a)
                v_g = g.subs(x, a)
                return bool(v_f.is_real and v_g.is_real)
            
            dom_f = continuous_domain(f, x, Interval(a, b))
            dom_g = continuous_domain(g, x, Interval(a, b))
            return bool(Interval(a, b).is_subset(dom_f) and Interval(a, b).is_subset(dom_g))
        except Exception:
            return False

    def check_h2():
        try:
            if bool(a >= b):
                return True
            zeros = solveset(g, x, domain=Interval.open(a, b))
            return bool(zeros.is_empty == True)
        except Exception:
            return False

    def check_neg_Q():
        try:
            if bool(a >= b):
                return True
            int_f = integrate(f, (x, a, b))
            int_g = integrate(g, (x, a, b))
            
            if int_g.is_zero or sympy.simplify(int_g) == 0:
                return True
                
            LHS = int_f / int_g
            RHS = f / g
            solutions = solveset(Eq(RHS, LHS), x, domain=Interval.open(a, b))
            return bool(solutions.is_empty == True)
        except Exception:
            return False

    return [check_h1(), check_h2(), check_neg_Q()]

CONDITION_LABELS = ["H_1: f and g on interval a to b are continuous", "H_2: g(x) != 0 for all x in open interval a to b", "\u00acQ: No c in open interval a to b satisfies the mean value equation"]

N_HYP = 2
NEG_Q_INDEX = 2