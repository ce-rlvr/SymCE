import sympy

# Top-level setup
x, y, z = sympy.symbols('x y z')

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: p is a prime element of R",
    "H_3: v_p(x) denotes the exponent of p in the prime factorization of an element x in R \\setminus {0}",
    "¬Q: The valuation map does not satisfy v_p(ab) = v_p(a) + v_p(b) (or is undefined)"
]

def conditions(witness):
    # Extract p, a, b from the witness
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            a = witness.get('a')
            b = witness.get('b')
            if p is None or a is None or b is None:
                return [False, False, False, False]
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                p, a, b = witness
            elif len(witness) == 4:
                _, p, a, b = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
        
        def is_int(val):
            if isinstance(val, int): 
                return True
            if hasattr(val, 'is_integer') and val.is_integer: 
                return True
            return False
            
        if not (is_int(p) and is_int(a) and is_int(b)):
            h1 = False
        else:
            p = int(p)
            a = int(a)
            b = int(b)
            # We restrict our verification to the ring of integers Z, which is a UFD.
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = h1 and sympy.isprime(abs(p))
    except Exception:
        h2 = False

    try:
        # This hypothesis is a definition that holds as long as we are in a valid ring setup.
        h3 = h1
    except Exception:
        h3 = False

    try:
        if not h1:
            neg_q = False
        else:
            def v_p(val, prime):
                if val == 0:
                    raise ValueError("v_p(0) is undefined")
                if abs(prime) <= 1:
                    raise ValueError("Invalid prime")
                count = 0
                while val % prime == 0:
                    count += 1
                    val //= prime
                return count
            
            val_ab = v_p(a * b, p)
            val_a = v_p(a, p)
            val_b = v_p(b, p)
            neg_q = not (val_ab == val_a + val_b)
    except Exception:
        # If evaluating v_p raises an exception (e.g., due to evaluating at 0),
        # the equation is undefined, meaning the conclusion fails.
        neg_q = True

    return [h1, h2, h3, neg_q]