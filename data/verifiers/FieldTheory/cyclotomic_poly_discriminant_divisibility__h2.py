import sympy
from sympy import Symbol, cyclotomic_poly, discriminant, totient

# Top-level setup
# No special named objects needed for this number theory / polynomial conjecture.

def conditions(witness) -> list[bool]:
    # Hypothesis 1: n >= 1 is an integer
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n >= 1)
    except Exception:
        h1 = False

    # Hypothesis 2: \Delta(\Phi_n) is the discriminant of \Phi_n(x)
    # This is a definitional hypothesis, so it holds whenever n is valid.
    h2 = h1

    # Conclusion: \Delta(\Phi_n) divides n^{\phi(n)} in \mathbb{Z}
    # Negated Conclusion: \Delta(\Phi_n) does NOT divide n^{\phi(n)} in \mathbb{Z}
    try:
        if not h1:
            neg_q = False
        else:
            x = Symbol('x')
            poly = cyclotomic_poly(n, x)
            delta = discriminant(poly, x)
            tot = totient(n)
            val = n**tot
            
            if delta == 0:
                neg_q = (val != 0)
            else:
                neg_q = (val % delta != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: \\Delta(\\Phi_n) is the discriminant of \\Phi_n(x)",
    "not Q: \\Delta(\\Phi_n) does not divide n^{\\phi(n)} in \\mathbb{Z}"
]

N_HYP = 2
NEG_Q_INDEX = 2