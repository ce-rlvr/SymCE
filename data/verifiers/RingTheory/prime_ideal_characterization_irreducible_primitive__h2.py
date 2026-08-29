import sympy
from sympy import abc
from sympy.polys.polytools import factor_list

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        domain_str, f = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = domain_str in ['ZZ', 'QQ']
    except Exception:
        h1_ok = False

    try:
        f_expr = sympy.sympify(f)
        is_zero = (f_expr == 0)
        
        is_unit = False
        if domain_str == 'ZZ':
            is_unit = (f_expr in [sympy.Integer(1), sympy.Integer(-1)])
        elif domain_str == 'QQ':
            is_unit = f_expr.is_number and not is_zero

        is_irred = False
        if not is_zero and not is_unit:
            coeff, factors = factor_list(f_expr, domain=domain_str)
            if domain_str == 'QQ':
                is_irred = (len(factors) == 1 and factors[0][1] == 1)
            elif domain_str == 'ZZ':
                if len(factors) == 1 and factors[0][1] == 1 and abs(coeff) == 1:
                    is_irred = True
                elif len(factors) == 0 and sympy.isprime(abs(coeff)):
                    is_irred = True

        is_prime_ideal = is_zero or is_irred
        q_holds = (is_prime_ideal == is_irred)
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: The equivalence between <f> being a prime ideal and f being irreducible fails"
]

N_HYP = 1
NEG_Q_INDEX = 1