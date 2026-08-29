import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If p is a prime number, the sum of all mutually incongruent primitive roots 
    modulo p is congruent to \mu(p-1) modulo p."
    """
    try:
        p = int(witness)
    except Exception:
        return [False, False]

    # Hypothesis 1: p is a prime number
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False

    # Conclusion: The sum of all mutually incongruent primitive roots modulo p 
    # is congruent to \mu(p-1) modulo p.
    try:
        if not h1:
            neg_q = False
        else:
            # Find all mutually incongruent primitive roots modulo p
            # We check integers in the range [1, p-1]
            primitive_roots = []
            for i in range(1, p):
                if sympy.ntheory.is_primitive_root(i, p):
                    primitive_roots.append(i)
            
            sum_roots = sum(primitive_roots)
            mu_val = sympy.mobius(p - 1)
            
            # The conclusion states that sum_roots is congruent to mu_val modulo p
            q = (sum_roots % p) == (mu_val % p)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The sum of all mutually incongruent primitive roots modulo p is NOT congruent to \mu(p-1) modulo p"
]

N_HYP = 1
NEG_Q_INDEX = 1