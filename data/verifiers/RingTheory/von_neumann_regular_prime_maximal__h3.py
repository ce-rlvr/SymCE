import math

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: For every element a in R, there exists an element x in R such that a = (a^2) * x",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = int(witness.get('n', 0))
            P = witness.get('P', [])
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, P = witness
            n = int(n)
        else:
            return [False, False, False]
            
        if n < 2:
            return [False, False, False]
            
        if isinstance(P, int):
            P_set = set((P * i) % n for i in range(n))
        else:
            P_set = set(int(p) % n for p in P)
            
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    # We model the ring R as Z/nZ, which is commutative with identity for n >= 2.
    try:
        h1 = (n >= 2)
    except Exception:
        h1 = False

    # H_2: For every element a in R, there exists an element x in R such that a = (a^2) * x
    try:
        h2 = True
        for a in range(n):
            found = False
            for x in range(n):
                if (a**2 * x) % n == a:
                    found = True
                    break
            if not found:
                h2 = False
                break
    except Exception:
        h2 = False

    # ¬Q: P is not a maximal ideal of R
    try:
        is_ideal = True
        if not P_set:
            is_ideal = False
        else:
            # Check closure under addition
            for x in P_set:
                for y in P_set:
                    if (x + y) % n not in P_set:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
            # Check closure under multiplication by any ring element
            for x in P_set:
                for r in range(n):
                    if (x * r) % n not in P_set:
                        is_ideal = False
                        break
                if not is_ideal:
                    break
                    
        if not is_ideal:
            is_maximal = False
        elif len(P_set) == n:
            is_maximal = False  # The whole ring is not a proper ideal
        else:
            is_maximal = True
            # In Z/nZ, an ideal is maximal iff adding any element outside it generates the whole ring
            for x in range(n):
                if x not in P_set:
                    g = n
                    for p in P_set:
                        g = math.gcd(g, p)
                    g = math.gcd(g, x)
                    if g != 1:
                        is_maximal = False
                        break
        neg_q = not is_maximal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]