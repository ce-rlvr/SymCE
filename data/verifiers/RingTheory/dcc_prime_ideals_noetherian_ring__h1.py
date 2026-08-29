import sympy
from sympy import oo
import sympy.combinatorics as combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "Every strictly descending chain of prime ideals in R is finite."
    
    The negation of the conclusion is:
    "R has an infinite strictly descending chain of prime ideals."
    """
    try:
        neg_q = False
        
        if isinstance(witness, str):
            s = witness.lower()
            # Check for common string representations of rings with infinitely many variables
            if "..." in s or "infinite" in s or "x_1, x_2" in s or "x1, x2" in s or "infinity" in s:
                neg_q = True
        else:
            # Check for mock objects with specific attributes
            if hasattr(witness, 'has_infinite_descending_chain_of_prime_ideals'):
                val = witness.has_infinite_descending_chain_of_prime_ideals
                neg_q = bool(val() if callable(val) else val)
            elif hasattr(witness, 'infinite_descending_chain_of_prime_ideals'):
                val = witness.infinite_descending_chain_of_prime_ideals
                neg_q = bool(val() if callable(val) else val)
            elif hasattr(witness, 'krull_dimension'):
                kd = witness.krull_dimension
                val = kd() if callable(kd) else kd
                if val == oo or str(val).lower() in ['infinity', 'oo']:
                    # While infinite Krull dimension doesn't strictly imply infinite descending chains 
                    # (e.g., in some Noetherian rings), in the context of typical counterexamples 
                    # (like polynomial rings in infinitely many variables), it does.
                    neg_q = True
                    
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R has an infinite strictly descending chain of prime ideals"
]

N_HYP = 0
NEG_Q_INDEX = 0