import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple or list: (a, u, p, e) or a dictionary with these keys,
    representing elements in the PID R = Z.
    - a: the integer element
    - u: the unit
    - p: list of prime factors
    - e: list of exponents
    """
    try:
        if isinstance(witness, dict):
            if not all(k in witness for k in ('a', 'u', 'p', 'e')):
                return [False, False, False]
            a = witness['a']
            u = witness['u']
            p = witness['p']
            e = witness['e']
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            a, u, p, e = witness
        else:
            return [False, False, False]
            
        # Ensure all elements are of correct type (integers)
        if type(a) is not int or type(u) is not int:
            return [False, False, False]
        if not (isinstance(p, (list, tuple)) and isinstance(e, (list, tuple))):
            return [False, False, False]
        if len(p) != len(e):
            return [False, False, False]
        if not (all(type(pi) is int for pi in p) and all(type(ei) is int for ei in e)):
            return [False, False, False]
            
        # H_1: R is a principal ideal domain
        # We restrict the witness to R = Z, which is always a PID.
        h1 = True
        
        # H_2: a = u * p_1^e_1 * ... * p_k^e_k is a prime factorization with u a unit 
        # and p_i pairwise non-associate primes.
        u_is_unit = (abs(u) == 1)
        p_are_primes = all(sympy.isprime(abs(pi)) for pi in p)
        
        # In Z, primes are associate iff their absolute values are equal
        abs_p = [abs(pi) for pi in p]
        pairwise_non_assoc = (len(abs_p) == len(set(abs_p)))
        
        # Check the product equality safely using Rational to handle potential negative exponents
        prod = sympy.Rational(u, 1)
        for pi, ei in zip(p, e):
            prod *= (sympy.Rational(pi, 1) ** ei)
        is_prod = (sympy.Rational(a, 1) == prod)
        
        h2 = u_is_unit and p_are_primes and pairwise_non_assoc and is_prod
        
        # Conclusion: The radical of the ideal (a) is the principal ideal (p_1 ... p_k)
        # Compute the generator of the radical of (a) in Z
        if a == 0:
            rad_a = 0
        else:
            rad_a = 1
            for prime_factor in sympy.primefactors(abs(a)):
                rad_a *= prime_factor
                
        # Compute the generator of the ideal (p_1 ... p_k)
        prod_p = 1
        for pi in p:
            prod_p *= pi
            
        # Two principal ideals in Z are equal iff their generators have the same absolute value
        q = (abs(rad_a) == abs(prod_p))
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a = u p_1^{e_1} ... p_k^{e_k} is a prime factorization with u a unit and p_i pairwise non-associate primes",
    "¬Q: The radical of the ideal (a) is not the principal ideal (p_1 ... p_k)"
]

N_HYP = 2
NEG_Q_INDEX = 2