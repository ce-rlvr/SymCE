import sympy
from sympy.abc import x, y, z, t, u, v
from sympy.ntheory import factorint
import itertools

# Top-level setup
# Standard symbols are provided for polynomial ring witnesses.
# The verifier handles monomial ideals in any number of variables,
# and treats integer primes as variables to support rings like Z[x].

def extract_generators(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            if hasattr(witness[0], 'gens') or isinstance(witness[0], str) or hasattr(witness[0], 'domain'):
                if isinstance(witness[1], (list, tuple, set)):
                    return list(witness[1])
        if isinstance(witness, (list, tuple, set)):
            return list(witness)
    except Exception:
        pass
    return None

def get_monomial_factors(expr):
    try:
        expr = sympy.sympify(expr)
        num, den = sympy.fraction(expr)
        if den != 1: 
            return None
        
        if getattr(expr, 'is_Integer', False):
            val = int(expr)
            if val == 0:
                return None
            return factorint(abs(val))
        elif getattr(expr, 'is_Symbol', False):
            return {expr: 1}
        elif getattr(expr, 'is_Pow', False):
            base, exp = expr.args
            if getattr(base, 'is_Symbol', False) and getattr(exp, 'is_Integer', False) and exp > 0:
                return {base: int(exp)}
            return None
        elif getattr(expr, 'is_Mul', False):
            res = {}
            for arg in expr.args:
                f = get_monomial_factors(arg)
                if f is None: 
                    return None
                for k, val in f.items():
                    res[k] = res.get(k, 0) + val
            return res
        return None
    except Exception:
        return None

def is_monomial_ideal(I_gens):
    factors_list = []
    for g in I_gens:
        try:
            if sympy.sympify(g) == 0:
                continue
        except Exception:
            pass
        f = get_monomial_factors(g)
        if f is None: 
            return None
        factors_list.append(f)
    return factors_list

def get_minimal_generators(factors_list):
    unique_factors = []
    for f in factors_list:
        if f not in unique_factors:
            unique_factors.append(f)
            
    minimal = []
    for i, f in enumerate(unique_factors):
        is_multiple = False
        for j, m in enumerate(unique_factors):
            if i != j:
                # f is a multiple of m if it contains all prime factors of m to at least the same power
                if all(f.get(k, 0) >= m.get(k, 0) for k in m.keys()):
                    is_multiple = True
                    break
        if not is_multiple:
            minimal.append(f)
    return minimal

def check_monomial_ideal_product_of_primes(minimal_gens, V):
    if not minimal_gens:
        return False
        
    degrees = [sum(f.values()) for f in minimal_gens]
    # A necessary condition for a monomial ideal to be a product of prime ideals
    # is that all its minimal generators have the exact same total degree.
    if len(set(degrees)) > 1:
        return False
        
    k = degrees[0]
    if k == 1:
        return True
        
    prime_ideals = []
    for r in range(1, len(V) + 1):
        for subset in itertools.combinations(V, r):
            prime_ideals.append(subset)
            
    matches = 0
    for combo in itertools.combinations_with_replacement(prime_ideals, k):
        prod_gens = []
        for vars_tuple in itertools.product(*combo):
            f = {}
            for var in vars_tuple:
                f[var] = f.get(var, 0) + 1
            if f not in prod_gens:
                prod_gens.append(f)
        prod_minimal = get_minimal_generators(prod_gens)
        
        if len(prod_minimal) == len(minimal_gens):
            match = True
            for m in minimal_gens:
                if m not in prod_minimal:
                    match = False
                    break
            if match:
                matches += 1
                
    return matches == 1

def conditions(witness):
    try:
        gens = extract_generators(witness)
        if gens is None:
            return [False, False]
            
        is_nonzero = any(sympy.sympify(g) != 0 for g in gens)
        
        factors_list = is_monomial_ideal(gens)
        if factors_list is None:
            # Fallback: if the ideal is not a monomial ideal (or equivalent in Z[x]),
            # we cannot easily verify its prime factorization properties.
            return [False, False]
            
        minimal_gens = get_minimal_generators(factors_list)
        
        # An ideal is proper if it does not contain 1 (represented by the empty factor dict)
        is_proper = {} not in minimal_gens
        
        H1 = bool(is_nonzero and is_proper)
        
        if not H1:
            return [H1, False]
            
        V = set()
        for f in minimal_gens:
            V.update(f.keys())
            
        is_prod = check_monomial_ideal_product_of_primes(minimal_gens, V)
        neg_Q = not is_prod
        
        return [H1, bool(neg_Q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a proper non-zero ideal of R",
    "¬Q: I cannot be uniquely expressed as a product of prime ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1