import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy import QQ, ZZ

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
O2 = zeros(2, 2)
I3 = eye(3)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness object, checks whether it is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1, H_2, H_3, H_4, neg_Q].
    """
    # 1. Try dictionary representation
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('P_is_prime', False))
            h2 = bool(witness.get('Q_is_P_primary', False))
            h3 = bool(witness.get('S_is_multiplicatively_closed', False))
            h4 = bool(witness.get('S_inter_P_is_empty', False))
            neg_q = not bool(witness.get('localized_Q_is_primary', True))
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    # 2. Try object with properties
    try:
        h1 = bool(witness.P_is_prime)
        h2 = bool(witness.Q_is_P_primary)
        h3 = bool(witness.S_is_multiplicatively_closed)
        h4 = bool(witness.S_inter_P_is_empty)
        neg_q = not bool(witness.localized_Q_is_primary)
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 3. Try object with methods
    try:
        h1 = bool(witness.is_prime_ideal(witness.P))
        h2 = bool(witness.is_P_primary(witness.Q, witness.P))
        h3 = bool(witness.is_multiplicatively_closed(witness.S))
        h4 = bool(witness.is_disjoint(witness.S, witness.P))
        neg_q = not bool(witness.localized_Q_is_primary(witness.Q, witness.P, witness.S))
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    # 4. Try tuple of lists (R, P, Q, S) representing a finite ring
    try:
        R, P, Q, S = witness
        
        def contains(lst, item):
            for x in lst:
                if x == item: return True
            return False

        def is_ideal(R, I):
            if not I: return False
            for x in I:
                if not contains(R, x): return False
                for y in I:
                    if not contains(I, x + y): return False
                for r in R:
                    if not contains(I, r * x): return False
                    if not contains(I, x * r): return False
            return True

        def is_prime_ideal(R, P):
            if not is_ideal(R, P): return False
            if len(P) == len(R): return False
            for a in R:
                if contains(P, a): continue
                for b in R:
                    if contains(P, b): continue
                    subset = True
                    for r in R:
                        if not contains(P, a * r * b):
                            subset = False
                            break
                    if subset: return False
            return True

        def is_P_primary(R, Q, P):
            if not is_ideal(R, Q): return False
            for x in Q:
                if not contains(P, x): return False
            for a in R:
                if contains(Q, a): continue
                for b in R:
                    if contains(P, b): continue
                    subset = True
                    for r in R:
                        if not contains(Q, a * r * b):
                            subset = False
                            break
                    if subset: return False
            return True

        def is_mult_closed(S):
            if not S: return False
            for x in S:
                for y in S:
                    if not contains(S, x * y): return False
            return True

        def is_disjoint(S, P):
            for x in S:
                if contains(P, x): return False
            return True

        h1 = is_prime_ideal(R, P)
        h2 = is_P_primary(R, Q, P)
        h3 = is_mult_closed(S)
        h4 = is_disjoint(S, P)

        # For non-commutative rings, localization requires the Ore condition.
        # If neither the right nor left Ore condition holds, S^{-1}R cannot be formed,
        # and thus the conclusion fails.
        right_ore = True
        for r in R:
            for s in S:
                found = False
                for r_prime in R:
                    for s_prime in S:
                        if r * s_prime == s * r_prime:
                            found = True
                            break
                    if found: break
                if not found:
                    right_ore = False
                    break
        
        left_ore = True
        for r in R:
            for s in S:
                found = False
                for r_prime in R:
                    for s_prime in S:
                        if s_prime * r == r_prime * s:
                            found = True
                            break
                    if found: break
                if not found:
                    left_ore = False
                    break

        neg_q = not (right_ore or left_ore)

        return [h1, h2, h3, h4, neg_q]
    except Exception:
        pass

    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: P is a prime ideal of R",
    "H_2: Q is a P-primary ideal of R",
    "H_3: S is a multiplicatively closed subset of R",
    "H_4: S \\cap P is the empty set",
    "¬Q: The extended ideal S^{-1}Q is not an S^{-1}P-primary ideal in S^{-1}R"
]

N_HYP = 4
NEG_Q_INDEX = 4