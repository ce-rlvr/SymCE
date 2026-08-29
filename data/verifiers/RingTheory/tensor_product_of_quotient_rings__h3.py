import sympy
from sympy import S, FiniteSet, ImageSet, Lambda
from sympy.abc import x, y, z
from sympy.polys.rings import ring
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup
# The witness is expected to be a tuple (R, I, J) or a dictionary {'R': R, 'I': I, 'J': J}
# where R is a commutative ring, I is an ideal of R, and J is the object that fails the dropped hypothesis.

def is_comm_ring(R):
    try:
        if getattr(R, 'is_commutative', False):
            return True
            
        domain_names = ('RationalField', 'IntegerRing', 'RealField', 'ComplexField', 
                        'PolyRing', 'FractionField', 'AlgebraicField', 'PolynomialRing')
        if type(R).__name__ in domain_names:
            if hasattr(R, 'is_commutative') and not R.is_commutative:
                return False
            return True
            
        if R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            return True
            
        if getattr(R, 'is_CommutativeRing', False):
            return True
    except Exception:
        pass
    return False

def is_ideal(R, I):
    if type(I).__name__ == 'PolyIdeal' and getattr(I, 'ring', None) == R:
        return True
    if hasattr(I, 'is_ideal') and I.is_ideal:
        if getattr(I, 'ring', None) == R:
            return True
    if R == S.Integers and isinstance(I, ImageSet) and I.base_set == S.Integers:
        return True
    if getattr(I, 'is_ideal_of', None):
        try:
            if I.is_ideal_of(R):
                return True
        except Exception:
            pass
    return False

def is_ideal_lenient(R, I):
    if is_ideal(R, I):
        return True
    if isinstance(I, (list, tuple, set, frozenset)):
        try:
            if all(i in R for i in I):
                return True
        except Exception:
            pass
    if getattr(I, 'is_FiniteSet', False):
        try:
            if all(i in R for i in I):
                return True
        except Exception:
            pass
    try:
        if I in R:
            return True
    except Exception:
        pass
    return False

def conclusion_holds(R, I, J):
    # If J is an ideal of R, the conclusion holds.
    if is_ideal(R, J):
        return True
        
    # If J is a collection of elements in R, it generates an ideal, so the conclusion holds.
    if isinstance(J, (list, tuple, set, frozenset)):
        try:
            if all(j in R for j in J):
                return True
        except Exception:
            pass
            
    if getattr(J, 'is_FiniteSet', False):
        try:
            if all(j in R for j in J):
                return True
        except Exception:
            pass
            
    # If J is a single element of R, it generates a principal ideal, so the conclusion holds.
    try:
        if J in R:
            return True
    except Exception:
        pass
        
    # If J is a SymPy Ideal or Submodule of R
    if type(J).__name__ in ('PolyIdeal', 'Submodule'):
        if getattr(J, 'ring', None) == R:
            return True
            
    # If J is an ImageSet over Integers
    if R == S.Integers and isinstance(J, ImageSet) and J.base_set == S.Integers:
        return True
        
    # Custom object claiming to be an ideal
    if getattr(J, 'is_ideal_of', None):
        try:
            if J.is_ideal_of(R):
                return True
        except Exception:
            pass
            
    # Otherwise, J is not an ideal (e.g., a subring, or an ideal of a different ring),
    # so R/J is not an R-module and the tensor product is undefined/not isomorphic.
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        else:
            R, I, J = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(is_comm_ring(R))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_ideal_lenient(R, I))
    except Exception:
        h2 = False

    try:
        neg_q = not bool(conclusion_holds(R, I, J))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The tensor product (R/I) \\otimes_R (R/J) is NOT isomorphic to R/(I+J)"
]

N_HYP = 2
NEG_Q_INDEX = 2