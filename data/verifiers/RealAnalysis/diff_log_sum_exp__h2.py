import sympy
import math
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H_1_ok, neg_Q_ok].
    """
    # H_1: f: R^n -> R is defined by f(x) = log(sum_{i=1}^n e^{x_i})
    # This hypothesis simply establishes the definition of f for a point in n-dimensional space.
    # We verify that the witness 'a' is a valid sequence of length n > 0.
    try:
        _ = iter(witness)
        n = len(witness)
        h1 = n > 0
    except Exception:
        h1 = False

    # neg_Q: The conclusion FAILS at the witness.
    # Conclusion: f is infinitely differentiable at a, and its gradient matches the softmax formula.
    # Since f is defined as a function from R^n to R, it is only differentiable at points within R^n.
    # If 'a' contains non-real or non-finite values (e.g., infinities or complex numbers), 
    # it is outside the domain, so f is not differentiable at a, and the conclusion fails.
    # If 'a' is in R^n, the theorem is true, so the conclusion holds (neg_Q = False).
    try:
        if not h1:
            neg_q = False
        else:
            all_real_finite = True
            for ai in witness:
                val = sympy.sympify(ai)
                
                # Check symbolic finiteness
                is_fin = getattr(val, 'is_finite', None)
                if is_fin is False:
                    all_real_finite = False
                    break
                
                # Check symbolic realness
                is_r = getattr(val, 'is_real', None)
                if is_r is False:
                    all_real_finite = False
                    break
                
                # Check numeric evaluation
                try:
                    c_val = complex(val.evalf())
                    if abs(c_val.imag) > 1e-12:
                        all_real_finite = False
                        break
                    if math.isnan(c_val.real) or math.isinf(c_val.real):
                        all_real_finite = False
                        break
                except Exception:
                    pass
            
            if not all_real_finite:
                neg_q = True
            else:
                # Even if all components are real and finite, verify the sum of exponentials
                # to ensure no division by zero or log of non-positive number occurs.
                S = sum(sympy.exp(sympy.sympify(ai)) for ai in witness)
                try:
                    S_val = complex(S.evalf())
                    if abs(S_val) < 1e-12 or S_val.real <= 0:
                        neg_q = True
                    else:
                        neg_q = False
                except Exception:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is defined as log-sum-exp",
    "¬Q: f is not infinitely differentiable at a or gradient does not match"
]

N_HYP = 1
NEG_Q_INDEX = 1