import sympy

class Zn:
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return f"Z{self.n}"

# Standard finite rings Z_n
Z2 = Zn(2)
Z3 = Zn(3)
Z4 = Zn(4)
Z5 = Zn(5)
Z6 = Zn(6)
Z8 = Zn(8)
Z10 = Zn(10)
Z12 = Zn(12)

def get_all_ideals(n):
    ideals = []
    for d in range(1, n + 1):
        if n % d == 0:
            ideal = set((d * k) % n for k in range(n // d))
            ideals.append(ideal)
    return ideals

def is_ideal(n, P):
    if not P:
        return False
    if 0 not in P:
        return False
    for a in P:
        for b in P:
            if (a - b) % n not in P:
                return False
    for a in P:
        for r in range(n):
            if (r * a) % n not in P:
                return False
    return True

def is_prime_ideal(n, P):
    if not is_ideal(n, P):
        return False
    if len(P) == n:
        return False
    for a in range(n):
        if a in P:
            continue
        for b in range(n):
            if b in P:
                continue
            if (a * b) % n in P:
                return False
    return True

def is_minimal_prime_ideal(n, P):
    if not is_prime_ideal(n, P):
        return False
    ideals = get_all_ideals(n)
    for I in ideals:
        if I != P and I.issubset(P):
            if is_prime_ideal(n, I):
                return False
    return True

def satisfies_condition(n, P):
    for x in P:
        found_y = False
        for y in range(n):
            if y in P:
                continue
            x_pow = x % n
            for n_pow in range(1, n + 1):
                if (y * x_pow) % n == 0:
                    found_y = True
                    break
                x_pow = (x_pow * x) % n
            if found_y:
                break
        if not found_y:
            return False
    return True

def conditions(witness):
    try:
        R, P = witness
        if isinstance(R, Zn):
            n = R.n
        else:
            n = int(R)
            
        if n < 2 or n > 100:
            return [False, False]
            
        P_set = set()
        for x in P:
            x_int = int(x)
            if not (0 <= x_int < n):
                return [False, False]
            P_set.add(x_int)
            
        # H_1: R is a commutative ring with identity
        # Z_n for n >= 2 is always a commutative ring with identity
        h1 = True
        
        # Evaluate the conclusion
        is_min_prime = is_minimal_prime_ideal(n, P_set)
        cond = satisfies_condition(n, P_set)
        
        # The conclusion is the iff statement
        conclusion = (is_min_prime == cond)
        
        # We want the conclusion to fail
        neg_q = not conclusion
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: P is a minimal prime ideal iff condition holds (fails)"
]
N_HYP = 1
NEG_Q_INDEX = 1