import sympy

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness):
    try:
        a, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: p is an odd prime
    try:
        h1 = bool(sympy.isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False
        
    # H2: a is not divisible by p
    try:
        h2 = bool(a % p != 0)
    except Exception:
        h2 = False
        
    # neg_Q: The number of solutions to x^2 = a mod p is not 1 + (a/p)
    try:
        if not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            p_int = int(p)
            sols = 0
            for x in range(p_int):
                try:
                    if (x**2 - a) % p_int == 0:
                        sols += 1
                except Exception:
                    pass
            
            # Check if 'a' is an integer or integer-like.
            # If 'a' is not an integer (e.g., a rational or float), the Legendre symbol 
            # is undefined and the formula 1 + (a/p) is invalid, making the conclusion false.
            try:
                if a == int(a):
                    a_int = int(a)
                    is_int_like = True
                else:
                    is_int_like = False
            except Exception:
                is_int_like = False
                
            if not is_int_like:
                neg_q = True
            else:
                expected = 1 + sympy.jacobi_symbol(a_int, p_int)
                neg_q = bool(sols != expected)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is not divisible by p",
    "¬Q: The congruence x^2 ≡ a (mod p) does not have exactly 1 + (a/p) incongruent solutions modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2