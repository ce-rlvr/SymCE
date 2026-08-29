import sympy

# Top-level setup
# The conjecture is about elements in a ring R. 
# We will evaluate the conditions in the ring of integers Z.
# In Z, the conjecture fails if we consider the strict definition of prime factorization
# where primes are positive, but elements can be negative, leading to unit differences
# that are not captured by prime exponents alone.
# Wait, a divides b iff v_p(a) <= v_p(b) is actually TRUE in Z for all non-zero a, b.
# However, if the witness is in a polynomial ring or another domain, we can evaluate it.
# We will provide a general verifier for Z.

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (a, b), check the remaining hypotheses and the negated conclusion.
    """
    try:
        a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: a and b are non-zero elements in R
    try:
        h1 = (a != 0) and (b != 0)
    except Exception:
        h1 = False

    # H_2: For any prime element p in R, let v_p(x) denote the exponent of p in the unique prime factorization of x
    # This is a definitional hypothesis, which holds in UFDs like Z or Q[x].
    # We will verify that a and b have prime factorizations by checking they are integers or sympy expressions.
    try:
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            h2 = True
        elif hasattr(a, 'factor') and hasattr(b, 'factor'):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The element a divides b in R if and only if v_p(a) <= v_p(b) for all prime elements p in R.
    # We need to check if (a divides b) == (v_p(a) <= v_p(b) for all p) is FALSE.
    try:
        if isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)):
            a_int, b_int = int(a), int(b)
            divides = (b_int % a_int == 0)
            
            factors_a = sympy.factorint(abs(a_int))
            factors_b = sympy.factorint(abs(b_int))
            
            all_le = True
            primes = set(factors_a.keys()).union(set(factors_b.keys()))
            for p in primes:
                if factors_a.get(p, 0) > factors_b.get(p, 0):
                    all_le = False
                    break
            
            neg_q = not (divides == all_le)
        else:
            # For polynomials or other expressions
            a_sym, b_sym = sympy.sympify(a), sympy.sympify(b)
            q, r = sympy.div(b_sym, a_sym)
            divides = (r == 0)
            
            factors_a = sympy.factor_list(a_sym)[1]
            factors_b = sympy.factor_list(b_sym)[1]
            
            dict_a = {f: e for f, e in factors_a}
            dict_b = {f: e for f, e in factors_b}
            
            all_le = True
            bases = set(dict_a.keys()).union(set(dict_b.keys()))
            for base in bases:
                if dict_a.get(base, 0) > dict_b.get(base, 0):
                    all_le = False
                    break
            
            neg_q = not (divides == all_le)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements in R",
    "H_2: For any prime element p in R, let v_p(x) denote the exponent of p in the unique prime factorization of x",
    "¬Q: It is NOT the case that (a divides b iff v_p(a) <= v_p(b) for all prime elements p)"
]

N_HYP = 2
NEG_Q_INDEX = 2