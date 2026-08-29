import sympy

# Top-level setup
# The witness is expected to be a tuple: (P_gen, Q_gen, S_list)
# representing the generators of ideals P and Q in the ring of integers Z,
# and a list of integers representing the subset S.

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 5
        P_gen, Q_gen, S_list = witness
        
        P_gen = abs(int(P_gen))
        Q_gen = abs(int(Q_gen))
        
        S_list = list(S_list)
        if len(S_list) > 1000:
            return [False] * 5
        S_list = [int(s) for s in S_list]
    except Exception:
        return [False] * 5

    # H_1: R is a commutative ring
    # We interpret the witness in the context of R = Z, which is a commutative ring.
    h1 = True

    # H_2: P is a prime ideal of R
    try:
        h2 = (P_gen == 0) or sympy.isprime(P_gen)
    except Exception:
        h2 = False

    # H_3: Q is a P-primary ideal of R
    try:
        h3 = False
        if P_gen == 0:
            h3 = (Q_gen == 0)
        else:
            if Q_gen > 0:
                temp = Q_gen
                k = 0
                while temp % P_gen == 0:
                    temp //= P_gen
                    k += 1
                if temp == 1 and k >= 1:
                    h3 = True
    except Exception:
        h3 = False

    # H_4: S \cap P is the empty set
    try:
        h4 = True
        for s in S_list:
            if P_gen == 0:
                if s == 0:
                    h4 = False
                    break
            else:
                if s % P_gen == 0:
                    h4 = False
                    break
    except Exception:
        h4 = False

    # ¬Q: S^{-1}Q is not an S^{-1}P-primary ideal in S^{-1}R
    # The dropped hypothesis from the true theorem is that S must be a multiplicatively closed subset.
    # If S is not multiplicatively closed, the standard construction of the ring of fractions S^{-1}R fails,
    # meaning S^{-1}R is not a valid ring and the conclusion fails.
    try:
        is_mult_closed = True
        if 1 not in S_list:
            is_mult_closed = False
        else:
            for s1 in S_list:
                for s2 in S_list:
                    if s1 * s2 not in S_list:
                        is_mult_closed = False
                        break
                if not is_mult_closed:
                    break
        neg_q = not is_mult_closed
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: P is a prime ideal of R",
    "H_3: Q is a P-primary ideal of R",
    "H_4: S \\cap P is the empty set",
    "¬Q: S^{-1}Q is not an S^{-1}P-primary ideal in S^{-1}R (e.g., S is not multiplicatively closed)"
]

N_HYP = 4
NEG_Q_INDEX = 4