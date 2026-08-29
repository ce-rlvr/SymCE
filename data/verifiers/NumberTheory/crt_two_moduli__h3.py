import sympy

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Chinese Remainder Theorem conjecture.
    The witness should be a tuple or list: (m1, m2, a1, a2)
    """
    try:
        if isinstance(witness, dict):
            m1 = witness.get('m1')
            m2 = witness.get('m2')
            a1 = witness.get('a1')
            a2 = witness.get('a2')
        else:
            m1, m2, a1, a2 = witness
    except Exception:
        return [False, False, False]

    # H1: m1 and m2 are positive integers
    try:
        m1_sym = sympy.sympify(m1)
        m2_sym = sympy.sympify(m2)
        if m1_sym.is_integer and m2_sym.is_integer:
            h1 = bool(m1_sym > 0 and m2_sym > 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: gcd(m1, m2) = 1
    try:
        if m1_sym.is_integer and m2_sym.is_integer:
            h2 = bool(sympy.gcd(m1_sym, m2_sym) == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    # Neg_Q: Conclusion fails
    # Conclusion: There exists an integer x such that x ≡ a1 (mod m1) and x ≡ a2 (mod m2), 
    # and x is unique modulo m1*m2.
    try:
        a1_sym = sympy.sympify(a1)
        a2_sym = sympy.sympify(a2)
        
        # If m1 and m2 are valid positive integers, we evaluate the existence and uniqueness of x.
        if m1_sym.is_integer and m2_sym.is_integer and m1_sym > 0 and m2_sym > 0:
            # For an integer x to satisfy x ≡ a1 (mod m1), a1 must be an integer.
            # If a1 or a2 is not an integer, no such integer x exists.
            if a1_sym.is_integer and a2_sym.is_integer:
                g = sympy.gcd(m1_sym, m2_sym)
                # By CRT, a solution exists iff gcd(m1, m2) divides (a1 - a2)
                if (a1_sym - a2_sym) % g != 0:
                    q = False
                else:
                    # If a solution exists, the number of solutions modulo m1*m2 is exactly g.
                    # The conclusion requires the solution to be unique modulo m1*m2.
                    q = (g == 1)
            else:
                q = False
        else:
            q = False
            
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m1 and m2 are positive integers",
    "H_2: gcd(m1, m2) = 1",
    "¬Q: It is not the case that there exists a unique integer x modulo m1*m2 satisfying the congruences"
]

N_HYP = 2
NEG_Q_INDEX = 2