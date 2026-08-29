import sympy as sp

x = sp.Symbol('x')

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a dictionary, tuple, or a single value representing p.
    Expected tuple formats: (p, zeta_p) or (p, Phi_p, Phi_p_prime, zeta_p).
    """
    p = None
    zeta_p = None
    Phi_p = None
    Phi_p_prime = None
    
    if isinstance(witness, dict):
        p = witness.get('p')
        zeta_p = witness.get('zeta_p')
        Phi_p = witness.get('Phi_p')
        Phi_p_prime = witness.get('Phi_p_prime')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 1:
            p = witness[0]
        elif len(witness) == 2:
            p, zeta_p = witness
        elif len(witness) == 3:
            p, Phi_p, Phi_p_prime = witness
        elif len(witness) >= 4:
            p, Phi_p, Phi_p_prime, zeta_p = witness[:4]
    else:
        p = witness

    # H1: p is a prime number
    try:
        h1 = bool(sp.isprime(p))
    except Exception:
        h1 = False

    # H2: \Phi_p(x) is the p-th cyclotomic polynomial
    try:
        if h1:
            expected_Phi = sp.cyclotomic_poly(int(p), x)
        else:
            expected_Phi = None
            
        if Phi_p is not None:
            Phi_p_sym = sp.sympify(Phi_p)
            if expected_Phi is None:
                h2 = False
            else:
                var = list(Phi_p_sym.free_symbols)[0] if Phi_p_sym.free_symbols else x
                h2 = bool(sp.simplify(Phi_p_sym.subs(var, x) - expected_Phi) == 0)
        else:
            Phi_p = expected_Phi
            h2 = True if h1 else False
    except Exception:
        h2 = False

    # H3: \Phi_p'(x) is the formal derivative of \Phi_p(x)
    try:
        if Phi_p is not None:
            Phi_p_sym = sp.sympify(Phi_p)
            var = list(Phi_p_sym.free_symbols)[0] if Phi_p_sym.free_symbols else x
            expected_prime = sp.diff(Phi_p_sym, var)
            if Phi_p_prime is not None:
                Phi_p_prime_sym = sp.sympify(Phi_p_prime)
                var_prime = list(Phi_p_prime_sym.free_symbols)[0] if Phi_p_prime_sym.free_symbols else x
                h3 = bool(sp.simplify(Phi_p_prime_sym.subs(var_prime, x) - expected_prime.subs(var, x)) == 0)
            else:
                Phi_p_prime = expected_prime
                h3 = True
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: \Phi_p'(\zeta_p) = p / (\zeta_p(\zeta_p - 1)) must FAIL
    try:
        if zeta_p is None:
            z = sp.Symbol('zeta_p')
        else:
            z = sp.sympify(zeta_p)
            
        if Phi_p_prime is None:
            neg_q = False
        else:
            Phi_p_prime_sym = sp.sympify(Phi_p_prime)
            var_prime = list(Phi_p_prime_sym.free_symbols)[0] if Phi_p_prime_sym.free_symbols else x
            lhs = Phi_p_prime_sym.subs(var_prime, z)
            rhs = sp.sympify(p) / (z * (z - 1))
            
            if lhs is sp.nan or lhs is sp.zoo or rhs is sp.nan or rhs is sp.zoo:
                neg_q = True
            elif isinstance(lhs, sp.Expr) or isinstance(rhs, sp.Expr):
                diff_expr = sp.simplify(lhs - rhs)
                if diff_expr == 0:
                    eq = True
                else:
                    if not diff_expr.free_symbols:
                        try:
                            eq = abs(complex(diff_expr.evalf())) < 1e-9
                        except Exception:
                            eq = False
                    else:
                        eq = False
                neg_q = not eq
            else:
                eq = (lhs == rhs)
                neg_q = not eq
    except ZeroDivisionError:
        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: \\Phi_p(x) is the p-th cyclotomic polynomial",
    "H_3: \\Phi_p'(x) is the formal derivative of \\Phi_p(x)",
    "¬Q: \\Phi_p'(\\zeta_p) != p / (\\zeta_p(\\zeta_p - 1))"
]

N_HYP = 3
NEG_Q_INDEX = 3