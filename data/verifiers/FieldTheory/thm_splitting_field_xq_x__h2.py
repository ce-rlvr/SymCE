import sympy
from sympy import Symbol, factor_list, isprime
from sympy.abc import x

# Top-level setup
# For this theorem, the witness is expected to provide the field size (a prime p) and the exponent q.
# No additional named bindings are strictly necessary for FieldTheory here.

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (q, p) or a dictionary {'q': q, 'p': p},
    where p is a prime representing the finite field F = GF(p), and q is the exponent in x^q - x.
    """
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            p = witness.get('p', witness.get('F'))
        else:
            q, p = witness[:2]
            
        q = int(q)
        p = int(p)
    except Exception:
        return [False, False]

    # Hypothesis 1: F is a finite field
    # We verify this by checking if p is prime (restricting to prime fields for simplicity).
    # We also require q > 0 for x^q - x to be a valid polynomial.
    try:
        h1 = isprime(p) and q > 0
    except Exception:
        h1 = False

    # Conclusion: The polynomial x^q - x factors completely over F, 
    # and its roots are precisely the elements of F.
    try:
        if not h1:
            neg_q_ok = False
        else:
            # Prevent timeout on excessively large q
            if q > 500:
                neg_q_ok = False
            else:
                # Check if roots are precisely the elements of F
                roots = set()
                for a in range(p):
                    if (pow(a, q, p) - a) % p == 0:
                        roots.add(a)
                roots_precisely_F = (len(roots) == p)

                # Check if the polynomial factors completely over F (all irreducible factors have degree 1)
                factored = factor_list(x**q - x, modulus=p)
                factors_completely = all(f[0].as_poly(x).degree() == 1 for f in factored[1])

                conclusion = roots_precisely_F and factors_completely
                neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a finite field",
    "¬Q: The polynomial x^q - x does not factor completely over F, or its roots are not precisely the elements of F"
]

N_HYP = 1
NEG_Q_INDEX = 1