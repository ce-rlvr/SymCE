import sympy

# Top-level setup
x, y, z = sympy.symbols('x y z')

def get_numerator(a):
    """
    Evaluates the continued fraction [a_0; a_1, ..., a_n] and returns the 
    numerator of the resulting reduced fraction.
    """
    a = [sympy.nsimplify(sympy.sympify(val)) for val in a]
    res = a[-1]
    for val in reversed(a[:-1]):
        res = val + sympy.S.One / res
    res = sympy.cancel(res)
    return sympy.fraction(res)[0]

def continuant(a):
    """
    Computes the continuant K(a_0, ..., a_n), which is mathematically equivalent 
    to the sum of the product a_0...a_n and all products obtained by omitting 
    one or more disjoint pairs of consecutive terms.
    """
    p_minus2 = sympy.S.Zero
    p_minus1 = sympy.S.One
    for val in a:
        p = sympy.nsimplify(sympy.sympify(val)) * p_minus1 + p_minus2
        p_minus2 = p_minus1
        p_minus1 = p
    return p_minus1

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be either a list of terms `a` or a tuple `(a, p_n)`.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple)):
            a, p_n = witness
        else:
            a = witness
            p_n = get_numerator(a)
            
        if isinstance(a, str):
            return [False, False]
            
        a = list(a)
        if len(a) < 1:
            return [False, False]
            
        p_n_sym = sympy.nsimplify(sympy.sympify(p_n))
            
        # H_1: p_n is the numerator of the n-th convergent of the continued fraction
        num = get_numerator(a)
        diff_h1 = sympy.simplify(p_n_sym - num)
        h1 = (diff_h1 == sympy.S.Zero)
        
        # ¬Q: p_n is NOT equal to the sum of the product and products with omitted disjoint pairs
        sop = continuant(a)
        diff_q = sympy.simplify(p_n_sym - sop)
        neg_q = (diff_q != sympy.S.Zero)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: p_n is the numerator of the n-th convergent of the continued fraction",
    "¬Q: p_n is NOT equal to the sum of the product and products with omitted disjoint pairs"
]

N_HYP = 1
NEG_Q_INDEX = 1