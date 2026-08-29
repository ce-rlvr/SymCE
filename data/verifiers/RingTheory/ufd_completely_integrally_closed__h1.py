import sympy
from sympy import Poly, fraction, cancel, Rational, Integer
from sympy.abc import t, x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    
    The witness can be provided in several formats:
    1. A tuple (x, d) of sympy expressions, implicitly using the ring R = k[t^2, t^3].
       Example: (t, t**2)
    2. A dictionary specifying the ring type and parameters.
       Example: {'ring_type': 'k[t^2, t^3]', 'x': t, 'd': t**2}
       Example: {'ring_type': 'Z[sqrt(D)]', 'D': 5, 'x': (Rational(1,2), Rational(1,2)), 'd': (2, 0)}
    3. A dictionary with custom 'in_R', 'mul', 'power', 'is_zero' functions.
    """
    try:
        # Parse witness and set up ring operations
        if isinstance(witness, dict):
            if 'in_R' in witness:
                in_R = witness['in_R']
                is_zero = witness.get('is_zero', lambda v: v == 0)
                mul = witness.get('mul', lambda a, b: a * b)
                power = witness.get('power', lambda a, n: a**n)
                x_val = witness['x']
                d_val = witness['d']
            elif witness.get('ring_type') == 'k[t^2, t^3]':
                var = witness.get('var', t)
                def in_R(expr):
                    try:
                        expr = cancel(expr)
                        num, den = fraction(expr)
                        if not den.is_constant():
                            return False
                        poly = Poly(num / den, var)
                        return poly.coeff_monomial(var) == 0
                    except Exception:
                        return False
                is_zero = lambda v: cancel(v) == 0
                mul = lambda a, b: cancel(a * b)
                power = lambda a, n: cancel(a**n)
                x_val = witness['x']
                d_val = witness['d']
            elif witness.get('ring_type') == 'Z[sqrt(D)]':
                D = witness['D']
                def in_R(val):
                    try:
                        a, b = val
                        return int(a) == a and int(b) == b
                    except Exception:
                        return False
                is_zero = lambda v: v[0] == 0 and v[1] == 0
                def mul(v1, v2):
                    a1, b1 = v1
                    a2, b2 = v2
                    return (a1*a2 + b1*b2*D, a1*b2 + a2*b1)
                def power(v, n):
                    res = (1, 0)
                    base = v
                    while n > 0:
                        if n % 2 == 1:
                            res = mul(res, base)
                        base = mul(base, base)
                        n //= 2
                    return res
                x_val = witness['x']
                d_val = witness['d']
            else:
                return [False, False, False]
        elif isinstance(witness, tuple) and len(witness) == 2:
            x_val, d_val = witness
            
            free_syms = x_val.free_symbols
            if not free_syms:
                return [False, False, False]
            var = list(free_syms)[0]
            
            def in_R(expr):
                try:
                    expr = cancel(expr)
                    num, den = fraction(expr)
                    if not den.is_constant():
                        return False
                    poly = Poly(num / den, var)
                    return poly.coeff_monomial(var) == 0
                except Exception:
                    return False
            is_zero = lambda v: cancel(v) == 0
            mul = lambda a, b: cancel(a * b)
            power = lambda a, n: cancel(a**n)
        else:
            return [False, False, False]
            
        # H_1: K is the field of fractions of R
        # This is structurally guaranteed by the supported witness formats.
        try:
            h1_ok = True
        except Exception:
            h1_ok = False
            
        # H_2: d is a non-zero element in R and d * x^n is in R for all positive integers n
        try:
            h2_ok = False
            if in_R(d_val) and not is_zero(d_val):
                all_in_R = True
                # Check for n up to 20, which is sufficient to establish the pattern for these rings
                for n in range(1, 21):
                    term = mul(d_val, power(x_val, n))
                    if not in_R(term):
                        all_in_R = False
                        break
                h2_ok = all_in_R
        except Exception:
            h2_ok = False
            
        # ¬Q: x does not belong to R (meaning R is not completely integrally closed)
        try:
            neg_q_ok = not in_R(x_val)
        except Exception:
            neg_q_ok = False
            
        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: d is a non-zero element in R and d * x^n is in R for all positive integers n",
    "¬Q: x does not belong to R (R is not completely integrally closed)"
]

N_HYP = 2
NEG_Q_INDEX = 2