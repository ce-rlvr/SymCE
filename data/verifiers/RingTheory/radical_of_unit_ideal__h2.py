import sympy

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def divides(a, b):
    if isinstance(a, sympy.Integer):
        a = int(a)
    if isinstance(b, sympy.Integer):
        b = int(b)
        
    if isinstance(a, int) and isinstance(b, int):
        if a == 0:
            return b == 0
        return b % a == 0
    else:
        try:
            # Try division over integers first to be strict about coefficients
            q, r = sympy.div(b, a, domain='ZZ')
            return r == 0
        except Exception:
            try:
                # Fallback to default domain (usually a field)
                q, r = sympy.div(b, a)
                return r == 0
            except Exception:
                return False

def radical_contains(i, r):
    if isinstance(i, sympy.Integer):
        i = int(i)
    if isinstance(r, sympy.Integer):
        r = int(r)
        
    if isinstance(i, int) and isinstance(r, int):
        if i == 0:
            return r == 0
        if i in (1, -1):
            return True
        if r == 0:
            return True
        factors_i = sympy.factorint(abs(i))
        factors_r = sympy.factorint(abs(r))
        return all(p in factors_r for p in factors_i)
    else:
        try:
            if i == 0:
                return r == 0
            factors_i = sympy.factor_list(i)
            factors_r = sympy.factor_list(r)
            
            const_i = factors_i[0]
            const_r = factors_r[0]
            
            # Check constant factors if they are integers
            if isinstance(const_i, sympy.Integer) and isinstance(const_r, sympy.Integer):
                if not radical_contains(int(const_i), int(const_r)):
                    return False
                
            primes_i = [f[0] for f in factors_i[1]]
            primes_r = [f[0] for f in factors_r[1]]
            
            # Every irreducible factor of i must divide some irreducible factor of r
            for pi in primes_i:
                if not any(divides(pi, pr) for pr in primes_r):
                    return False
            return True
        except Exception:
            return False

def conditions(witness):
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False, False]
        r, i = witness
        if isinstance(r, str):
            r = sympy.sympify(r)
        if isinstance(i, str):
            i = sympy.sympify(i)
    except Exception:
        return [False, False, False]
    
    # H_1: R is a commutative ring
    # We interpret the witness (r, i) as generators for principal ideals rZ and iZ (or rZ[x] and iZ[x]).
    # Any integer or polynomial generates a commutative ring (possibly without identity).
    try:
        if isinstance(r, sympy.Integer):
            r = int(r)
        if isinstance(i, sympy.Integer):
            i = int(i)
            
        valid_r = isinstance(r, int) or isinstance(r, sympy.Expr)
        valid_i = isinstance(i, int) or isinstance(i, sympy.Expr)
        is_comm_ring = valid_r and valid_i
    except Exception:
        is_comm_ring = False

    # H_2: The radical of I is equal to R
    # This requires I to be an ideal of R (so r divides i)
    # and the radical of I in R to be R (so i divides r^n for some n)
    try:
        is_ideal = divides(r, i)
        rad_eq_R = is_ideal and radical_contains(i, r)
    except Exception:
        rad_eq_R = False

    # ¬Q: I != R
    # I = R if and only if they generate the same ideal (r divides i and i divides r)
    try:
        I_eq_R = divides(r, i) and divides(i, r)
        neg_q = not I_eq_R
    except Exception:
        neg_q = False

    return [is_comm_ring, rad_eq_R, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The radical of I is equal to R",
    "¬Q: I != R"
]

N_HYP = 2
NEG_Q_INDEX = 2