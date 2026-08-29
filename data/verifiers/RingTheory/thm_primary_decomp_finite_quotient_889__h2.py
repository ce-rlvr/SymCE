import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z, t

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the conjecture:
    "If R is a commutative ring and R/I is finite, then I has a primary decomposition."
    
    The mathematically true theorem requires I to be a proper ideal.
    If I = R, then R/I is the zero ring (which is finite, size 1), 
    but R itself does not have a primary decomposition (as primary ideals must be proper).
    """
    # 1. Handle mock objects or dictionaries
    try:
        if isinstance(witness, dict):
            if 'is_commutative' in witness:
                H1 = bool(witness.get('is_commutative', False))
                H2 = bool(witness.get('quotient_is_finite', False))
                neg_Q = not bool(witness.get('has_primary_decomposition', True))
                return [H1, H2, neg_Q]
        elif hasattr(witness, 'is_commutative') and hasattr(witness, 'quotient_is_finite'):
            H1 = bool(getattr(witness, 'is_commutative', False))
            H2 = bool(getattr(witness, 'quotient_is_finite', False))
            neg_Q = not bool(getattr(witness, 'has_primary_decomposition', True))
            return [H1, H2, neg_Q]
    except Exception:
        pass

    # 2. Handle SymPy objects, typically a tuple (R, I)
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            I = witness
            R = I.ring
            
        H1 = True
        if hasattr(R, 'is_commutative'):
            H1 = bool(R.is_commutative)
            
        is_whole = False
        H2 = False
        
        if isinstance(I, (list, tuple)):
            if R == sympy.ZZ:
                from sympy import gcd
                g = 0
                for gen in I:
                    g = gcd(g, gen)
                if abs(g) == 1:
                    is_whole = True
                elif g != 0:
                    H2 = True
            elif hasattr(R, 'ideal'):
                try:
                    ideal_obj = R.ideal(*I)
                    if ideal_obj.is_whole_ring():
                        is_whole = True
                except Exception:
                    pass
        else:
            if hasattr(I, 'is_whole_ring'):
                is_whole = I.is_whole_ring()
            elif hasattr(I, 'contains') and hasattr(R, 'one'):
                is_whole = I.contains(R.one)
            elif I == R or I == 1:
                is_whole = True
            elif hasattr(R, 'ideal') and I == R.ideal(1):
                is_whole = True
            elif isinstance(I, (int, sympy.Integer)) and abs(int(I)) == 1:
                is_whole = True
                
            if R == sympy.ZZ and not is_whole:
                if isinstance(I, (int, sympy.Integer)):
                    H2 = (I != 0)
                elif hasattr(I, 'gens'):
                    H2 = any(g != 0 for g in I.gens)
                    
        # If I is the whole ring, R/I is the zero ring (finite), and I has no primary decomposition.
        if is_whole:
            H2 = True
            neg_Q = True
            return [H1, H2, neg_Q]
            
        # If I is a proper ideal and R/I is finite, it mathematically ALWAYS has a primary decomposition.
        neg_Q = False
        return [H1, H2, neg_Q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The quotient ring R/I is a finite ring",
    "¬Q: The ideal I does not have a primary decomposition in R"
]

N_HYP = 2
NEG_Q_INDEX = 2