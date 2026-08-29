import sympy

def is_prime_power(q):
    if not isinstance(q, int) or q < 2:
        return False
    f = sympy.factorint(q)
    return len(f) == 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the parameters (q, n, m) or (q, m).
    """
    try:
        # Extract parameters from the witness
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            m = witness.get('m')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                q, n, alpha, m = witness
            elif len(witness) == 3:
                if isinstance(witness[1], int):
                    q, n, m = witness
                else:
                    q, alpha, m = witness
                    n = sympy.n_order(q, m) if m > 1 else 1
            elif len(witness) == 2:
                q, m = witness
                n = sympy.n_order(q, m) if m > 1 else 1
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if q is None or m is None:
            return [False, False, False]
            
        if n is None:
            n = sympy.n_order(q, m) if m > 1 else 1

        # H_1: F_q is a finite field with q elements
        # This is true if and only if q is a prime power.
        h1 = is_prime_power(q)
        
        # H_2: \alpha is a non-zero element of F_{q^n} with multiplicative order m
        # Such an element exists if and only if m divides the order of the multiplicative group of F_{q^n}.
        h2 = isinstance(n, int) and n >= 1 and isinstance(m, int) and m >= 1 and (q**n - 1) % m == 0
        
        # Conclusion: The smallest positive integer k such that \alpha^{q^k} = \alpha 
        # is equal to the multiplicative order of q modulo m.
        # Note: \alpha^{q^k} = \alpha  <=>  \alpha^{q^k - 1} = 1  <=>  m | q^k - 1
        if not h2:
            neg_q = False
        else:
            if m == 1:
                # The multiplicative order of q modulo 1 is undefined, 
                # while the smallest k such that 1 | q^k - 1 is k = 1.
                # Thus, they cannot be equal.
                neg_q = True
            else:
                k = 1
                while (q**k - 1) % m != 0:
                    k += 1
                expected = sympy.n_order(q, m)
                neg_q = (k != expected)
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: \\alpha is a non-zero element of F_{q^n} with multiplicative order m",
    "¬Q: The smallest positive integer k such that \\alpha^{q^k} = \\alpha is NOT equal to the multiplicative order of q modulo m"
]

N_HYP = 2
NEG_Q_INDEX = 2