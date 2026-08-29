import sympy
from sympy import Symbol, isprime, simplify, diff, I, pi, exp
from sympy.polys.specialpolys import cyclotomic_poly

# Top-level setup
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: zeta_p is a primitive p-th root of unity in C",
    "H_3: Phi_p(x) is the p-th cyclotomic polynomial",
    "not Q: Phi_p'(zeta_p) != p / (zeta_p * (zeta_p - 1))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1, h2, h3, neg_q = False, False, False, False
    
    p, zeta, Phi, var_x = None, None, None, None
    
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            zeta = witness.get('zeta')
            Phi = witness.get('Phi')
            var_x = witness.get('x', x)
        elif isinstance(witness, (int, sympy.Integer)):
            p = int(witness)
            var_x = x
            zeta = exp(2 * I * pi / p)
            Phi = cyclotomic_poly(p, var_x)
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                p, zeta, Phi, var_x = witness
            elif len(witness) == 3:
                p, zeta, Phi = witness
                var_x = x
            elif len(witness) == 2:
                p, zeta = witness
                var_x = x
                Phi = cyclotomic_poly(p, var_x)
            elif len(witness) == 1:
                p = witness[0]
                var_x = x
                zeta = exp(2 * I * pi / p)
                Phi = cyclotomic_poly(p, var_x)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: zeta_p is a primitive p-th root of unity in C
    try:
        if h1:
            val1 = zeta**p - 1
            val2 = zeta - 1
            
            try:
                num1 = complex(val1.evalf())
                eq1 = (abs(num1) <= 1e-5) and bool(simplify(val1) == 0)
            except Exception:
                eq1 = bool(simplify(val1) == 0)
                
            try:
                num2 = complex(val2.evalf())
                eq2 = (abs(num2) > 1e-5) or bool(simplify(val2) != 0)
            except Exception:
                eq2 = bool(simplify(val2) != 0)
                
            h2 = bool(eq1 and eq2)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: Phi_p(x) is the p-th cyclotomic polynomial
    try:
        expected_Phi = cyclotomic_poly(p, var_x)
        h3 = bool(simplify(Phi - expected_Phi) == 0)
    except Exception:
        h3 = False

    # not Q: Phi_p'(zeta_p) != p / (zeta_p * (zeta_p - 1))
    try:
        lhs = diff(Phi, var_x).subs(var_x, zeta)
        rhs = p / (zeta * (zeta - 1))
        diff_val = lhs - rhs
        
        try:
            num_val = complex(diff_val.evalf())
            if abs(num_val) > 1e-5:
                neg_q = True
            else:
                neg_q = bool(simplify(diff_val) != 0)
        except Exception:
            neg_q = bool(simplify(diff_val) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]