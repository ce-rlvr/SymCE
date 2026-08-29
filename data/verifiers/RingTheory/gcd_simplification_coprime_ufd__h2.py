import sympy
from sympy.abc import x, y, z
from sympy.polys.domains import ZZ, QQ

# Top-level setup
# (Standard domains and symbols are available for witness construction)

def conditions(witness):
    """
    Checks whether the given witness satisfies the remaining hypotheses
    and fails the conclusion of the conjecture.
    
    Witness is expected to be a tuple: (R, a, b, c)
    where R is a sympy Domain (e.g., ZZ, QQ[x]), and a, b, c are elements of R.
    """
    try:
        R, a, b, c = witness
    except Exception:
        return [False, False, False]
        
    # Safely convert a, b, c to domain elements if they are sympy expressions
    try:
        if hasattr(R, 'of_type') and hasattr(R, 'from_sympy'):
            if not R.of_type(a): a = R.from_sympy(sympy.sympify(a))
            if not R.of_type(b): b = R.from_sympy(sympy.sympify(b))
            if not R.of_type(c): c = R.from_sympy(sympy.sympify(c))
    except Exception:
        pass

    # H_1: R is a unique factorization domain
    try:
        h1 = (R.is_UFD == True)
    except Exception:
        h1 = False
        
    # H_2: gcd(a, b) = 1 up to units
    try:
        g = R.gcd(a, b)
        if g == R.zero:
            h2 = (R.one == R.zero)
        else:
            # g is a unit if it divides 1
            R.exquo(R.one, g)
            h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: gcd(a, bc) and gcd(a, c) are NOT associates in R
    try:
        bc = R.mul(b, c)
        g1 = R.gcd(a, bc)
        g2 = R.gcd(a, c)
        
        def divides(elem1, elem2):
            if elem1 == R.zero:
                return elem2 == R.zero
            try:
                R.exquo(elem2, elem1)
                return True
            except Exception:
                return False
                
        # They are associates if they divide each other
        are_associates = divides(g1, g2) and divides(g2, g1)
        neg_q = not are_associates
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: gcd(a, b) = 1 up to units",
    "¬Q: gcd(a, bc) and gcd(a, c) are not associates in R"
]

N_HYP = 2
NEG_Q_INDEX = 2