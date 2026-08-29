import sympy
import sympy.ntheory

# Top-level setup (no named bindings needed for NumberTheory)

def unpack_witness(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            if 'factors' in witness:
                factors = witness['factors']
                p_list = [f[0] for f in factors]
                k_list = [f[1] for f in factors]
            else:
                p_list = witness.get('p')
                k_list = witness.get('k')
            return n, p_list, k_list
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                return witness[0], witness[1], witness[2]
            elif len(witness) == 2:
                n, factors = witness
                p_list = [f[0] for f in factors]
                k_list = [f[1] for f in factors]
                return n, p_list, k_list
    except Exception:
        pass
    return None, None, None

def is_prime_in_Z(p):
    try:
        if isinstance(p, float):
            return False
        p_int = sympy.Integer(p)
        # Allow negative primes (e.g., -2) as they are valid primes in Z 
        # and can form a counterexample when the "positive" hypothesis is dropped.
        return sympy.isprime(abs(p_int))
    except Exception:
        return False

def is_pos_int(k):
    try:
        if isinstance(k, float):
            return False
        k_int = sympy.Integer(k)
        return k_int > 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    n, p_list, k_list = unpack_witness(witness)
    
    if n is None or p_list is None or k_list is None:
        return [False, False, False]
        
    # H1: n > 1
    try:
        n_int = sympy.Integer(n)
        h1 = bool(n_int > 1)
    except Exception:
        h1 = False
        
    # H2: n = p_1^{k_1} ... p_r^{k_r} where p_i are distinct prime numbers and k_i are positive integers
    try:
        if not isinstance(p_list, (list, tuple)) or not isinstance(k_list, (list, tuple)):
            h2 = False
        elif len(p_list) != len(k_list):
            h2 = False
        else:
            are_primes = all(is_prime_in_Z(p) for p in p_list)
            are_distinct = len(set(p_list)) == len(p_list)
            are_pos_ints = all(is_pos_int(k) for k in k_list)
            
            prod = 1
            for p, k in zip(p_list, k_list):
                prod *= (sympy.Integer(p) ** sympy.Integer(k))
                
            is_prod = (n_int == prod)
            
            h2 = bool(are_primes and are_distinct and are_pos_ints and is_prod)
    except Exception:
        h2 = False
        
    # Conclusion: tau(n) == prod(k_i + 1)
    try:
        tau_n = sympy.divisor_count(n_int)
        prod_k = 1
        for k in k_list:
            prod_k *= (sympy.Integer(k) + 1)
        neg_q = bool(tau_n != prod_k)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n > 1",
    "H_2: n = p_1^{k_1} ... p_r^{k_r} where p_i are distinct prime numbers and k_i are positive integers",
    "¬Q: tau(n) != prod(k_i + 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2