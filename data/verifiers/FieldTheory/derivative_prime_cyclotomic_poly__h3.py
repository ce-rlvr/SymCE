import sympy
from sympy import simplify, isprime, diff, exp, I, pi

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness):
    h1_ok = False
    h2_ok = False
    h3_ok = False
    neg_q_ok = False
    
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                p, zeta_p, Phi_p, Phi_p_prime = witness
            elif len(witness) == 3:
                p, zeta_p, Phi_p = witness
                Phi_p_prime = None
            elif len(witness) == 2:
                p, Phi_p = witness
                zeta_p = exp(2 * I * pi / p)
                Phi_p_prime = None
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # Determine the variable of the polynomial
    try:
        free_symbols = set()
        if hasattr(Phi_p, 'free_symbols'):
            free_symbols.update(Phi_p.free_symbols)
        if Phi_p_prime is not None and hasattr(Phi_p_prime, 'free_symbols'):
            free_symbols.update(Phi_p_prime.free_symbols)
            
        if len(free_symbols) >= 1:
            x_sym = sympy.Symbol('x')
            if x_sym in free_symbols:
                var = x_sym
            else:
                var = list(free_symbols)[0]
        else:
            var = sympy.Symbol('x')
    except Exception:
        var = sympy.Symbol('x')

    if Phi_p_prime is None:
        try:
            Phi_p_prime = diff(Phi_p, var)
        except Exception:
            return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1_ok = bool(isprime(p))
    except Exception:
        h1_ok = False

    # H2: \zeta_p is a primitive p-th root of unity in \mathbb{C}
    try:
        diff1 = simplify(zeta_p**p - 1)
        if diff1 == 0:
            cond1 = True
        else:
            try:
                cond1 = abs(complex(diff1.evalf())) < 1e-9
            except Exception:
                cond1 = False
                
        diff2 = simplify(zeta_p - 1)
        if diff2 == 0:
            cond2 = False
        else:
            try:
                cond2 = abs(complex(diff2.evalf())) > 1e-9
            except Exception:
                cond2 = True
                
        h2_ok = bool(cond1 and cond2)
    except Exception:
        h2_ok = False

    # H3: \Phi_p'(x) is the formal derivative of \Phi_p(x)
    try:
        deriv = diff(Phi_p, var)
        diff3 = simplify(deriv - Phi_p_prime)
        if diff3 == 0:
            h3_ok = True
        else:
            try:
                val = diff3.subs(var, 2.5).evalf()
                h3_ok = abs(complex(val)) < 1e-9
            except Exception:
                h3_ok = False
    except Exception:
        h3_ok = False

    # \neg Q: \Phi_p'(\zeta_p) \neq \frac{p}{\zeta_p(\zeta_p - 1)}
    try:
        lhs = Phi_p_prime.subs(var, zeta_p)
        rhs = p / (zeta_p * (zeta_p - 1))
        
        diff_val = simplify(lhs - rhs)
        if diff_val == 0:
            neg_q_ok = False
        else:
            try:
                num_val = complex(diff_val.evalf())
                neg_q_ok = abs(num_val) > 1e-9
            except Exception:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: \\zeta_p is a primitive p-th root of unity in \\mathbb{C}",
    "H_3: \\Phi_p'(x) is the formal derivative of \\Phi_p(x)",
    "\\neg Q: \\Phi_p'(\\zeta_p) \\neq \\frac{p}{\\zeta_p(\\zeta_p - 1)}"
]

N_HYP = 3
NEG_Q_INDEX = 3