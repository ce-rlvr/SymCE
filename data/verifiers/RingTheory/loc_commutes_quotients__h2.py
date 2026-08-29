import math
import sympy
from sympy import symbols, Rational, Integer

# Top-level setup
# Witness format:
# A tuple (n, I_elements, S, S_bar) where:
# - n is an integer >= 2, representing the commutative ring R = Z_n
# - I_elements is a list of integers, representing the ideal I in Z_n
# - S is a list of integers, representing the subset S of Z_n
# - S_bar is a list of integers, representing the image of S in R/I

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            I_elements = witness.get('I')
            S = witness.get('S')
            S_bar = witness.get('S_bar')
        else:
            n, I_elements, S, S_bar = witness
            
        # H1: R is a commutative ring with identity
        h1 = isinstance(n, int) and n >= 2
        
        # H2: I is an ideal of R
        if not isinstance(I_elements, (list, set, tuple)) or len(I_elements) == 0:
            h2 = False
            I_set = set()
        else:
            h2 = True
            I_set = set()
            for x in I_elements:
                if not isinstance(x, int):
                    h2 = False
                    break
                I_set.add(x % n)
            
            if h2:
                # Check closure under addition and scalar multiplication
                for x in I_set:
                    for y in I_set:
                        if (x + y) % n not in I_set:
                            h2 = False
                    for r in range(n):
                        if (r * x) % n not in I_set:
                            h2 = False
                            
        # H3: \bar{S} is the image of S in the quotient ring R/I
        if h1 and h2 and isinstance(S, (list, set, tuple)) and isinstance(S_bar, (list, set, tuple)):
            def canonical(val):
                # Returns the minimum non-negative representative of the coset val + I
                return min((val + i) % n for i in I_set)
            
            expected_S_bar = set(canonical(s % n) for s in S)
            actual_S_bar = set(canonical(s % n) for s in S_bar)
            h3 = actual_S_bar == expected_S_bar
        else:
            h3 = False
            
        # ¬Q: The conclusion fails
        # The conclusion "The ring (S^{-1}R)/(S^{-1}I) is isomorphic to \bar{S}^{-1}(R/I)" fails 
        # if S^{-1}R is not a valid ring under standard fraction operations.
        # This happens exactly when S is empty or not multiplicatively closed (the dropped hypothesis).
        if h1 and isinstance(S, (list, set, tuple)):
            S_mod = set(s % n for s in S)
            is_mult_closed = len(S_mod) > 0 and all((s1 * s2) % n in S_mod for s1 in S_mod for s2 in S_mod)
            neg_q = not is_mult_closed
        else:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is an ideal of R",
    "H_3: \\bar{S} is the image of S in the quotient ring R/I",
    "¬Q: The ring (S^{-1}R)/(S^{-1}I) is not isomorphic to \\bar{S}^{-1}(R/I) (e.g., S^{-1}R is not a ring)"
]

N_HYP = 3
NEG_Q_INDEX = 3