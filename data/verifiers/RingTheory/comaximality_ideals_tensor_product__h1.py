import math
import sympy
from sympy.abc import x, y, z

# Top-level setup
# The witness is expected to be a tuple of integers (m, n, a, b)
# representing rings A = Z/mZ, B = Z/nZ and ideals I = aA, J = bA.
# Alternatively, a dictionary with boolean flags is accepted.

CONDITION_LABELS = [
    "H_1: A and B are commutative R-algebras",
    "H_2: I and J are ideals of A",
    "H_3: I + J = A",
    "¬Q: The extended ideals I \\otimes_R B and J \\otimes_R B are not comaximal in A \\otimes_R B"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # Support dictionary witness as a fallback
        if isinstance(witness, dict):
            keys_h1 = ["H_1", "h1", "A_and_B_are_commutative_R_algebras"]
            keys_h2 = ["H_2", "h2", "I_and_J_are_ideals_of_A"]
            keys_h3 = ["H_3", "h3", "I_plus_J_equals_A"]
            keys_neg_q = ["neg_Q", "neg_q", "extended_ideals_are_not_comaximal"]
            
            if any(k in witness for k in keys_h1 + keys_h2 + keys_h3 + keys_neg_q) or "extended_ideals_are_comaximal" in witness:
                h1 = any(bool(witness.get(k, False)) for k in keys_h1)
                h2 = any(bool(witness.get(k, False)) for k in keys_h2)
                h3 = any(bool(witness.get(k, False)) for k in keys_h3)
                neg_q = any(bool(witness.get(k, False)) for k in keys_neg_q)
                if not neg_q and "extended_ideals_are_comaximal" in witness:
                    neg_q = not bool(witness["extended_ideals_are_comaximal"])
                return [h1, h2, h3, neg_q]

        # Primary witness format: tuple (m, n, a, b)
        if not (isinstance(witness, tuple) and len(witness) == 4):
            return [False, False, False, False]
        
        m, n, a, b = witness
        
        if not all(isinstance(val, int) for val in witness):
            return [False, False, False, False]

        # H_1: A and B are commutative R-algebras
        # Z/mZ and Z/nZ are always commutative Z-algebras
        h1 = True
        
        # H_2: I and J are ideals of A
        # aA and bA are always ideals of A
        h2 = True
        
        # H_3: I + J = A
        # In Z/mZ, aA + bA = A iff gcd(a, b, m) == 1
        if m == 0:
            h3 = (math.gcd(a, b) == 1)
        else:
            h3 = (math.gcd(math.gcd(a, b), m) == 1)
            
        # ¬Q: The extended ideals I \otimes_R B and J \otimes_R B are not comaximal
        # This happens if the map I \otimes B -> A \otimes B is not injective (so I \otimes B is not an ideal),
        # or if A \otimes B = 0 (so the only ideal is 0, which is not proper).
        if m == 0:
            not_ideal = (n != 0 and (math.gcd(a, n) > 1 or math.gcd(b, n) > 1))
        else:
            not_ideal = False
            
        tensor_zero = (m != 0 and n != 0 and math.gcd(m, n) == 1)
        
        neg_q = not_ideal or tensor_zero
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]