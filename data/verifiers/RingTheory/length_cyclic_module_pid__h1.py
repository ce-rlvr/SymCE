import sympy
from sympy import Symbol, Poly, expand, isprime, factor_list

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')
y = Symbol('y')

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should specify the ring and the elements.
    Expected witness format:
      (ring_name, a, u, primes, exponents)
    Supported ring_names for counterexamples: 'ZZ[x]', 'QQ[x,y]'
    """
    try:
        if isinstance(witness, dict):
            ring_name = witness.get('ring', 'ZZ[x]')
            a = witness['a']
            u = witness['u']
            primes = witness['primes']
            exponents = witness['exponents']
        else:
            if isinstance(witness[0], str):
                ring_name, a, u, primes, exponents = witness
            else:
                ring_name = 'ZZ[x]'
                a, u, primes, exponents = witness
    except Exception:
        return [False, False, False]

    # H1: a is a non-zero non-unit element of R
    try:
        h1_ok = False
        if ring_name == 'ZZ':
            a_int = int(a)
            h1_ok = (a_int != 0) and (abs(a_int) != 1)
        elif ring_name == 'ZZ[x]':
            p = Poly(a, x, domain='ZZ')
            h1_ok = not p.is_zero and not (p.is_constant() and abs(int(p.as_expr())) == 1)
        elif ring_name == 'QQ[x,y]':
            p = Poly(a, x, y, domain='QQ')
            h1_ok = not p.is_zero and not p.is_constant()
    except Exception:
        h1_ok = False

    # H2: a = u p_1^{k_1} \cdots p_m^{k_m} is a factorization of a, where p_i are prime elements, k_i are positive integers, and u is a unit
    try:
        h2_ok = False
        prod = u
        for p_elem, k in zip(primes, exponents):
            prod *= p_elem**k
        
        if expand(a) == expand(prod):
            # check u is unit
            u_ok = False
            if ring_name == 'ZZ':
                u_ok = abs(int(u)) == 1
            elif ring_name == 'ZZ[x]':
                p_u = Poly(u, x, domain='ZZ')
                u_ok = p_u.is_constant() and abs(int(p_u.as_expr())) == 1
            elif ring_name == 'QQ[x,y]':
                p_u = Poly(u, x, y, domain='QQ')
                u_ok = p_u.is_constant() and not p_u.is_zero
            
            if u_ok:
                # check primes
                primes_ok = True
                if not primes:
                    primes_ok = False
                else:
                    for p_elem in primes:
                        if ring_name == 'ZZ':
                            if not isprime(abs(int(p_elem))):
                                primes_ok = False
                                break
                        elif ring_name == 'ZZ[x]':
                            poly = Poly(p_elem, x, domain='ZZ')
                            if poly.is_zero:
                                primes_ok = False
                                break
                            elif poly.is_constant():
                                if not isprime(abs(int(poly.as_expr()))):
                                    primes_ok = False
                                    break
                            else:
                                if abs(poly.content()) != 1:
                                    primes_ok = False
                                    break
                                factors = factor_list(poly.as_expr(), domain='QQ')[1]
                                if len(factors) != 1 or factors[0][1] != 1:
                                    primes_ok = False
                                    break
                        elif ring_name == 'QQ[x,y]':
                            poly = Poly(p_elem, x, y, domain='QQ')
                            if poly.is_zero or poly.is_constant():
                                primes_ok = False
                                break
                            factors = factor_list(poly.as_expr(), domain='QQ')[1]
                            if len(factors) != 1 or factors[0][1] != 1:
                                primes_ok = False
                                break
                        else:
                            primes_ok = False
                            break
                
                if primes_ok:
                    # check exponents
                    exps_ok = True
                    if not exponents or len(exponents) != len(primes):
                        exps_ok = False
                    else:
                        for k in exponents:
                            if type(k) not in (int, sympy.Integer) or int(k) != k or k <= 0:
                                exps_ok = False
                                break
                    
                    if exps_ok:
                        h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q: The R-module R/<a> does not have finite length equal to \sum_{i=1}^m k_i
    # For ZZ[x] and QQ[x,y], the length of R/<a> is infinite for any non-zero non-unit a.
    try:
        neg_q_ok = False
        if ring_name in ['ZZ[x]', 'QQ[x,y]']:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a is a non-zero non-unit element of R",
    "H_2: a = u p_1^{k_1} \\cdots p_m^{k_m} is a factorization of a, where p_i are prime elements, k_i are positive integers, and u is a unit",
    "¬Q: The R-module R/<a> does not have finite length equal to \\sum_{i=1}^m k_i"
]

N_HYP = 2
NEG_Q_INDEX = 2