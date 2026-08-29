import sympy

CONDITION_LABELS = [
    "H_1: a is an integer",
    "¬Q: The difference a/n - sum(a_i/p_i^{e_i}) cannot be made an integer for any integers a_i"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide values for 'a' and 'n', e.g., as a tuple (a, n) or a dict.
    """
    a, n = None, None
    if isinstance(witness, dict):
        a = witness.get('a')
        n = witness.get('n')
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        a, n = witness
    else:
        try:
            a = witness.a
            n = witness.n
        except Exception:
            pass

    # H_1: a is an integer
    try:
        if a is None:
            h1_ok = False
        else:
            a_sym = sympy.sympify(a)
            h1_ok = bool(a_sym.is_integer)
    except Exception:
        h1_ok = False

    # ¬Q: The conclusion fails at the witness
    try:
        if a is None or n is None:
            q_ok = False
        else:
            a_sym = sympy.sympify(a)
            n_sym = sympy.sympify(n)
            
            # If n is not an integer, the prime factorization p_i^{e_i} is undefined.
            if not n_sym.is_integer:
                q_ok = False
            # If n is 0, division by zero occurs, so the expression is undefined.
            elif n_sym == 0:
                q_ok = False
            else:
                # If n is a non-zero integer, by the Chinese Remainder Theorem and Bezout's identity,
                # the map (a_1, ..., a_k) -> sum(a_i * (n / p_i^{e_i})) mod n is surjective onto Z/nZ.
                # Thus, we can always find integers a_i such that a/n - sum(a_i/p_i^{e_i}) is an integer,
                # provided that 'a' itself is an integer.
                q_ok = bool(a_sym.is_integer)
                
        neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = True

    return [h1_ok, neg_q_ok]