import math
from sympy.ntheory import primefactors, isprime

# Top-level setup
# (No specific named objects needed for this domain; witnesses are represented by integers and lists)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = abs(int(witness.get("n", 0)))
            I_gen = int(witness.get("I", 0))
            S = [int(s) for s in witness.get("S", [])]
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            n = abs(int(witness[0]))
            I_gen = int(witness[1])
            S = [int(s) for s in witness[2]]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a commutative ring
    # The witness represents the ring Z/nZ (or Z if n == 0), which is always commutative.
    h1 = True

    # H2: I is an ideal of R that is maximal with respect to the property of being disjoint from S
    h2 = False
    try:
        if n == 0:
            g = abs(I_gen)
        else:
            g = math.gcd(I_gen, n)
            
        if g == 0:
            disjoint = all(s != 0 for s in S)
        else:
            disjoint = all(s % g != 0 for s in S)
            
        if disjoint:
            if g == 0:
                # In Z, the zero ideal is contained in infinitely many ideals.
                # For it to be maximal disjoint from S, S would need to intersect every non-zero ideal,
                # which is impossible for a finite set S.
                maximal = False
            else:
                maximal = True
                # Check all ideals strictly containing I.
                # It is sufficient to check the maximal ideals containing I,
                # which correspond to generators d = g // p for each prime factor p of g.
                for p in primefactors(g):
                    d = g // p
                    intersects = any(s % d == 0 for s in S)
                    if not intersects:
                        maximal = False
                        break
            h2 = maximal
    except Exception:
        h2 = False

    # neg_Q: I is not a prime ideal of R
    neg_q = False
    try:
        if n == 0:
            is_prime_ideal = isprime(g) or g == 0
        else:
            is_prime_ideal = isprime(g)
        neg_q = not is_prime_ideal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R that is maximal with respect to the property of being disjoint from S",
    "¬Q: I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2