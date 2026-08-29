import sympy
from sympy.polys.domains import FF

# Top-level setup
Y = sympy.Symbol('Y')

def conditions(witness):
    try:
        p, q, a = witness
    except Exception:
        return [False, False, False]
        
    # H1: p is a prime number dividing q-1
    try:
        h1 = sympy.isprime(p) and (q - 1) % p == 0
    except Exception:
        h1 = False
        
    try:
        q_int = int(q)
        is_prime_power = (q_int >= 2 and len(sympy.factorint(q_int)) == 1)
    except Exception:
        is_prime_power = False

    # H2: a is an element of F_q that is not the p-th power of any element in F_q
    try:
        if not is_prime_power:
            h2 = False
        else:
            if sympy.isprime(q_int):
                a_int = int(a) % q_int
                if a_int == 0:
                    is_p_power = True
                else:
                    is_p_power = (pow(a_int, (q_int - 1) // int(p), q_int) == 1)
            else:
                F = FF(q_int)
                try:
                    a_val = F(a)
                except Exception:
                    a_val = a
                if a_val == F(0):
                    is_p_power = True
                else:
                    is_p_power = (a_val ** ((q_int - 1) // int(p)) == F(1))
            h2 = not is_p_power
    except Exception:
        h2 = False
        
    # neg_Q: x^p - a is reducible over F_q
    try:
        if not is_prime_power:
            neg_q = False
        else:
            if sympy.isprime(q_int):
                poly = Y**int(p) - int(a)
                factors = sympy.factor_list(poly, modulus=q_int)
                is_irreducible = len(factors[1]) == 1 and factors[1][0][1] == 1 and factors[1][0][0].degree() == int(p)
                neg_q = not is_irreducible
            else:
                F = FF(q_int)
                poly = sympy.Poly(Y**int(p) - a, Y, domain=F)
                is_irreducible = poly.is_irreducible
                neg_q = not is_irreducible
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number dividing q-1",
    "H_2: a is an element of F_q that is not the p-th power of any element in F_q",
    "¬Q: The binomial x^p - a is reducible over F_q"
]

N_HYP = 2
NEG_Q_INDEX = 2