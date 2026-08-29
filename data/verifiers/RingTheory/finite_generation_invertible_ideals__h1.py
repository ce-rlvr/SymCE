import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If I and J are ideals of R and IJ = R, then I is finitely generated."
    (This is false for rings without identity).
    """
    def check_prop(obj, names, default=False):
        if isinstance(obj, dict):
            for name in names:
                if name in obj:
                    try:
                        val = obj[name]
                        return val() if callable(val) else val
                    except Exception:
                        pass
        for name in names:
            if hasattr(obj, name):
                try:
                    val = getattr(obj, name)
                    return val() if callable(val) else val
                except Exception:
                    pass
        return default

    def is_sympy_ideal(obj):
        return type(obj).__name__ in ['PolyIdeal', 'Ideal']

    h1, h2, h3, neg_q = False, False, False, False

    try:
        # 1. Dictionary or object with direct boolean flags
        if isinstance(witness, dict) or any(hasattr(witness, attr) for attr in ['I_is_ideal', 'is_ideal_I', 'IJ_equals_R', 'product_equals_ring']):
            h1 = bool(check_prop(witness, ['I_is_ideal', 'is_ideal_I', 'I_ideal']))
            h2 = bool(check_prop(witness, ['J_is_ideal', 'is_ideal_J', 'J_ideal']))
            h3 = bool(check_prop(witness, ['IJ_equals_R', 'product_equals_ring', 'IJ_eq_R']))
            q = bool(check_prop(witness, ['I_is_finitely_generated', 'is_finitely_generated_I', 'I_finitely_generated'], True))
            neg_q = not q
            return [h1, h2, h3, neg_q]

        # 2. Tuple (R, I, J)
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
            
            # H1: I is ideal
            try:
                if is_sympy_ideal(I):
                    h1 = True
                elif hasattr(R, 'is_ideal'):
                    h1 = bool(R.is_ideal(I))
                else:
                    h1 = bool(check_prop(I, ['is_ideal', 'is_ideal_of'], False))
            except Exception:
                h1 = False
                
            # H2: J is ideal
            try:
                if is_sympy_ideal(J):
                    h2 = True
                elif hasattr(R, 'is_ideal'):
                    h2 = bool(R.is_ideal(J))
                else:
                    h2 = bool(check_prop(J, ['is_ideal', 'is_ideal_of'], False))
            except Exception:
                h2 = False
                
            # H3: IJ = R
            try:
                if hasattr(R, 'product_equals_ring'):
                    h3 = bool(R.product_equals_ring(I, J))
                elif hasattr(R, 'product'):
                    h3 = bool(R.product(I, J) == R)
                elif hasattr(I, 'product'):
                    h3 = bool(I.product(J) == R)
                else:
                    h3 = bool((I * J) == R)
            except Exception:
                h3 = False
                
            # Q: I is finitely generated
            try:
                if is_sympy_ideal(I):
                    q = True
                elif hasattr(R, 'is_finitely_generated'):
                    q = bool(R.is_finitely_generated(I))
                else:
                    q = bool(check_prop(I, ['is_finitely_generated', 'is_fin_gen'], True))
                neg_q = not q
            except Exception:
                neg_q = False
                
            return [h1, h2, h3, neg_q]

        # 3. Tuple (I, J)
        if isinstance(witness, tuple) and len(witness) == 2:
            I, J = witness
            try:
                h1 = True if is_sympy_ideal(I) else bool(check_prop(I, ['is_ideal'], False))
            except Exception:
                h1 = False
            try:
                h2 = True if is_sympy_ideal(J) else bool(check_prop(J, ['is_ideal'], False))
            except Exception:
                h2 = False
            try:
                if hasattr(I, 'ring'):
                    h3 = bool((I * J) == I.ring)
                elif hasattr(I, 'product_equals_ring'):
                    h3 = bool(I.product_equals_ring(J))
                else:
                    h3 = False
            except Exception:
                h3 = False
            try:
                if is_sympy_ideal(I):
                    q = True
                else:
                    q = bool(check_prop(I, ['is_finitely_generated'], True))
                neg_q = not q
            except Exception:
                neg_q = False
            return [h1, h2, h3, neg_q]

    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "H_3: The product ideal IJ is equal to the ring R",
    "¬Q: The ideal I is not finitely generated"
]

N_HYP = 3
NEG_Q_INDEX = 3