import sympy
import math

def conditions(witness) -> list[bool]:
    """
    Checks if the given witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a dictionary or tuple containing:
      a: int
      b: int
      p: list of ints (the prime factors)
      e: list of ints (exponents for a)
      f: list of ints (exponents for b)
    """
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            p = witness['p']
            e = witness['e']
            f = witness['f']
        else:
            a, b, p, e, f = witness
            
        # Ensure a and b are strictly integers (and not booleans)
        if not (isinstance(a, int) and isinstance(b, int) and not isinstance(a, bool) and not isinstance(b, bool)):
            return [False, False, False]
            
        p = list(p)
        e = list(e)
        f = list(f)
    except Exception:
        return [False, False, False]
        
    # H_1: p_1, ..., p_r is the set of all distinct prime factors dividing either a or b
    h1_ok = False
    try:
        if a != 0 and b != 0:
            pos_primes_a = sympy.primefactors(a)
            pos_primes_b = sympy.primefactors(b)
            expected_abs_primes = set(pos_primes_a) | set(pos_primes_b)
            
            actual_abs_primes = set()
            all_primes = True
            for q in p:
                if not (isinstance(q, int) and not isinstance(q, bool)):
                    all_primes = False
                    break
                if not sympy.isprime(abs(q)):
                    all_primes = False
                    break
                actual_abs_primes.add(abs(q))
                
            # Check that p contains exactly one associate for each prime factor, and no duplicates
            if all_primes and actual_abs_primes == expected_abs_primes and len(set(p)) == len(p) and len(p) == len(expected_abs_primes):
                h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: a = prod p_i^e_i and b = prod p_i^f_i where e_i >= 0 and f_i >= 0 are integers
    h2_ok = False
    try:
        if len(p) == len(e) and len(p) == len(f):
            valid_exponents = True
            for ei, fi in zip(e, f):
                if not (isinstance(ei, int) and not isinstance(ei, bool)) or not (isinstance(fi, int) and not isinstance(fi, bool)):
                    valid_exponents = False
                    break
                if ei < 0 or fi < 0 or ei > 10000 or fi > 10000:
                    valid_exponents = False
                    break
            if valid_exponents:
                prod_a = 1
                for qi, ei in zip(p, e):
                    prod_a *= (qi ** ei)
                prod_b = 1
                for qi, fi in zip(p, f):
                    prod_b *= (qi ** fi)
                if a == prod_a and b == prod_b:
                    h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: gcd(a, b) != prod p_i^min(e_i, f_i)
    neg_q_ok = False
    try:
        g = math.gcd(a, b)
        prod_gcd = 1
        for qi, ei, fi in zip(p, e, f):
            prod_gcd *= (qi ** min(ei, fi))
        if g != prod_gcd:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p_1, ..., p_r is the set of all distinct prime factors dividing either a or b",
    "H_2: a = prod p_i^e_i and b = prod p_i^f_i where e_i >= 0 and f_i >= 0 are integers",
    "¬Q: gcd(a, b) is not equal to prod p_i^min(e_i, f_i)"
]

N_HYP = 2
NEG_Q_INDEX = 2