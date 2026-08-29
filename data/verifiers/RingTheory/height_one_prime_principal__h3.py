import sympy
from sympy import sympify, Poly, ZZ, QQ, isprime, gcd
from sympy.polys.polytools import groebner
from sympy.abc import x, y, z

def to_expr(p):
    if hasattr(p, 'as_expr'):
        return p.as_expr()
    return sympify(p)

def is_prime_ideal(R, P_gens):
    P_gens = [p for p in P_gens if p != 0]
    if not P_gens:
        return True
        
    if R == ZZ:
        g = P_gens[0]
        for p in P_gens[1:]:
            g = gcd(g, p)
        return isprime(abs(int(g)))
        
    try:
        p_exprs = [to_expr(p) for p in P_gens]
        r_gens_exprs = [to_expr(g) for g in R.gens]
    except Exception:
        p_exprs = P_gens
        r_gens_exprs = []
        
    if len(p_exprs) == 1:
        p = p_exprs[0]
        if p.is_number:
            try:
                return isprime(abs(int(p)))
            except Exception:
                pass
        else:
            try:
                kwargs = {}
                if hasattr(R, 'domain'):
                    kwargs['domain'] = R.domain
                poly = Poly(p, *r_gens_exprs, **kwargs)
                if poly.is_irreducible:
                    return True
            except Exception:
                pass
                
    p_set = set(p_exprs)
    r_gens_set = set(r_gens_exprs)
    
    vars_in_gens = p_set.intersection(r_gens_set)
    constants_in_gens = p_set - r_gens_set
    
    if not constants_in_gens and vars_in_gens:
        return True
        
    if len(constants_in_gens) == 1 and vars_in_gens:
        c = list(constants_in_gens)[0]
        try:
            if c.is_number and isprime(abs(int(c))):
                return True
        except Exception:
            pass
            
    try:
        kwargs = {}
        if hasattr(R, 'domain'):
            kwargs['domain'] = R.domain
        gb = groebner(p_exprs, r_gens_exprs, **kwargs)
        gb_exprs = [to_expr(g) for g in gb]
        
        gb_set = set(gb_exprs)
        gb_vars = gb_set.intersection(r_gens_set)
        gb_consts = gb_set - r_gens_set
        
        if not gb_consts and gb_vars:
            return True
            
        if len(gb_consts) == 1 and gb_vars:
            c = list(gb_consts)[0]
            if c.is_number and isprime(abs(int(c))):
                return True
                
        if hasattr(R, 'domain') and getattr(R.domain, 'is_Field', False):
            all_linear = True
            for g in gb_exprs:
                try:
                    poly = Poly(g, *r_gens_exprs)
                    if poly.total_degree() != 1:
                        all_linear = False
                        break
                except Exception:
                    all_linear = False
                    break
            if all_linear and len(gb_exprs) > 0:
                return True
                
        if hasattr(R, 'domain') and R.domain == ZZ:
            primes = []
            linears = []
            others = []
            for g in gb_exprs:
                if g.is_number:
                    try:
                        if isprime(abs(int(g))):
                            primes.append(g)
                        else:
                            others.append(g)
                    except Exception:
                        others.append(g)
                else:
                    try:
                        poly = Poly(g, *r_gens_exprs)
                        if poly.total_degree() == 1:
                            linears.append(g)
                        else:
                            others.append(g)
                    except Exception:
                        others.append(g)
            if len(primes) == 1 and not others and linears:
                return True
                
    except Exception:
        pass
        
    return False

def is_principal_and_generated_by_prime(R, P_gens):
    P_gens = [p for p in P_gens if p != 0]
    
    if not P_gens:
        return False
        
    if R == ZZ:
        g = P_gens[0]
        for p in P_gens[1:]:
            g = gcd(g, p)
        return isprime(abs(int(g)))
        
    try:
        p_exprs = [to_expr(p) for p in P_gens]
        r_gens_exprs = [to_expr(g) for g in R.gens]
    except Exception:
        p_exprs = P_gens
        r_gens_exprs = []
        
    try:
        kwargs = {}
        if hasattr(R, 'domain'):
            kwargs['domain'] = R.domain
        gb = groebner(p_exprs, r_gens_exprs, **kwargs)
        if len(gb) == 1:
            g = gb[0]
            if g == 0:
                return False
            if g.is_number:
                try:
                    return isprime(abs(int(g)))
                except Exception:
                    return False
            else:
                try:
                    poly = Poly(g, *r_gens_exprs, **kwargs)
                    return poly.is_irreducible
                except Exception:
                    return False
        else:
            return False
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        R, P_gens = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_prime_ideal(R, P_gens))
    except Exception:
        h2 = False
        
    try:
        neg_q = not is_principal_and_generated_by_prime(R, P_gens)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: P is a prime ideal of R",
    "¬Q: P is not a principal ideal generated by a prime element"
]

N_HYP = 2
NEG_Q_INDEX = 2