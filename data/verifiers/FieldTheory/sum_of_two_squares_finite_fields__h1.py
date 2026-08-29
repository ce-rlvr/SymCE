import sympy

# Top-level setup
# (No specific named bindings needed for this FieldTheory/Number Theory conjecture.
# Witnesses are expected to be tuples of integers (q, a) or dicts.)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the field size (or ring size) `q` and the element `a`.
    """
    # H_1: a is an element of F_q
    try:
        if isinstance(witness, dict):
            q = witness['q']
            a = witness['a']
        else:
            q, a = witness
            
        q_val = int(q)
        a_val = int(a)
        h1 = (q_val >= 2) and (0 <= a_val < q_val)
    except Exception:
        h1 = False

    # ¬Q: a is NOT a sum of two squares in F_q
    # (Evaluated in Z_q, which is the ring used when the prime/prime-power hypothesis is dropped)
    try:
        if isinstance(witness, dict):
            q = witness['q']
            a = witness['a']
        else:
            q, a = witness
            
        q_val = int(q)
        a_val = int(a)
        
        # Precompute all squares modulo q
        squares = set((x * x) % q_val for x in range(q_val))
        
        # Check if there exist s1, s2 in squares such that (s1 + s2) % q == a
        is_sum = any(((a_val - s) % q_val) in squares for s in squares)
        
        neg_q = not is_sum
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of F_q",
    "¬Q: a is not a sum of two squares in F_q"
]

N_HYP = 1
NEG_Q_INDEX = 1