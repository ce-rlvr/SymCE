import sympy
from sympy import Matrix, eye, zeros
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture.
    Since the conclusion is mathematically a tautology (an endomorphism is a unit 
    in the endomorphism ring if and only if it is an automorphism), neg_Q will 
    evaluate to False for any valid mathematical object. A dictionary mock is 
    supported for testing purposes.
    """
    # H1: R is a ring (contextual setup, always True for a valid witness)
    h1 = True
    
    # H2: End_R(M) is the ring of R-module endomorphisms of M (contextual setup)
    h2 = True
    
    h3 = False
    neg_q = False
    
    try:
        # Support for a mock dictionary witness
        if isinstance(witness, dict):
            h3 = bool(witness.get("is_endomorphism", False))
            is_unit = bool(witness.get("is_unit", False))
            is_automorphism = bool(witness.get("is_automorphism", False))
            neg_q = is_unit != is_automorphism
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    try:
        # Support for a matrix witness representing an endomorphism of a free module over Z
        if isinstance(witness, Matrix) and witness.is_square:
            h3 = True
            det = witness.det()
            is_unit = (abs(det) == 1)
            is_automorphism = (abs(det) == 1)
            neg_q = is_unit != is_automorphism
            
        # Support for an integer witness representing an endomorphism of Z
        elif isinstance(witness, int):
            h3 = True
            is_unit = (abs(witness) == 1)
            is_automorphism = (abs(witness) == 1)
            neg_q = is_unit != is_automorphism
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Let R be a ring",
    "H_2: Let End_R(M) be the ring of R-module endomorphisms of M",
    "H_3: Let f be an element of End_R(M)",
    "¬Q: f is a unit in End_R(M) XOR f is an R-module automorphism of M"
]

N_HYP = 3
NEG_Q_INDEX = 3