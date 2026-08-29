import sympy
from sympy import Symbol, Rational, Integer, eye, zeros, cyclotomic_poly
from sympy.ntheory import mobius, divisors
from sympy.abc import x, y, z
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Mobius Inversion Formula 
    for Cyclotomic Polynomials.
    
    The witness is expected to be a tuple (n, x_val) where n is the index of the 
    cyclotomic polynomial and x_val is the point of evaluation. It can also be 
    just n for a symbolic check.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, x_val = witness
        else:
            n = witness
            x_val = None
    except Exception:
        return [False, False, False]
        
    # H_1: \Phi_n(x) is the n-th cyclotomic polynomial
    # This requires n to be a positive integer.
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: \mu is the Mobius function
    # This is a definitional tautology in our context.
    h2 = True
    
    # ¬Q: The conclusion fails at the witness
    # Conclusion: \Phi_n(x) = \prod_{d|n} (x^{n/d} - 1)^{\mu(d)}
    try:
        if not h1:
            neg_q = False
        else:
            x_sym = Symbol('x')
            if x_val is not None:
                lhs = cyclotomic_poly(n, x_sym).subs(x_sym, x_val)
                rhs = 1
                undefined = False
                for d in divisors(n):
                    exponent = mobius(d)
                    base = x_val**(n//d) - 1
                    if exponent > 0:
                        rhs *= base**exponent
                    elif exponent < 0:
                        try:
                            if hasattr(base, 'is_zero') and base.is_zero is not None:
                                is_zero = base.is_zero
                            else:
                                is_zero = (base == 0)
                        except Exception:
                            is_zero = False
                            
                        if is_zero:
                            undefined = True
                            break
                        rhs /= base**(-exponent)
                
                if undefined:
                    # Division by zero means the RHS is undefined, so equality fails.
                    neg_q = True
                else:
                    try:
                        # Fast numerical check if possible
                        val_lhs = complex(lhs)
                        val_rhs = complex(rhs)
                        neg_q = abs(val_lhs - val_rhs) > 1e-9
                    except TypeError:
                        # Fallback to symbolic comparison
                        try:
                            diff = sympy.cancel(lhs - rhs)
                            neg_q = not bool(diff == 0)
                        except Exception:
                            neg_q = bool(lhs != rhs)
            else:
                # Symbolic check if no x_val is provided
                lhs = cyclotomic_poly(n, x_sym)
                rhs = 1
                for d in divisors(n):
                    exponent = mobius(d)
                    base = x_sym**(n//d) - 1
                    if exponent > 0:
                        rhs *= base**exponent
                    elif exponent < 0:
                        rhs /= base**(-exponent)
                diff = sympy.cancel(lhs - rhs)
                neg_q = not bool(diff == 0)
    except Exception:
        # Any evaluation error (e.g., unsupported operations) means the identity fails
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Phi_n(x) is the n-th cyclotomic polynomial",
    "H_2: mu is the Mobius function",
    "¬Q: Phi_n(x) != prod_{d|n} (x^{n/d} - 1)^{mu(d)}"
]

N_HYP = 2
NEG_Q_INDEX = 2