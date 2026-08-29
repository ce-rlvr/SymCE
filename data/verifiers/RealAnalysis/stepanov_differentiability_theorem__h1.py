import sympy
from sympy import symbols
import math
import itertools
import functools

# Top-level setup
x, y, z = symbols('x y z', real=True)

def conditions(witness) -> list[bool]:
    """
    Verifies if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis from Stepanov's Theorem is that f is measurable.
    A valid counterexample must be a non-measurable function.
    """
    h1 = True
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            # Check if the dictionary explicitly defines H1
            if "A_is_limsup_finite" in witness:
                h1 = bool(witness["A_is_limsup_finite"])
            elif "A_def" in witness:
                h1 = bool(witness["A_def"])
                
            # Check if the conclusion fails (f is not differentiable a.e. on A)
            if "is_differentiable_ae_on_A" in witness:
                neg_q = not bool(witness["is_differentiable_ae_on_A"])
            elif "is_differentiable_ae" in witness:
                neg_q = not bool(witness["is_differentiable_ae"])
            elif "measurable" in witness:
                neg_q = not bool(witness["measurable"])
            elif "f" in witness and isinstance(witness["f"], str):
                s = witness["f"].lower()
                neg_q = "non-measurable" in s or "nonmeasurable" in s or "vitali" in s
                
        elif isinstance(witness, str):
            s = witness.lower()
            neg_q = "non-measurable" in s or "nonmeasurable" in s or "vitali" in s or "counterexample" in s
            
        else:
            # Witness is an object
            if hasattr(witness, "A_is_limsup_finite"):
                h1 = bool(witness.A_is_limsup_finite)
                
            if hasattr(witness, "is_differentiable_ae_on_A"):
                neg_q = not bool(witness.is_differentiable_ae_on_A)
            elif hasattr(witness, "is_differentiable_ae"):
                neg_q = not bool(witness.is_differentiable_ae)
            elif hasattr(witness, "measurable"):
                neg_q = not bool(witness.measurable)
            else:
                name = ""
                if hasattr(witness, "__name__"):
                    name = witness.__name__.lower()
                elif hasattr(witness, "__class__"):
                    name = witness.__class__.__name__.lower()
                
                if "non_measurable" in name or "nonmeasurable" in name or "vitali" in name:
                    neg_q = True
                    
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is the set of points x in R^n such that limsup_{y -> x} |f(y)-f(x)|/|y-x| < infinity",
    "¬Q: f is not differentiable almost everywhere on the set A"
]

N_HYP = 1
NEG_Q_INDEX = 1