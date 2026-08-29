import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: S is an integral extension of R",
    "H_3: P1 and P2 are prime ideals of R such that P1 is a subset of P2",
    "H_4: Q1 is a prime ideal of S such that the intersection of Q1 and R is equal to P1",
    "¬Q: There does not exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and the intersection of Q2 and R is equal to P2"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    # Handle dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('h1', False))
            h2 = bool(witness.get('h2', False))
            h3 = bool(witness.get('h3', False))
            h4 = bool(witness.get('h4', False))
            neg_q = not bool(witness.get('conclusion', True))
            return [h1, h2, h3, h4, neg_q]
        except Exception:
            pass

    # Handle tuple or object witness
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            R, S, P1, P2, Q1 = witness
        else:
            R = witness.R
            S = witness.S
            P1 = witness.P1
            P2 = witness.P2
            Q1 = witness.Q1
    except Exception:
        return [False, False, False, False, False]

    def get_bool(obj, attr):
        val = getattr(obj, attr)
        return val() if callable(val) else val

    # H_1: R and S are commutative rings with identity
    try:
        h1 = bool(get_bool(R, 'is_commutative') and get_bool(R, 'has_identity') and 
                  get_bool(S, 'is_commutative') and get_bool(S, 'has_identity'))
    except Exception:
        h1 = False

    # H_2: S is an integral extension of R
    try:
        if hasattr(S, 'is_integral_extension'):
            val = S.is_integral_extension
            h2 = bool(val(R) if callable(val) else val)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: P1 and P2 are prime ideals of R such that P1 is a subset of P2
    try:
        p1_prime = P1.is_prime_ideal(R) if callable(getattr(P1, 'is_prime_ideal', None)) else P1.is_prime_ideal
        p2_prime = P2.is_prime_ideal(R) if callable(getattr(P2, 'is_prime_ideal', None)) else P2.is_prime_ideal
        subset = P1.issubset(P2) if callable(getattr(P1, 'issubset', None)) else P1.issubset
        h3 = bool(p1_prime and p2_prime and subset)
    except Exception:
        h3 = False

    # H_4: Q1 is a prime ideal of S such that the intersection of Q1 and R is equal to P1
    try:
        q1_prime = Q1.is_prime_ideal(S) if callable(getattr(Q1, 'is_prime_ideal', None)) else Q1.is_prime_ideal
        intersect = Q1.intersection(R)
        if callable(intersect): 
            intersect = intersect()
        h4 = bool(q1_prime and intersect == P1)
    except Exception:
        h4 = False

    # ¬Q: There does not exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and Q2 \cap R = P2
    try:
        if hasattr(S, 'has_prime_ideal_over'):
            val = S.has_prime_ideal_over(Q1, R, P2)
            conclusion = bool(val() if callable(val) else val)
        elif hasattr(S, 'prime_ideals'):
            ideals = S.prime_ideals() if callable(S.prime_ideals) else S.prime_ideals
            conclusion = False
            for Q2 in ideals:
                subset_q = Q1.issubset(Q2) if callable(getattr(Q1, 'issubset', None)) else Q1.issubset
                intersect_q = Q2.intersection(R)
                if callable(intersect_q): 
                    intersect_q = intersect_q()
                if subset_q and intersect_q == P2:
                    conclusion = True
                    break
        else:
            # If we cannot determine the ideals, we cannot verify the negation of the conclusion
            conclusion = True 
            
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]