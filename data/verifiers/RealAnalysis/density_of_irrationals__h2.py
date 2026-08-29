import sympy

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a tuple or list of two real numbers (x, y).
    """
    try:
        if isinstance(witness, str):
            return [False, False]
        iterator = iter(witness)
        x = next(iterator)
        y = next(iterator)
        try:
            next(iterator)
            # More than 2 elements
            return [False, False]
        except StopIteration:
            pass
    except Exception:
        return [False, False]
        
    try:
        x_sp = sympy.sympify(x)
        y_sp = sympy.sympify(y)
        h1 = bool(x_sp.is_number and x_sp.is_real and y_sp.is_number and y_sp.is_real)
    except Exception:
        h1 = False
        
    try:
        x_sp = sympy.sympify(x)
        y_sp = sympy.sympify(y)
        # The negated conclusion is that there is NO irrational z such that x < z < y.
        # Since the irrational numbers are dense in the reals, this is true if and only if x >= y.
        neg_q = bool(x_sp >= y_sp)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are real numbers",
    "¬Q: There does not exist an irrational number z such that x < z < y"
]

N_HYP = 1
NEG_Q_INDEX = 1