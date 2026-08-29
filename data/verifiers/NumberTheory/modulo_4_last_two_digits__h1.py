import sympy
import math
import itertools
import functools

# No special named bindings needed for this number theory conjecture.

CONDITION_LABELS = [
    "H_1: n = \\sum_{i=0}^k d_i 10^i is the decimal representation of n, with d_i \\in {0, 1, ..., 9} for all i",
    "¬Q: n \\equiv 10d_1 + d_0 \\pmod 4 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        # The witness can be provided as a tuple (n, d) or just the integer n.
        if isinstance(witness, tuple) and len(witness) == 2:
            n, d = witness
        elif isinstance(witness, list) and len(witness) == 2 and isinstance(witness[0], int) and isinstance(witness[1], list):
            n, d = witness[0], witness[1]
        else:
            n = witness
            if isinstance(n, int) and not isinstance(n, bool) and n >= 0:
                # Construct the 0-indexed decimal representation (d_0 is the units digit)
                d = [int(x) for x in reversed(str(n))]
            else:
                d = None
                
        if isinstance(n, int) and isinstance(d, list):
            if all(isinstance(di, int) and 0 <= di <= 9 for di in d):
                if n == sum(di * (10**i) for i, di in enumerate(d)):
                    # Must be the standard decimal representation (no leading zeros unless n=0)
                    if len(d) > 0:
                        if len(d) == 1 or d[-1] != 0:
                            h1 = True
    except Exception:
        h1 = False

    try:
        if isinstance(d, list):
            if len(d) >= 2:
                # If d_1 and d_0 are defined, evaluate the congruence
                q = (n % 4) == ((10 * d[1] + d[0]) % 4)
            else:
                # If the number has fewer than 2 digits, d_1 is undefined,
                # making the conclusion mathematically invalid/false.
                q = False
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]