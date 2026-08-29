import sympy
import math

# Top-level setup
# (No named bindings needed for Number Theory; use integers directly)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness is expected to be a list of (prime, exponent) pairs, e.g., [(2, 1), (2, 1)],
    or a tuple (n, factors), or an object with .n and .factors attributes.
    """
    try:
        if hasattr(witness, 'n') and hasattr(witness, 'factors'):
            n = witness.n
            factors = witness.factors
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, factors = witness
        else:
            factors = witness
            
        if isinstance(factors, dict):
            factors = list(factors.items())
            
        # If n was not explicitly provided, compute it from the factors
        if not (hasattr(witness, 'n') or (isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int))):
            n = 1
            for p, a in factors:
                n *= int(p)**int(a)
    except Exception:
        return [False, False]

    # H_1: n = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k} is the prime factorization of n
    h1_ok = False
    try:
        prod_val = 1
        all_prime = True
        all_pos = True
        for p, a in factors:
            try:
                if int(p) != p or int(a) != a:
                    all_prime = False
                    all_pos = False
                    break
                p_val = int(p)
                a_val = int(a)
            except Exception:
                all_prime = False
                all_pos = False
                break
            
            prod_val *= p_val**a_val
            if not sympy.isprime(p_val):
                all_prime = False
            if a_val < 1:
                all_pos = False
                
        if n == prod_val and all_prime and all_pos:
            h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: \sigma(n) \neq \prod_{i=1}^k \frac{p_i^{a_i+1}-1}{p_i-1}
    neg_q_ok = False
    try:
        if h1_ok:
            actual_sigma = sympy.divisor_sigma(n)
            
            formula_val = 1
            for p, a in factors:
                p_val = int(p)
                a_val = int(a)
                formula_val *= (p_val**(a_val+1) - 1) // (p_val - 1)
                
            if actual_sigma != formula_val:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n = p_1^{a_1} p_2^{a_2} \\cdots p_k^{a_k} is the prime factorization of n",
    "¬Q: \\sigma(n) \\neq \\prod_{i=1}^k \\frac{p_i^{a_i+1}-1}{p_i-1}"
]

N_HYP = 1
NEG_Q_INDEX = 1