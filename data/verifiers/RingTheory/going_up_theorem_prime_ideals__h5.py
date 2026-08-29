import sympy
from sympy import ZZ, isprime

# Top-level setup
# We expose ZZ so the witness can easily reference it.
# A typical witness would be (ZZ, ZZ, 0, 3, 5) representing R, S, P1, P2, Q1.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            S = witness.get('S', ZZ)
            P1 = witness.get('P1')
            P2 = witness.get('P2')
            Q1 = witness.get('Q1')
        else:
            if len(witness) == 5:
                R, S, P1, P2, Q1 = witness
            elif len(witness) == 3:
                R, S = ZZ, ZZ
                P1, P2, Q1 = witness
            else:
                return [False] * 5
                
        if R == 'ZZ': R = ZZ
        if S == 'ZZ': S = ZZ
        
        def extract_gen(I):
            if isinstance(I, (list, tuple, set)) and len(I) == 1:
                return list(I)[0]
            return I
        
        P1 = extract_gen(P1)
        P2 = extract_gen(P2)
        Q1 = extract_gen(Q1)
        
        # Convert to int if they are sympy Integers or similar
        P1 = int(P1)
        P2 = int(P2)
        Q1 = int(Q1)
        
    except Exception:
        return [False] * 5

    # H1: R and S are commutative rings with identity
    try:
        h1 = (R == ZZ and S == ZZ)
    except Exception:
        h1 = False

    # H2: R is a subring of S
    try:
        h2 = (R == ZZ and S == ZZ)
    except Exception:
        h2 = False

    # H3: S is an integral extension of R
    try:
        h3 = (R == ZZ and S == ZZ)
    except Exception:
        h3 = False

    # H4: P1 and P2 are prime ideals of R such that P1 is a subset of P2
    try:
        if R == ZZ:
            p1_prime = (P1 == 0 or isprime(abs(P1)))
            p2_prime = (P2 == 0 or isprime(abs(P2)))
            # In ZZ, ideal(P1) is a subset of ideal(P2) iff P2 divides P1
            if P2 == 0:
                subset = (P1 == 0)
            else:
                subset = (P1 % P2 == 0)
            h4 = p1_prime and p2_prime and subset
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: There does NOT exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and Q2 \cap R = P2
    try:
        if S == ZZ and R == ZZ:
            # In ZZ, Q2 \cap R = P2 implies Q2 = P2.
            # So we only need to check if Q1 is a subset of P2.
            # If Q1 is a subset of P2, then Q2 = P2 satisfies the condition, so neg_Q is False.
            # If Q1 is NOT a subset of P2, then no such Q2 exists, so neg_Q is True.
            if P2 == 0:
                q1_subset_p2 = (Q1 == 0)
            else:
                q1_subset_p2 = (Q1 % P2 == 0)
            neg_q = not q1_subset_p2
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is a subring of S",
    "H_3: S is an integral extension of R",
    "H_4: P1 and P2 are prime ideals of R such that P1 is a subset of P2",
    "¬Q: There does not exist a prime ideal Q2 of S such that Q1 is a subset of Q2 and Q2 \\cap R = P2"
]

N_HYP = 4
NEG_Q_INDEX = 4