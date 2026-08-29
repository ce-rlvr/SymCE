import itertools

# Expected witness format:
# A dictionary representing finite rings as products of Z/nZ.
# {
#     'R': [n1, n2, ...],  # moduli for R (e.g., [2] for Z/2Z)
#     'S': [m1, m2, ...],  # moduli for S (e.g., [2, 2] for Z/2Z x Z/2Z)
#     'f': { (x1, x2, ...): (y1, y2, ...), ... }, # map from R to S
#     'P': [(x1, x2, ...), ...] # elements of the prime ideal P in R
# }

def add(x, y, moduli):
    return tuple((a + b) % m for a, b, m in zip(x, y, moduli))

def mul(x, y, moduli):
    return tuple((a * b) % m for a, b, m in zip(x, y, moduli))

def neg(x, moduli):
    return tuple((-a) % m for a, m in zip(x, moduli))

def zero(moduli):
    return tuple(0 for _ in moduli)

def one(moduli):
    return tuple(1 % m for m in moduli)

def elements(moduli):
    return list(itertools.product(*[range(m) for m in moduli]))

def is_ideal(I, moduli):
    if not I:
        return False
    I_set = set(I)
    R_elems = set(elements(moduli))
    if not I_set.issubset(R_elems):
        return False
    z = zero(moduli)
    if z not in I_set:
        return False
    # closed under subtraction
    for x in I:
        for y in I:
            if add(x, neg(y, moduli), moduli) not in I_set:
                return False
    # closed under scalar multiplication
    for r in R_elems:
        for x in I:
            if mul(r, x, moduli) not in I_set:
                return False
    return True

def is_prime_ideal(I, moduli):
    if not is_ideal(I, moduli):
        return False
    I_set = set(I)
    R_elems = elements(moduli)
    if len(I_set) == len(R_elems):
        return False # must be proper
    for x in R_elems:
        for y in R_elems:
            if mul(x, y, moduli) in I_set:
                if x not in I_set and y not in I_set:
                    return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R_mod = witness.get('R')
            S_mod = witness.get('S')
            f_map = witness.get('f')
            P_elems = witness.get('P')
        else:
            R_mod = getattr(witness, 'R', None)
            S_mod = getattr(witness, 'S', None)
            f_map = getattr(witness, 'f', None)
            P_elems = getattr(witness, 'P', None)
            
        if R_mod is None or S_mod is None or f_map is None or P_elems is None:
            return [False, False, False]
            
        if not R_mod or not S_mod:
            return [False, False, False]

        if isinstance(f_map, dict):
            f = lambda x: f_map[x]
        else:
            f = f_map
            
        # H1: R and S are commutative rings with identity, f is a ring homomorphism
        h1_ok = False
        try:
            if all(isinstance(m, int) and m >= 1 for m in R_mod) and \
               all(isinstance(m, int) and m >= 1 for m in S_mod):
                
                R_elems = elements(R_mod)
                S_elems = set(elements(S_mod))
                
                is_hom = True
                for x in R_elems:
                    if f(x) not in S_elems:
                        is_hom = False
                        break
                
                if is_hom and f(one(R_mod)) == one(S_mod):
                    for x in R_elems:
                        for y in R_elems:
                            if f(add(x, y, R_mod)) != add(f(x), f(y), S_mod):
                                is_hom = False
                            if f(mul(x, y, R_mod)) != mul(f(x), f(y), S_mod):
                                is_hom = False
                    h1_ok = is_hom
        except Exception:
            h1_ok = False

        # H2: P is a prime ideal of R such that ker(f) subseteq P
        h2_ok = False
        try:
            if is_prime_ideal(P_elems, R_mod):
                P_set = set(P_elems)
                ker_subset = True
                z_S = zero(S_mod)
                for x in elements(R_mod):
                    if f(x) == z_S and x not in P_set:
                        ker_subset = False
                        break
                h2_ok = ker_subset
        except Exception:
            h2_ok = False

        # Q: The image f(P) is a prime ideal of S
        neg_q_ok = False
        try:
            fP = [f(x) for x in P_elems]
            is_Q = is_prime_ideal(fP, S_mod)
            neg_q_ok = not is_Q
        except Exception:
            neg_q_ok = False

        return [h1_ok, h2_ok, neg_q_ok]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity, and f is a ring homomorphism from R to S",
    "H_2: P is a prime ideal of R such that ker(f) is a subset of P",
    "¬Q: The image f(P) is not a prime ideal of S"
]

N_HYP = 2
NEG_Q_INDEX = 2