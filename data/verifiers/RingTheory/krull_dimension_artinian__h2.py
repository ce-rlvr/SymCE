import sympy
from sympy import Integer

# Top-level setup: named object bindings that the witness expression may reference.
# We represent the ring Z/nZ using a simple wrapper class.
class ZnZ:
    def __init__(self, n):
        self.n = n

# The trivial ring (Z/1Z) is the unique counterexample, as its Krull dimension is -\infty (not 0).
ZeroRing = ZnZ(1)
TrivialRing = ZnZ(1)
Z1 = ZnZ(1)

# Other common rings for testing
Z2 = ZnZ(2)
Z3 = ZnZ(3)
Z4 = ZnZ(4)
Z = ZnZ(0)  # Represents the integers Z

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "Every commutative Artinian ring has Krull dimension zero."
    
    The dropped hypothesis from the true theorem is that the ring must be NON-ZERO.
    The trivial ring (zero ring) has Krull dimension -\infty, which is not zero.
    """
    try:
        n = None
        if hasattr(witness, 'n'):
            n = witness.n
        elif isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            
        if n is not None:
            if n == 1:
                # Trivial ring Z/1Z: commutative, Artinian, Krull dim = -\infty != 0
                return [True, True, True]
            elif n > 1:
                # Z/nZ for n > 1: commutative, Artinian, Krull dim = 0
                return [True, True, False]
            elif n == 0:
                # Z: commutative, NOT Artinian, Krull dim = 1 != 0
                return [True, False, True]
            elif n < 0:
                return [False, False, False]
                
        # Fallback for string-based witnesses
        if isinstance(witness, str):
            w_str = witness.strip().lower()
            if w_str in ["z/1z", "0", "{0}", "trivial", "trivial ring", "z1", "zeroring"]:
                return [True, True, True]
                
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "¬Q: The Krull dimension of R is not zero"
]

N_HYP = 2
NEG_Q_INDEX = 2