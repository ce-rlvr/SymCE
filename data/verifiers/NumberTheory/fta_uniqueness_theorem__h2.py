import sympy
import math
import itertools
import functools

# Top-level setup for witness evaluation
# No specific named groups or matrices are needed for this Number Theory conjecture.

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    
    Expected witness format:
    A tuple/list (n, p_list, q_list) or a dict/object with these attributes.
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            p_list = list(witness['p_list'])
            q_list = list(witness['q_list'])
        elif hasattr(witness, 'n') and hasattr(witness, 'p_list') and hasattr(witness, 'q_list'):
            n = witness.n
            p_list = list(witness.p_list)
            q_list = list(witness.q_list)
        else:
            n, p_list, q_list = witness
            p_list = list(p_list)
            q_list = list(q_list)
    except Exception:
        return [False, False, False]

    # H_1: n is an integer greater than 1
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h1 = False

    # H_2: n = q_1 q_2 ... q_s where each q_j is a prime number
    try:
        prod_q = 1
        for q in q_list:
            prod_q *= q
        h2 = (prod_q == n) and all(sympy.isprime(q) for q in q_list)
    except Exception:
        h2 = False

    # ¬Q: It is not the case that r = s and p_i = q_i after reordering
    try:
        if len(p_list) != len(q_list):
            neg_q = True
        else:
            try:
                neg_q = sorted(p_list) != sorted(q_list)
            except TypeError:
                # Fallback if elements are not comparable
                neg_q = False
                for x in p_list:
                    if p_list.count(x) != q_list.count(x):
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: n = q_1 q_2 ... q_s where each q_j is a prime number",
    "¬Q: It is not the case that r = s and p_i = q_i after reordering"
]

N_HYP = 2
NEG_Q_INDEX = 2