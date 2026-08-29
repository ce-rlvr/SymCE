import sympy
from sympy import Symbol, Poly

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (f, p, n) where:
      - f is a sympy expression representing the polynomial f(x)
      - p is the prime modulus
      - n is the integer bound on the number of solutions
    """
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            p = witness.get('p')
            n = witness.get('n')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            f, p, n = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        f = sympy.sympify(f)
    except Exception:
        pass

    # H1: p is a prime number
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False

    # H2: The leading coefficient of f(x) is not divisible by p
    try:
        poly = Poly(f, x)
        lc = poly.LC()
        h2 = bool(lc % p != 0)
    except Exception:
        h2 = False

    # neg_Q: The congruence f(x) \equiv 0 \pmod p has strictly MORE than n incongruent solutions modulo p
    try:
        if p > 100000:  # Prevent timeout for unreasonably large primes
            neg_q = False
        else:
            solutions = 0
            for i in range(int(p)):
                try:
                    val = f.subs(x, i)
                    if val % p == 0:
                        solutions += 1
                except Exception:
                    pass
            neg_q = bool(solutions > n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: The leading coefficient of f(x) is not divisible by p",
    "¬Q: The congruence f(x) \equiv 0 \pmod p has strictly more than n incongruent solutions modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2