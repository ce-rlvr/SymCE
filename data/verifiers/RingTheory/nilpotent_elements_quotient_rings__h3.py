import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
# Using sympy symbols and basic rings/fields as needed for commutative rings.

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The image of x in R/I is nilpotent XOR x belongs to the radical of I"
]

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    The witness can be provided as a custom object with methods, a dictionary,
    or a tuple of SymPy objects (R, I, x).
    """
    # 1. Try custom object interface
    try:
        h1 = bool(witness.is_commutative_ring())
        h2 = bool(witness.is_ideal())
        nilpotent = bool(witness.is_nilpotent_mod())
        in_rad = bool(witness.in_radical())
        return [h1, h2, nilpotent != in_rad]
    except Exception:
        pass

    # 2. Try dictionary interface
    try:
        h1 = witness['is_commutative_ring']
        if callable(h1): h1 = h1()
        
        h2 = witness['is_ideal']
        if callable(h2): h2 = h2()
        
        nilpotent = witness['is_nilpotent_mod']
        if callable(nilpotent): nilpotent = nilpotent()
        
        in_rad = witness['in_radical']
        if callable(in_rad): in_rad = in_rad()
        
        return [bool(h1), bool(h2), bool(nilpotent != in_rad)]
    except Exception:
        pass

    # 3. Try SymPy tuple interface: witness = (R, I, x)
    try:
        R, I, elem = witness
        
        # Check H1: R is a commutative ring
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            h1 = True  # Fallback assumption if it's a valid SymPy ring
            
        # Check H2: I is an ideal of R
        from sympy.polys.ideals import Ideal
        h2 = isinstance(I, Ideal) and I.ring == R
        
        # Check if elem is nilpotent modulo I
        nilpotent = False
        curr = elem
        for n in range(1, 100):
            if I.contains(curr):
                nilpotent = True
                break
            curr = curr * elem
            
        # Check if elem is in the radical of I
        if hasattr(I, 'radical'):
            rad_I = I.radical()
            if callable(rad_I):
                rad_I = rad_I()
            in_rad = bool(rad_I.contains(elem))
        else:
            # If the ideal doesn't have a radical method, fallback to the nilradical definition
            in_rad = nilpotent
            
        neg_q = (nilpotent != in_rad)
        
        return [h1, h2, neg_q]
    except Exception:
        pass

    # If all interfaces fail, return False for all conditions
    return [False, False, False]