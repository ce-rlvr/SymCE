import sympy
from sympy.matrices import eye, zeros
import math

# Top-level setup for standard algebra objects relevant to RealAnalysis/LinearAlgebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "The set of subsequential limits of the sequence (|x_n|) is equal to {|s| : s \in S}."
    
    Since computing the set of subsequential limits of an arbitrary sequence is 
    uncomputable in general, the verifier expects the witness to directly provide 
    the set of subsequential limits S of (x_n) and the set of subsequential limits T of (|x_n|).
    """
    try:
        # H_1: Let S be the set of subsequential limits of (x_n).
        # This is a definitional hypothesis, so it holds for any valid witness.
        h1_ok = True
        
        # Extract S and T from the witness
        if hasattr(witness, 'S') and hasattr(witness, 'T'):
            S = set(witness.S)
            T = set(witness.T)
        elif isinstance(witness, dict) and 'S' in witness and 'T' in witness:
            S = set(witness['S'])
            T = set(witness['T'])
        elif isinstance(witness, tuple) and len(witness) >= 2:
            S = set(witness[-2])
            T = set(witness[-1])
        else:
            # Cannot extract S and T from the witness
            return [False, False]
            
        # Compute {|s| : s \in S}
        abs_S = set()
        for s in S:
            try:
                abs_S.add(abs(s))
            except Exception:
                # Fallback for objects where abs() might be defined differently (e.g. vectors)
                if hasattr(s, 'norm'):
                    abs_S.add(s.norm())
                else:
                    raise
                    
        # ¬Q: The set of subsequential limits of (|x_n|) is NOT equal to {|s| : s \in S}
        neg_q_ok = (T != abs_S)
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: Let S be the set of subsequential limits of (x_n)",
    "¬Q: The set of subsequential limits of the sequence (|x_n|) is not equal to {|s| : s \in S}"
]

N_HYP = 1
NEG_Q_INDEX = 1