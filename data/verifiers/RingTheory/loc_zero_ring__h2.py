import sympy

# Top-level setup: named object bindings that the witness expression may reference.
# We represent the ring Z/nZ simply by the integer n (with 0 representing Z).
Z = 0
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z7 = 7
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample.
    The witness is expected to be a tuple (n, S) where:
      - n is an integer representing the commutative ring Z/nZ (n=0 means Z).
      - S is a list/set/tuple of integers representing the subset S.
    """
    # H_1: R is a commutative ring with identity
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            h1_ok = False
        else:
            n, S = witness
            if not isinstance(n, (int, sympy.Integer)):
                h1_ok = False
            elif not isinstance(S, (list, set, tuple)):
                h1_ok = False
            else:
                h1_ok = all(isinstance(s, (int, sympy.Integer)) for s in S)
    except Exception:
        h1_ok = False

    # ¬Q: The localized ring S^{-1}R is the zero ring if and only if 0 \in S (must FAIL)
    # This means (S^{-1}R is the zero ring) != (0 \in S in the ring R)
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            n, S = witness
            n = int(n)
            S = [int(s) for s in S]
            
            if n == 0:
                # In Z, 0 is in S iff the integer 0 is in S
                has_zero = 0 in S
                # In Z, S^-1 Z is the zero ring iff 0 is in the multiplicative closure of S,
                # which only happens if 0 is in S.
                zero_ring = 0 in S
            else:
                n = abs(n)
                # In Z/nZ, 0 is in S iff any element in S is 0 mod n
                has_zero = any(s % n == 0 for s in S)
                
                if n == 1:
                    # Z/1Z is the zero ring, so any localization is the zero ring
                    zero_ring = True
                else:
                    # Compute the multiplicative closure of S in Z/nZ
                    closure = {1}
                    queue = [1]
                    S_mod = [s % n for s in S]
                    
                    # BFS to find all elements in the multiplicative closure
                    while queue and len(closure) < n + 1:
                        curr = queue.pop(0)
                        for s in S_mod:
                            nxt = (curr * s) % n
                            if nxt not in closure:
                                closure.add(nxt)
                                queue.append(nxt)
                                
                    # S^-1 R is the zero ring iff 0 is in the multiplicative closure of S
                    zero_ring = 0 in closure
                    
            neg_q_ok = bool(zero_ring != has_zero)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: (S^{-1}R is the zero ring) is NOT equivalent to (0 \\in S)"
]

N_HYP = 1
NEG_Q_INDEX = 1