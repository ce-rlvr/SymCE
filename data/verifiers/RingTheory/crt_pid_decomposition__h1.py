import sympy
from sympy import sympify, expand, Poly, cancel, Rational, Float, groebner, gcd, resultant
from sympy.ntheory import isprime
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: a is a non-zero, non-unit element of R",
    "H_2: a = u p_1^{e_1} ... p_k^{e_k} is the prime factorization of a, with p_i pairwise non-associate primes, e_i >= 1, u is a unit",
    "¬Q: R/(a) is not isomorphic to the direct product of R/(p_i^{e_i})"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_domain(exprs):
    for expr in exprs:
        try:
            for atom in expr.atoms(Rational, Float):
                if not atom.is_integer:
                    return 'QQ'
        except Exception:
            pass
    return 'ZZ'

def is_prime_in_R(p, free_vars, domain):
    try:
        p = sympify(p)
        if p == 0: return False
        
        if p.is_number:
            if domain == 'ZZ':
                return isprime(abs(int(p)))
            else:
                return False
                
        poly = Poly(p, *free_vars, domain=domain)
        if domain == 'ZZ':
            if poly.content() != 1:
                return False
        return poly.is_irreducible
    except Exception:
        return False

def are_associates(p1, p2, free_vars, domain):
    try:
        if domain == 'ZZ':
            return expand(p1 - p2) == 0 or expand(p1 + p2) == 0
        else:
            q = cancel(p1 / p2)
            return q.is_number and q != 0
    except Exception:
        return False

def is_comaximal(A, B, free_vars, domain):
    if not free_vars:
        if domain == 'ZZ':
            return gcd(A, B) == 1
        else:
            return True
            
    try:
        if len(free_vars) == 1 and domain == 'ZZ':
            res = resultant(A, B, free_vars[0])
            if res == 1 or res == -1:
                return True
    except Exception:
        pass

    try:
        gb = groebner([A, B], *free_vars, domain=domain)
        for poly in gb:
            if poly == 1 or poly == -1:
                return True
        if domain == 'QQ':
            if len(gb) == 1 and gb[0].is_number and gb[0] != 0:
                return True
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False, False]
        a, factors, u = witness
    except Exception:
        return [False, False, False]

    # H1
    h1_ok = False
    try:
        a_sym = sympify(a)
        if a_sym != 0:
            domain = get_domain([a_sym])
            free_vars = list(a_sym.free_symbols)
            if not free_vars:
                if domain == 'ZZ':
                    h1_ok = abs(int(a_sym)) != 1
                else:
                    h1_ok = False
            else:
                if domain == 'ZZ':
                    h1_ok = a_sym not in [1, -1]
                else:
                    h1_ok = not a_sym.is_number
    except Exception:
        h1_ok = False

    # H2
    h2_ok = False
    try:
        a_sym = sympify(a)
        u_sym = sympify(u)
        
        all_exprs = [a_sym, u_sym]
        for p, e in factors:
            all_exprs.append(sympify(p))
            
        domain = get_domain(all_exprs)
        
        free_vars = set()
        for expr in all_exprs:
            free_vars.update(expr.free_symbols)
        free_vars = list(free_vars)
        
        is_u_unit = False
        if domain == 'ZZ':
            is_u_unit = u_sym in [1, -1]
        else:
            is_u_unit = u_sym.is_number and u_sym != 0
            
        if is_u_unit:
            prod = u_sym
            factors_valid = True
            for p, e in factors:
                p_sym = sympify(p)
                e_sym = sympify(e)
                if not e_sym.is_Integer or e_sym < 1:
                    factors_valid = False
                    break
                if not is_prime_in_R(p_sym, free_vars, domain):
                    factors_valid = False
                    break
                prod *= p_sym**e_sym
                
            if factors_valid and expand(a_sym - prod) == 0:
                pairwise_non_assoc = True
                for i in range(len(factors)):
                    for j in range(i+1, len(factors)):
                        p1 = sympify(factors[i][0])
                        p2 = sympify(factors[j][0])
                        if are_associates(p1, p2, free_vars, domain):
                            pairwise_non_assoc = False
                            break
                    if not pairwise_non_assoc:
                        break
                if pairwise_non_assoc:
                    h2_ok = True
    except Exception:
        h2_ok = False

    # neg_Q
    neg_q = False
    try:
        a_sym = sympify(a)
        all_exprs = [a_sym]
        for p, e in factors:
            all_exprs.append(sympify(p))
            
        domain = get_domain(all_exprs)
        
        free_vars = set()
        for expr in all_exprs:
            free_vars.update(expr.free_symbols)
        free_vars = list(free_vars)
        
        if len(factors) > 1:
            all_comaximal = True
            for i in range(len(factors)):
                for j in range(i+1, len(factors)):
                    p1, e1 = factors[i]
                    p2, e2 = factors[j]
                    A = sympify(p1)**sympify(e1)
                    B = sympify(p2)**sympify(e2)
                    if not is_comaximal(A, B, free_vars, domain):
                        all_comaximal = False
                        break
                if not all_comaximal:
                    break
            if not all_comaximal:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]