import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is a two-sided ideal of R",
    "¬Q: The map pi is not an epimorphism in the category of rings"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a ring and I is a two-sided ideal, then the canonical projection 
    pi: R -> R/I is an epimorphism in the category of rings."
    
    The conjecture fails in the category of unital rings if:
    1. R is a rng (non-unital ring), so R is not an object in the category.
    2. I = R, so R/I is the zero ring, which is not an object in the category 
       (under the convention that rings require 1 != 0).
    """
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        # Format 1: witness is an integer n, representing R = ZZ, I = n*ZZ
        if isinstance(witness, int):
            H1 = True
            H2 = True
            # neg_Q is True if I = ZZ (i.e., n = 1 or -1)
            if abs(witness) == 1:
                neg_Q = True
                
        # Format 2: witness is a tuple of two integers (r, i), representing R = r*ZZ, I = i*ZZ
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int) and isinstance(witness[1], int):
            r, i = witness
            H1 = True
            if r != 0 and i % r == 0:
                H2 = True
            elif r == 0 and i == 0:
                H2 = True
                
            # neg_Q is True if R has no identity (r != 1 and r != -1) OR I == R (abs(i) == abs(r))
            if abs(r) != 1 or (r != 0 and abs(i) == abs(r)) or (r == 0 and i == 0):
                neg_Q = True
                
        # Format 3: witness is a tuple (R, I) of sympy objects
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            # Check H1: R is a ring
            if hasattr(R, 'is_Ring') and R.is_Ring:
                H1 = True
            elif hasattr(R, 'is_ring') and R.is_ring:
                H1 = True
            elif R in [ZZ, QQ, RR, CC]:
                H1 = True
            elif type(R).__name__ == 'PolyRing':
                H1 = True
                
            # Check H2: I is a two-sided ideal of R
            if type(I).__name__ == 'Ideal' and hasattr(I, 'ring') and I.ring == R:
                H2 = True
            elif I == R:
                H2 = True
            elif hasattr(I, 'is_ideal') and I.is_ideal:
                H2 = True
            elif I == 0 or I == sympy.S.Zero or I == {0}:
                H2 = True
                
            # Check neg_Q: pi is not an epimorphism in the category of rings
            if H1 and H2:
                has_id = False
                if hasattr(R, 'has_Identity'):
                    has_id = R.has_Identity
                elif hasattr(R, 'one'):
                    has_id = True
                elif R in [ZZ, QQ, RR, CC]:
                    has_id = True
                    
                is_whole = False
                if I == R:
                    is_whole = True
                elif hasattr(I, 'is_whole_ring') and I.is_whole_ring():
                    is_whole = True
                elif hasattr(I, 'contains') and has_id and I.contains(R.one):
                    is_whole = True
                    
                # Fails to be an epimorphism in the category of unital rings if R lacks 1 or R/I is the zero ring
                if not has_id or is_whole:
                    neg_Q = True
                    
    except Exception:
        pass
        
    return [H1, H2, neg_Q]