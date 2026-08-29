import sympy

# Top-level setup: named object bindings that the witness expression may reference.
Integers = sympy.S.Integers
Reals = sympy.S.Reals
Rationals = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness can be a tuple (R, a, b) or just (a, b) where R defaults to Integers.
    """
    try:
        if len(witness) == 3:
            R, a, b = witness
        elif len(witness) == 2:
            a, b = witness
            R = Integers
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: a and b are elements of R
    try:
        if hasattr(R, '__contains__'):
            h1_ok = (a in R) and (b in R)
        else:
            # Fallback if R doesn't support 'in'
            h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The equation ax = b has a solution for x in R if and only if ab = b (must FAIL)
    try:
        # Check if ab = b
        ab_equals_b = (a * b == b)
        
        # Check if ax = b has a solution in R
        has_solution = False
        try:
            if hasattr(R, '__iter__') and not isinstance(R, sympy.Set):
                # Finite iterable ring
                for x in R:
                    try:
                        if a * x == b:
                            has_solution = True
                            break
                    except Exception:
                        pass
            elif R == Integers:
                if a == 0:
                    has_solution = (b == 0)
                else:
                    has_solution = (b % a == 0)
            elif R == Rationals or R == Reals:
                if a == 0:
                    has_solution = (b == 0)
                else:
                    has_solution = True
            else:
                # Fallback to sympy solve
                x = sympy.Symbol('x')
                sols = sympy.solve(a * x - b, x)
                if isinstance(sols, dict):
                    sols = list(sols.values())
                
                if sols:
                    if hasattr(R, '__contains__'):
                        has_solution = any((sol in R) for sol in sols)
                    else:
                        has_solution = True
                else:
                    has_solution = False
        except Exception:
            has_solution = False

        # The conclusion is (has_solution <-> ab_equals_b).
        # We want the conclusion to FAIL, so we want XOR.
        neg_q_ok = (has_solution != ab_equals_b)
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "¬Q: (ax = b has a solution in R) is not equivalent to (ab = b)"
]

N_HYP = 1
NEG_Q_INDEX = 1