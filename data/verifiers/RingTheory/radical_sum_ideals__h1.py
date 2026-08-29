import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z, t, a, b, c, d

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: The radical of I + J is not equal to the radical of \\sqrt{I} + \\sqrt{J}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    I = None
    J = None
    try:
        if isinstance(witness, dict):
            I = witness.get('I')
            J = witness.get('J')
        elif hasattr(witness, 'I') and hasattr(witness, 'J'):
            I = witness.I
            J = witness.J
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                I, J = witness
            elif len(witness) == 3:
                _, I, J = witness
    except Exception:
        pass

    if I is None or J is None:
        return [False, False, False]

    # H_1: I is an ideal of R
    try:
        if hasattr(witness, 'is_ideal'):
            h1 = bool(witness.is_ideal(I))
        elif hasattr(I, 'is_ideal'):
            h1 = bool(I.is_ideal())
        elif hasattr(I, 'is_ideal_of'):
            h1 = bool(I.is_ideal_of())
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: J is an ideal of R
    try:
        if hasattr(witness, 'is_ideal'):
            h2 = bool(witness.is_ideal(J))
        elif hasattr(J, 'is_ideal'):
            h2 = bool(J.is_ideal())
        elif hasattr(J, 'is_ideal_of'):
            h2 = bool(J.is_ideal_of())
        else:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The radical of I + J is not equal to the radical of \sqrt{I} + \sqrt{J}
    try:
        def get_rad(X):
            if hasattr(witness, 'radical'):
                rad_attr = witness.radical
                if callable(rad_attr):
                    return rad_attr(X)
                elif isinstance(rad_attr, dict):
                    return rad_attr[X]
            if hasattr(witness, 'rad'):
                rad_attr = witness.rad
                if callable(rad_attr):
                    return rad_attr(X)
                elif isinstance(rad_attr, dict):
                    return rad_attr[X]
            if hasattr(X, 'radical'):
                rad = X.radical
                return rad() if callable(rad) else rad
            elif hasattr(X, 'rad'):
                rad = X.rad
                return rad() if callable(rad) else rad
            else:
                raise AttributeError("No radical method found on object")

        def add_ideals(X, Y):
            if hasattr(witness, 'add'):
                return witness.add(X, Y)
            if hasattr(X, 'add'):
                return X.add(Y)
            return X + Y

        def are_equal(X, Y):
            if hasattr(witness, 'are_equal'):
                return witness.are_equal(X, Y)
            if hasattr(witness, 'equals'):
                return witness.equals(X, Y)
            if hasattr(X, 'equals'):
                return X.equals(Y)
            if hasattr(X, 'is_equal'):
                return X.is_equal(Y)
            return X == Y

        rad_I = get_rad(I)
        rad_J = get_rad(J)
        
        I_plus_J = add_ideals(I, J)
        rad_I_plus_J = get_rad(I_plus_J)
        
        rad_I_plus_rad_J = add_ideals(rad_I, rad_J)
        rad_rad_I_plus_rad_J = get_rad(rad_I_plus_rad_J)

        eq = are_equal(rad_I_plus_J, rad_rad_I_plus_rad_J)
        neg_q = not eq
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]