import sympy
from sympy import Poly

# Top-level setup
x, y, z, t = sympy.symbols('x y z t')

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the conjecture.
    The witness is expected to be a SymPy expression representing a polynomial 
    generator for a principal ideal P in the graded commutative ring Q[x, y, ...].
    """
    try:
        # Handle list/tuple/set by taking the first element if it's a principal ideal
        if isinstance(witness, (list, tuple, set)):
            if len(witness) == 1:
                witness = list(witness)[0]
            else:
                return [False, False]
                
        if isinstance(witness, str):
            witness = sympy.sympify(witness)
            
        if not isinstance(witness, sympy.Basic):
            witness = sympy.sympify(witness)
            
        free_symbols = list(witness.free_symbols)
        if not free_symbols:
            # If it's a constant, use a dummy variable to form the polynomial ring
            free_symbols = [x]
            
        # Interpret the witness as a polynomial over the rationals
        f = Poly(witness, *free_symbols, domain='QQ')
    except Exception:
        return [False, False]
        
    # H_1: R is a graded commutative ring
    # By interpreting the witness as a polynomial in Q[X], R is Q[X] 
    # which is always a graded commutative ring under the standard grading.
    h1 = True
    
    try:
        # Check if P = <f> is a prime ideal in Q[X]
        # Q[X] is a UFD, so <f> is prime iff f is irreducible or f == 0.
        # Note: units (degree 0 non-zero constants) generate the whole ring, which is not prime.
        if f.is_zero:
            is_prime = True
        elif f.degree() == 0:
            is_prime = False
        else:
            is_prime = f.is_irreducible
            
        # Check if the condition holds: 
        # "for every pair of homogeneous elements a, b in R, ab in P implies a in P or b in P"
        # In a graded integral domain, the product of two non-zero elements is homogeneous 
        # if and only if both elements are homogeneous.
        # Thus, if f is NOT homogeneous, it can never divide a product of homogeneous elements 
        # unless that product is zero. So the condition holds vacuously (or trivially for 0).
        # If f IS homogeneous, the condition holds iff f is prime (or a unit/zero).
        if f.is_zero:
            condition_holds = True
        elif f.degree() == 0:
            condition_holds = True
        elif not f.is_homogeneous:
            condition_holds = True
        else:
            condition_holds = f.is_irreducible
            
        # The conclusion claims: P is prime iff the condition holds.
        # We negate this to find a counterexample.
        neg_q = not (is_prime == condition_holds)
        
    except Exception:
        return [False, False]
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a graded commutative ring",
    "¬Q: The equivalence (P is prime iff homogeneous condition holds) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1