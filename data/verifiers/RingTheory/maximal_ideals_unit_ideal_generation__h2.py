import math
import sympy
from sympy.combinatorics.named_groups import CyclicGroup

# Top-level setup: named object bindings that the witness expression may reference.
Z = "Z"
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)

def conditions(witness) -> list[bool]:
    try:
        n = None
        KNOWN_RINGS = {Z, ZZ, QQ, RR, CC, Z2, Z3, Z4, Z6}
        
        # Parse the witness to extract the ideal generator 'n' in Z,
        # or determine if the witness represents the whole ring (n = 1).
        if witness in KNOWN_RINGS:
            n = 1
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            r, m = witness
            if r == m:
                n = 1
            elif isinstance(m, int):
                n = m
            elif isinstance(r, int):
                n = r
            elif m in KNOWN_RINGS:
                n = 1
        elif isinstance(witness, (tuple, list)):
            for x in reversed(witness):
                if isinstance(x, int):
                    n = x
                    break
        elif isinstance(witness, int):
            n = witness
        else:
            try:
                n = int(witness)
            except Exception:
                pass
                
        if n is None:
            return [False, False]

        # H_1: R is a commutative ring with identity
        # We evaluate in Z (or assume the provided ring is commutative with identity)
        h1_ok = True
        
        n = abs(n)
        is_maximal = sympy.isprime(n)
        
        if n == 1:
            # M = R. R \ M is empty. Condition holds vacuously.
            condition_holds = True
        elif n == 0:
            # M = {0}. R \ M = R \ {0}. gcd(0, x) = |x| != 1 for |x| > 1.
            condition_holds = False
        else:
            # M = nZ. For x in Z \ nZ, we check if (n, x) = Z, i.e., gcd(n, x) == 1.
            # We only need to check x in 1 .. n-1.
            condition_holds = True
            for x in range(1, n):
                if math.gcd(n, x) != 1:
                    condition_holds = False
                    break
                    
        # The conclusion is the equivalence: M is maximal iff condition_holds.
        # neg_Q is True when this equivalence FAILS.
        neg_q_ok = (is_maximal != condition_holds)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: M is maximal iff for every x in R \\ M, (M, x) = R FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1