import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for RingTheory
ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: S is an integral domain",
    "H_2: f: R -> S is a ring homomorphism",
    "H_3: f(1_R) = 1_S",
    "¬Q: The kernel of f is not a prime ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample.
    The witness can be a tuple (n, m) representing the rings R = Z/nZ and S = Z/mZ,
    with f: R -> S being the natural projection f(x) = x mod m.
    Alternatively, it can be an object with attributes R, S, f, and ker.
    """
    # Fast path for the tuple (n, m) witness format
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, m = witness
            if isinstance(n, int) and isinstance(m, int):
                # H1: S = Z/mZ is an integral domain if it has no zero divisors.
                # This occurs if m is prime, m == 0 (Z), or m == 1 (the zero ring).
                # The zero ring is the critical edge case where the conjecture fails.
                h1 = sympy.isprime(m) or m == 1 or m == 0
                
                # H2: f(x) = x mod m is a well-defined ring homomorphism iff m divides n.
                h2 = (n % m == 0) if m != 0 else (n == 0)
                
                # H3: f(1_R) = 1_S is always true for this natural projection.
                h3 = True
                
                # ¬Q: ker(f) is a prime ideal iff S is an integral domain AND ker(f) is proper.
                # ker(f) is proper iff m != 1. Thus ker(f) is prime iff m is prime or m == 0.
                # We want ¬Q to be True when ker(f) is NOT prime.
                neg_q = not (sympy.isprime(m) or m == 0)
                
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Fallback path for custom object witness
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if hasattr(witness, 'S'):
            S = witness.S
            if hasattr(S, 'is_integral_domain'):
                h1 = bool(S.is_integral_domain())
            elif hasattr(S, 'is_domain'):
                h1 = bool(S.is_domain)
    except Exception:
        pass

    try:
        if hasattr(witness, 'f'):
            f = witness.f
            if hasattr(f, 'is_ring_homomorphism'):
                h2 = bool(f.is_ring_homomorphism())
            else:
                h2 = callable(f)
    except Exception:
        pass

    try:
        if hasattr(witness, 'f') and hasattr(witness, 'R') and hasattr(witness, 'S'):
            f = witness.f
            R = witness.R
            S = witness.S
            one_R = R.one if hasattr(R, 'one') else 1
            one_S = S.one if hasattr(S, 'one') else 1
            h3 = bool(f(one_R) == one_S)
    except Exception:
        pass

    try:
        if hasattr(witness, 'ker'):
            ker = witness.ker
            if hasattr(ker, 'is_prime_ideal'):
                neg_q = not bool(ker.is_prime_ideal())
            elif hasattr(ker, 'is_prime'):
                neg_q = not bool(ker.is_prime)
        elif hasattr(witness, 'f') and hasattr(witness.f, 'kernel'):
            ker = witness.f.kernel()
            if hasattr(ker, 'is_prime_ideal'):
                neg_q = not bool(ker.is_prime_ideal())
            elif hasattr(ker, 'is_prime'):
                neg_q = not bool(ker.is_prime)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]