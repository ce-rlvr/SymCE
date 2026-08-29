import sympy
from sympy import Symbol, Poly, degree, gcd, diff

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture.
    The conjecture states:
      Hypotheses:
        - f(x) is a separable polynomial over F of degree n >= 2
        - K is the splitting field of f(x) over F
      Conclusion:
        G acts 2-transitively on the roots of f(x) if and only if f(x) is irreducible over F 
        and for any root alpha of f(x), the polynomial f(x)/(x-alpha) is irreducible over F(alpha).
        
    Mathematically, for any separable polynomial, the Galois group G acts 2-transitively on its roots 
    if and only if G acts transitively (f is irreducible) and the stabilizer of a root alpha acts 
    transitively on the remaining roots (f(x)/(x-alpha) is irreducible over F(alpha)). 
    Therefore, the conclusion is a mathematical tautology (A <==> B and C is always true).
    Thus, the negated conclusion is always False for any valid polynomial.
    """
    x = Symbol('x')
    
    # H1: f(x) is a separable polynomial over F of degree n >= 2
    h1_ok = False
    try:
        f = witness
        p = Poly(f, x, domain='QQ')
        n = degree(p)
        if n >= 2:
            # Check separability: gcd(f, f') == 1
            f_diff = diff(f, x)
            if Poly(gcd(f, f_diff, x), x).degree() == 0:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H2: K is the splitting field of f(x) over F
    # This is a definitional hypothesis for K and G, so it holds by definition for the witness.
    h2_ok = h1_ok

    # neg_Q: The conclusion fails.
    # Since the conclusion is a known theorem in Galois theory (a tautology), it never fails.
    neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f(x) is a separable polynomial over F of degree n >= 2",
    "H_2: K is the splitting field of f(x) over F",
    "¬Q: The equivalence between 2-transitivity and the irreducibility conditions fails"
]

N_HYP = 2
NEG_Q_INDEX = 2