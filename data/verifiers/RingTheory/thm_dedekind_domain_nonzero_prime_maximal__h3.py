import sympy
from sympy.abc import x, y, z
from sympy import Rational, Integer, Poly

def conditions(witness):
    """
    Verifies that the witness is a counterexample to the false conjecture:
    "In a Dedekind domain, every prime ideal is maximal."
    (The true theorem requires the prime ideal to be non-zero).
    
    The witness is interpreted as the generator of a principal ideal.
    For example, witness = 0 represents the zero ideal in the ring of integers Z,
    which is a Dedekind domain.
    """
    h1_ok = False
    h2_ok = False
    neg_q = False

    # Unpack tuple if the witness is provided as (Ring, IdealGenerator)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            _, witness = witness
    except Exception:
        pass

    # Handle string inputs gracefully
    try:
        if isinstance(witness, str):
            witness = sympy.sympify(witness)
    except Exception:
        pass

    try:
        # Case 1: Ideal in the ring of integers Z (a PID, hence Dedekind)
        if isinstance(witness, (int, sympy.Integer)):
            n = abs(int(witness))
            h1_ok = True
            # In Z, an ideal (n) is prime iff n == 0 or n is prime
            h2_ok = (n == 0) or sympy.isprime(n)
            # In Z, an ideal (n) is maximal iff n is prime
            is_maximal = sympy.isprime(n)
            neg_q = not is_maximal

        # Case 2: Ideal in a polynomial ring like QQ[x] (a PID, hence Dedekind)
        elif isinstance(witness, (sympy.Expr, sympy.Poly)):
            if isinstance(witness, sympy.Poly):
                p = witness
                is_zero = p.is_zero
            else:
                is_zero = (witness == 0)
                if not is_zero:
                    p = sympy.Poly(witness)
            
            if is_zero:
                h1_ok = True
                h2_ok = True
                is_maximal = False
                neg_q = True
            else:
                # Restrict to univariate polynomials to ensure it's a PID
                if len(p.gens) <= 1:
                    h1_ok = True
                    if p.degree() > 0:
                        h2_ok = p.is_irreducible
                        is_maximal = p.is_irreducible
                    else:
                        # Units (non-zero constants) generate the whole ring, not prime/maximal
                        h2_ok = False
                        is_maximal = False
                    neg_q = not is_maximal
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Dedekind domain",
    "H_2: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2