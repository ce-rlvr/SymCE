import sympy
from sympy import Symbol, S
from sympy.calculus.singularities import singularities
from sympy.solvers.solveset import solveset

# Top-level setup: named object bindings that the witness expression may reference.
z = Symbol('z')

def conditions(witness):
    """
    Given a witness expression f(z), checks if it satisfies the hypotheses and 
    falsifies the conclusion of the conjecture.
    """
    h1_ok = False
    try:
        f = sympy.sympify(witness)
        if hasattr(f, 'as_expr'):
            f = f.as_expr()
            
        # Check if f is an entire function (element of H(C))
        if f.is_polynomial(z):
            h1_ok = True
        else:
            sings = singularities(f, z)
            if sings is S.EmptySet:
                h1_ok = True
    except Exception:
        h1_ok = False

    side_a = False
    side_b = False
    try:
        f = sympy.sympify(witness)
        if hasattr(f, 'as_expr'):
            f = f.as_expr()
            
        if h1_ok:
            # In the ring of entire functions H(C), a function is a unit
            # if and only if it has no zeros in C.
            zeros = solveset(f, z, domain=S.Complexes)
            if zeros is S.EmptySet:
                side_a = True
            
            # Similarly, an entire function f can be written as e^g for some entire g
            # if and only if f has no zeros in C (since C is simply connected).
            if zeros is S.EmptySet:
                side_b = True
    except Exception:
        pass

    # The conclusion is the equivalence: side_a <==> side_b
    # The negated conclusion is True if the equivalence fails.
    neg_q = not (side_a == side_b)

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f is an element of H(C)",
    "¬Q: f is a unit in H(C) is not equivalent to exists g in H(C) such that f(z) = e^{g(z)}"
]

N_HYP = 1
NEG_Q_INDEX = 1