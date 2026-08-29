import itertools

# Top-level setup
# (No specific named objects required for this domain; witnesses are expected to provide their own finite ring structures)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            S = witness['S']
            R = witness['R']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            one = witness['one']
            Q = witness['Q']
            P = witness['P']
        else:
            S = witness.S
            R = witness.R
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            Q = witness.Q
            P = witness.P
    except Exception:
        return [False] * 5

    def is_ideal(I, Ring):
        if not set(I).issubset(set(Ring)): return False
        if zero not in I: return False
        for a in I:
            for b in I:
                if add(a, b) not in I: return False
        for a in I:
            inv_in_I = False
            for b in I:
                if add(a, b) == zero:
                    inv_in_I = True
                    break
            if not inv_in_I: return False
        for a in I:
            for r in Ring:
                if mul(a, r) not in I: return False
                if mul(r, a) not in I: return False
        return True

    def is_maximal(I, Ring):
        if not is_ideal(I, Ring): return False
        if set(I) == set(Ring): return False
        for size in range(len(I) + 1, len(Ring)):
            for subset in itertools.combinations(Ring, size):
                if set(I).issubset(set(subset)):
                    if is_ideal(subset, Ring):
                        return False
        return True

    def check_H1():
        if zero not in S or one not in S: return False
        for a in S:
            for b in S:
                if add(a, b) not in S: return False
                if mul(a, b) not in S: return False
        for a in S:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            inv_found = False
            for b in S:
                if add(a, b) == zero:
                    inv_found = True
                    break
            if not inv_found: return False
            for b in S:
                if add(a, b) != add(b, a): return False
                if mul(a, b) != mul(b, a): return False
                for c in S:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
        
        if zero not in R or one not in R: return False
        for a in R:
            for b in R:
                if add(a, b) not in R: return False
                if mul(a, b) not in R: return False
        for a in R:
            if add(a, zero) != a or add(zero, a) != a: return False
            if mul(a, one) != a or mul(one, a) != a: return False
            inv_found = False
            for b in R:
                if add(a, b) == zero:
                    inv_found = True
                    break
            if not inv_found: return False
            for b in R:
                if add(a, b) != add(b, a): return False
                if mul(a, b) != mul(b, a): return False
                for c in R:
                    if add(add(a, b), c) != add(a, add(b, c)): return False
                    if mul(mul(a, b), c) != mul(a, mul(b, c)): return False
                    if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
        return True

    def check_H2():
        if not set(R).issubset(set(S)): return False
        for a in R:
            for b in R:
                if add(a, b) not in R: return False
                if mul(a, b) not in R: return False
        return True

    def check_H3():
        for s in S:
            is_integral = False
            for deg in range(1, len(S) + 1):
                for coeffs in itertools.product(R, repeat=deg):
                    val = one
                    for _ in range(deg):
                        val = mul(val, s)
                    term_val = zero
                    for i, c in enumerate(coeffs):
                        temp = c
                        for _ in range(i):
                            temp = mul(temp, s)
                        term_val = add(term_val, temp)
                    if add(val, term_val) == zero:
                        is_integral = True
                        break
                if is_integral:
                    break
            if not is_integral:
                return False
        return True

    def check_H4():
        if not is_ideal(Q, S): return False
        expected_P = [x for x in Q if x in R]
        return set(P) == set(expected_P)

    def check_neg_Q():
        q_max = is_maximal(Q, S)
        p_max = is_maximal(P, R)
        return q_max != p_max

    try:
        h1 = bool(check_H1())
    except Exception:
        h1 = False

    try:
        h2 = bool(check_H2())
    except Exception:
        h2 = False

    try:
        h3 = bool(check_H3())
    except Exception:
        h3 = False

    try:
        h4 = bool(check_H4())
    except Exception:
        h4 = False

    try:
        nq = bool(check_neg_Q())
    except Exception:
        nq = False

    return [h1, h2, h3, h4, nq]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "H_4: Q is an ideal of S and P = Q \\cap R",
    "¬Q: Q is a maximal ideal of S iff P is a maximal ideal of R is FALSE"
]

N_HYP = 4
NEG_Q_INDEX = 4