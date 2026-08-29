import itertools

# Top-level setup
S3 = None
Z4 = None
I2 = None

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    The conjecture is:
    Hypothesis: {P_i} is a non-empty family of prime ideals of R totally ordered under set inclusion.
    Conclusion: The intersection \bigcap P_i is a prime ideal of R.
    """
    try:
        # Support for mock objects or custom classes
        if hasattr(witness, 'is_chain_of_prime_ideals'):
            h1 = bool(witness.is_chain_of_prime_ideals())
            q = bool(witness.intersection_is_prime_ideal())
            return [h1, not q]
    except Exception:
        pass

    try:
        # Support for finite rings represented by tables or elements
        if len(witness) == 4:
            R_size, add_table, mul_table, P_list = witness
            R = list(range(R_size))
            def add(a, b): return add_table[a][b]
            def mul(a, b): return mul_table[a][b]
            def neg(a):
                for x in R:
                    if add(a, x) == add_table[0][0]:
                        return x
                return a
            zero = add_table[0][0]
        elif len(witness) == 2:
            R, P_list = witness
            R = list(R)
            def add(a, b): return a + b
            def mul(a, b): return a * b
            def neg(a): return -a
            zero = None
            for z in R:
                if all(add(z, a) == a for a in R):
                    zero = z
                    break
            if zero is None:
                return [False, False]
        else:
            return [False, False]

        def is_ideal(P):
            if not P: 
                return False
            if zero not in P: 
                return False
            for a in P:
                for b in P:
                    if add(a, neg(b)) not in P: 
                        return False
            for a in P:
                for r in R:
                    if mul(a, r) not in P: 
                        return False
                    if mul(r, a) not in P: 
                        return False
            return True

        def is_prime_ideal(P):
            if not is_ideal(P): 
                return False
            if set(P) == set(R): 
                return False
            # Definition of prime ideal: a * R * b \subseteq P implies a \in P or b \in P
            for a in R:
                for b in R:
                    if all(mul(mul(a, r), b) in P for r in R):
                        if a not in P and b not in P:
                            return False
            return True

        # Check Hypothesis 1: non-empty family of prime ideals, totally ordered
        if not P_list:
            h1 = False
        else:
            h1 = True
            for P in P_list:
                if not is_prime_ideal(P):
                    h1 = False
                    break
            if h1:
                for P1 in P_list:
                    for P2 in P_list:
                        s1 = set(P1)
                        s2 = set(P2)
                        if not (s1.issubset(s2) or s2.issubset(s1)):
                            h1 = False
                            break

        # Check Conclusion: intersection is a prime ideal
        if not P_list:
            intersection = []
        else:
            intersection = set(P_list[0])
            for P in P_list[1:]:
                intersection = intersection.intersection(set(P))
            intersection = list(intersection)

        q = is_prime_ideal(intersection)
        neg_q = not q

        return [h1, neg_q]

    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: {P_i} is a non-empty family of prime ideals of R that is totally ordered under set inclusion",
    "¬Q: The intersection of the family is not a prime ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1