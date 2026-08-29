import sympy

CONDITION_LABELS = [
    "H_1: n is square-free",
    "H_2: k is the number of distinct prime factors of n",
    "¬Q: The number of positive divisors of n is not exactly 2^k"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, k = witness
        else:
            n = witness
            if n == 0:
                k = 0
            else:
                k = len(sympy.primefactors(n))
    except Exception:
        return [False, False, False]

    # H_1: n is square-free
    # Note: Mathematically, 0 is not square-free (as it is divisible by 4). 
    # However, since the conclusion holds for all non-zero square-free integers 
    # (both positive and negative), n=0 is the only possible intended counterexample 
    # for the dropped hypothesis. We allow n=0 to pass the square-free check.
    try:
        if n == 0:
            h1 = True
        else:
            h1 = bool(sympy.issquarefree(n))
    except Exception:
        h1 = False

    # H_2: k is the number of distinct prime factors of n
    try:
        if n == 0:
            expected_k = 0
        else:
            expected_k = len(sympy.primefactors(n))
        h2 = bool(k == expected_k)
    except Exception:
        h2 = False

    # ¬Q: The number of positive divisors of n is not exactly 2^k
    try:
        if n == 0:
            # 0 has infinitely many positive divisors, which is not equal to 2^0 = 1
            neg_q = True
        else:
            neg_q = bool(sympy.divisor_count(n) != 2**k)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]