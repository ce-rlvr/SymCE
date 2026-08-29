import sympy

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a sequence (list or tuple) of complex numbers.
    """
    # H_1: x is a sequence of complex numbers
    try:
        h1 = isinstance(witness, (list, tuple)) and len(witness) > 0
        if h1:
            for xi in witness:
                # sympify will raise an exception if it's not a valid mathematical expression/number
                sympy.sympify(xi)
    except Exception:
        h1 = False

    # H_2: x_0 != 0
    try:
        h2 = False
        if h1:
            h2 = sympy.simplify(sympy.sympify(witness[0])) != 0
    except Exception:
        h2 = False

    # neg_Q: The finite sum is NOT exactly equal to the generalized continued fraction
    try:
        neg_q = False
        if h1:
            x = [sympy.sympify(xi) for xi in witness]
            
            # Calculate the finite sum: sum_{i=0}^n prod_{j=0}^i x_j
            total_sum = 0
            current_prod = 1
            for xi in x:
                current_prod *= xi
                total_sum += current_prod
                
            n = len(x) - 1
            if n == 0:
                cf_val = x[0]
                diff = sympy.simplify(total_sum - cf_val)
                neg_q = (diff != 0)
            else:
                # Evaluate the continued fraction bottom-up
                W = 0
                undefined = False
                for k in range(n, 0, -1):
                    denom = sympy.simplify(1 + x[k] - W)
                    if denom == 0:
                        undefined = True
                        break
                    W = x[k] / denom
                
                if undefined:
                    # If division by zero occurs, the continued fraction is undefined,
                    # hence it cannot be exactly equal to the well-defined finite sum.
                    neg_q = True
                else:
                    denom_final = sympy.simplify(1 - W)
                    if denom_final == 0:
                        neg_q = True
                    else:
                        cf_val = x[0] / denom_final
                        diff = sympy.simplify(total_sum - cf_val)
                        neg_q = (diff != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x is a sequence of complex numbers",
    "H_2: x_0 != 0",
    "¬Q: The finite sum is not exactly equal to the generalized continued fraction"
]

N_HYP = 2
NEG_Q_INDEX = 2