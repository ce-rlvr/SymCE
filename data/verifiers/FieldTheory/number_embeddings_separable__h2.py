import sympy as sp
from sympy.abc import x, y, z, t, u, v

def conditions(witness):
    best_result = [False, False, False]
    
    try:
        if isinstance(witness, tuple):
            f = witness[0]
        else:
            f = witness
            
        if isinstance(f, str):
            f = sp.sympify(f)
            
        if isinstance(f, sp.Eq):
            f = f.lhs - f.rhs
            
        if isinstance(f, sp.Poly):
            f = f.as_expr()
            
        syms = list(f.free_symbols)
        if len(syms) < 2:
            return best_result
            
        primes_to_try = [2, 3, 5, 7, 11]
        if isinstance(witness, tuple):
            for item in witness[1:]:
                if isinstance(item, (int, sp.Integer)) and sp.isprime(item):
                    primes_to_try = [item]
                    break
                    
        for p in primes_to_try:
            for var in syms:
                param_list = [s for s in syms if s != var]
                if not param_list:
                    continue
                
                vars_list = [var] + param_list
                
                h1_local = False
                h2_local = False
                neg_q_local = False
                
                deg_var = sp.degree(f, var)
                if deg_var < 1:
                    continue
                    
                try:
                    c, factors = sp.factor_list(f, *vars_list, modulus=p)
                except Exception:
                    continue
                    
                if len(factors) == 1 and factors[0][1] == 1:
                    if sp.degree(factors[0][0], var) >= 1:
                        h1_local = True
                        h2_local = True
                        
                        df = sp.diff(f, var)
                        g = sp.gcd(f, df, *vars_list, modulus=p)
                        deg_g = sp.degree(g, var)
                        
                        if deg_g > 0:
                            neg_q_local = True
                            return [True, True, True]
                
                if h1_local and not best_result[0]:
                    best_result = [h1_local, h2_local, neg_q_local]
                    
    except Exception:
        pass
        
    return best_result

CONDITION_LABELS = [
    "H_1: E/K is a finite field extension",
    "H_2: C is an algebraically closed field containing K",
    "¬Q: There are not exactly degree distinct K-algebra homomorphisms from E into C"
]

N_HYP = 2
NEG_Q_INDEX = 2