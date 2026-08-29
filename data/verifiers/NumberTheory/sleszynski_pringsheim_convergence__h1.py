import math

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two functions (a, b) that return the n-th terms
    of the sequences a_n and b_n for n >= 1.
    """
    try:
        a, b = witness
    except Exception:
        return [False, False]

    # Check Hypothesis 1: For all integers n >= 1, |b_n| >= |a_n| + 1
    # We check this for the first 100 terms.
    h1_ok = True
    try:
        for n in range(1, 101):
            an = complex(a(n))
            bn = complex(b(n))
            if abs(bn) < abs(an) + 1 - 1e-9:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    # Check Negated Conclusion: The continued fraction does NOT converge to a finite
    # complex number f such that |f| <= 1.
    # We compute the convergents up to n=100.
    neg_q = False
    try:
        A_prev2, A_prev1 = 1.0 + 0j, 0.0 + 0j
        B_prev2, B_prev1 = 0.0 + 0j, 1.0 + 0j
        
        for n in range(1, 101):
            an = complex(a(n))
            bn = complex(b(n))
            
            An = bn * A_prev1 + an * A_prev2
            Bn = bn * B_prev1 + an * B_prev2
            
            A_prev2, A_prev1 = A_prev1, An
            B_prev2, B_prev1 = B_prev1, Bn
            
        if abs(B_prev1) < 1e-9:
            # Diverges due to division by zero
            neg_q = True
        else:
            f = A_prev1 / B_prev1
            # The conclusion fails if it diverges (which we approximate by checking if it hasn't settled)
            # or if it converges to a value with |f| > 1.
            # However, the Sleszynski-Pringsheim theorem is actually true for all complex numbers.
            # If the user provides a witness, we just evaluate the negation of the conclusion.
            if abs(f) > 1 + 1e-9 or math.isnan(f.real) or math.isnan(f.imag):
                neg_q = True
            else:
                # Check if it diverges by comparing the last few convergents
                A_prev3 = A_prev2 * complex(b(101)) + complex(a(101)) * A_prev1
                B_prev3 = B_prev2 * complex(b(101)) + complex(a(101)) * B_prev1
                if abs(B_prev3) > 1e-9:
                    f_next = A_prev3 / B_prev3
                    if abs(f - f_next) > 1e-2:
                        neg_q = True
    except Exception:
        # If an exception occurs (e.g., overflow), it means it diverges, so conclusion fails.
        neg_q = True

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: For all integers n >= 1, |b_n| >= |a_n| + 1",
    "¬Q: The continued fraction does not converge to a finite complex number f such that |f| <= 1"
]

N_HYP = 1
NEG_Q_INDEX = 1