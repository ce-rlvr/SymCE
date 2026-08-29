import sympy

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (n, m, f) representing:
      - R = Z_n (integers modulo n)
      - S = Z_m (integers modulo m)
      - f = a mapping from Z_n to Z_m (can be a dict, list, callable, or sympy expression)
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        n_raw, m_raw, f = witness
        
        try:
            n = int(n_raw)
        except Exception:
            try:
                n = len(n_raw)
            except Exception:
                n = None
                
        try:
            m = int(m_raw)
        except Exception:
            try:
                m = len(m_raw)
            except Exception:
                m = None
                
        if not (isinstance(n, int) and isinstance(m, int)):
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]

    def eval_f(x):
        if isinstance(f, dict):
            if x in f:
                return f[x]
            elif str(x) in f:
                return f[str(x)]
            else:
                raise KeyError(x)
        elif isinstance(f, (list, tuple)):
            return f[x]
        elif hasattr(f, 'subs') and hasattr(f, 'free_symbols'):
            symbols = list(f.free_symbols)
            if len(symbols) == 1:
                return int(f.subs(symbols[0], x))
            elif len(symbols) == 0:
                return int(f)
            else:
                raise ValueError("Expression has too many free symbols")
        else:
            return f(x)

    # H_1: R and S are commutative rings with identity
    # Z_n and Z_m are commutative rings with identity for n, m >= 2
    try:
        h1 = (n >= 2) and (m >= 2)
    except Exception:
        h1 = False

    # H_2: S is an integral domain
    # Z_m is an integral domain iff m is prime
    try:
        h2 = sympy.isprime(m)
    except Exception:
        h2 = False

    # H_3: f(1_R) = 1_S
    try:
        h3 = (eval_f(1) % m) == 1
    except Exception:
        h3 = False

    # ¬Q: The kernel of f is NOT a prime ideal of R
    try:
        K = set()
        for x in range(n):
            if (eval_f(x) % m) == 0:
                K.add(x)
        
        is_ideal = True
        if 0 not in K:
            is_ideal = False
        else:
            # Check closed under subtraction
            for a in K:
                for b in K:
                    if (a - b) % n not in K:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
            # Check closed under multiplication by any element in R
            if is_ideal:
                for a in K:
                    for r in range(n):
                        if (r * a) % n not in K:
                            is_ideal = False
                            break
                    if not is_ideal:
                        break
        
        # A prime ideal must be a proper ideal
        is_proper = is_ideal and (len(K) < n)
        
        is_prime = is_proper
        if is_prime:
            # Check prime condition: ab in K => a in K or b in K
            for a in range(n):
                for b in range(n):
                    if (a * b) % n in K:
                        if a not in K and b not in K:
                            is_prime = False
                            break
                if not is_prime:
                    break
        
        neg_q = not is_prime
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: S is an integral domain",
    "H_3: f(1_R) = 1_S",
    "¬Q: The kernel of f is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3