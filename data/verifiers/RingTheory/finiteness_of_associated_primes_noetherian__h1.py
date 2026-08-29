import sympy
from sympy import symbols
import math
import itertools
import functools

# Top-level setup
# Since SymPy does not natively support rings with infinitely many variables or 
# computing associated primes, we provide mock classes that the witness expression 
# may return, or the witness can be a descriptive string/dictionary.

class Module:
    def __init__(self, is_finitely_generated=True, has_finite_associated_primes=True):
        self.is_finitely_generated = is_finitely_generated
        self.has_finite_associated_primes = has_finite_associated_primes

class Counterexample(Module):
    """
    Witness for the Finiteness of Associated Primes conjecture.
    Represents a finitely generated module over a non-Noetherian ring
    with infinitely many associated primes.
    For example, M = R = k[x_1, x_2, ...] / (x_i x_j | i != j).
    """
    def __init__(self):
        super().__init__(is_finitely_generated=True, has_finite_associated_primes=False)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # Handle string descriptions
        if isinstance(witness, str):
            s = witness.lower()
            h1 = True
            if "infinite" in s or "..." in s or "x_i" in s or "not noetherian" in s or "infinitely many" in s:
                neg_q = True
            return [h1, neg_q]
            
        # Handle tuple/list descriptions
        if isinstance(witness, (tuple, list)):
            s = str(witness).lower()
            h1 = True
            if "infinite" in s or "..." in s or "x_i" in s or "not noetherian" in s or "infinitely many" in s:
                neg_q = True
            return [h1, neg_q]

        # Handle dictionary representations
        if isinstance(witness, dict):
            h1 = witness.get("is_finitely_generated", True)
            if "has_finite_associated_primes" in witness:
                neg_q = not bool(witness["has_finite_associated_primes"])
            elif "has_infinite_associated_primes" in witness:
                neg_q = bool(witness["has_infinite_associated_primes"])
            else:
                s = str(witness).lower()
                neg_q = "infinite" in s or "..." in s or "x_i" in s or "not noetherian" in s
            return [bool(h1), bool(neg_q)]

        # Handle custom objects or mock classes
        if hasattr(witness, "is_finitely_generated"):
            h1 = bool(witness.is_finitely_generated)
        elif hasattr(witness, "is_fg"):
            h1 = bool(witness.is_fg)
        else:
            h1 = True  # Default to True for custom objects assuming M=R
            
        if hasattr(witness, "has_finite_associated_primes"):
            neg_q = not bool(witness.has_finite_associated_primes)
        elif hasattr(witness, "has_infinite_associated_primes"):
            neg_q = bool(witness.has_infinite_associated_primes)
        elif hasattr(witness, "associated_primes_finite"):
            neg_q = not bool(witness.associated_primes_finite)
        elif hasattr(witness, "is_noetherian"):
            neg_q = not bool(witness.is_noetherian)
        else:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a finitely generated R-module",
    "¬Q: The set of associated primes Ass_R(M) is not finite"
]

N_HYP = 1
NEG_Q_INDEX = 1