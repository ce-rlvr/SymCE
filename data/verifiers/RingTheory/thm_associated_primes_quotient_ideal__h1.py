import sympy
from sympy.ntheory import factorint

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z, t = sympy.symbols('x y z t')

def get_ass_primes(val, is_int_domain):
    """
    Computes the associated primes of the cyclic module R/(val).
    If is_int_domain is True, we work in Z.
    Otherwise, we work in a polynomial ring over a field (e.g., Q[x]).
    """
    if is_int_domain:
        n = int(val)
        if n == 0:
            return {0}
        n = abs(n)
        if n == 1:
            return set()
        return set(factorint(n).keys())
    else:
        val = sympy.sympify(val)
        if val == 0:
            return {0}
        try:
            # factor_list returns (constant, [(factor1, mult1), ...])
            factors = sympy.factor_list(val)[1]
            res = set()
            for f, mult in factors:
                if f.is_constant():
                    continue
                res.add(sympy.expand(f))
            return res
        except Exception:
            return set()

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the conjecture.
    The witness is expected to represent two ideals I and J in a PID (like Z or k[x]).
    It can be provided as a tuple (I, J) or (R, I, J).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, i, j = witness
            elif len(witness) == 2:
                i, j = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # Determine if the domain is Z or a polynomial ring
    is_int = False
    try:
        int(i)
        int(j)
        is_int = True
    except Exception:
        pass

    # H_1: I and J are ideals of R
    # In our supported domains (Z or k[x]), any element generates an ideal.
    h1 = True
    
    # H_2: I is a subset of J
    try:
        if is_int:
            i_val = int(i)
            j_val = int(j)
            if j_val == 0:
                h2 = (i_val == 0)
            else:
                h2 = (i_val % j_val == 0)
        else:
            i_sym = sympy.sympify(i)
            j_sym = sympy.sympify(j)
            if j_sym == 0:
                h2 = (i_sym == 0)
            else:
                try:
                    h2 = (sympy.rem(i_sym, j_sym) == 0)
                except Exception:
                    # Fallback for multivariate or complex expressions
                    frac = sympy.cancel(i_sym / j_sym)
                    h2 = (frac.as_numer_denom()[1] == 1)
    except Exception:
        h2 = False
        
    # ¬Q: The set of associated primes of J/I is NOT a subset of the set of associated primes of R/I
    try:
        if not h2:
            neg_q = False
        else:
            if is_int:
                i_val = int(i)
                j_val = int(j)
                ann_JI = 0 if j_val == 0 else i_val // j_val
                ann_RI = i_val
            else:
                i_sym = sympy.sympify(i)
                j_sym = sympy.sympify(j)
                if j_sym == 0:
                    ann_JI = 0
                else:
                    try:
                        ann_JI = sympy.quo(i_sym, j_sym)
                    except Exception:
                        ann_JI = sympy.cancel(i_sym / j_sym)
                ann_RI = i_sym
                
            ass_JI = get_ass_primes(ann_JI, is_int)
            ass_RI = get_ass_primes(ann_RI, is_int)
            
            neg_q = not ass_JI.issubset(ass_RI)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I is a subset of J",
    "¬Q: The set of associated primes of the R-module J/I is not a subset of the set of associated primes of the R-module R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2