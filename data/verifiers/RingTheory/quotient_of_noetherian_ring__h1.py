import sympy
from sympy import symbols, Rational, Integer
from sympy.polys.domains import ZZ, QQ

# Top-level setup
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks if the witness is a counterexample to the conjecture:
    "If R is a Noetherian ring and I is an ideal of R, then R/I is a Noetherian ring."
    """
    try:
        # Extract R and I from the witness
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = witness.R
            I = witness.I
    except Exception:
        return [False, False, False]

    # H_1: R is a Noetherian ring
    def is_noetherian(ring):
        if hasattr(ring, 'is_Noetherian'):
            return bool(ring.is_Noetherian)
        if hasattr(ring, 'is_noetherian'):
            return bool(ring.is_noetherian() if callable(ring.is_noetherian) else ring.is_noetherian)
        
        # SymPy domains (like ZZ, QQ, PolyRing with finite generators) are Noetherian
        if hasattr(ring, 'is_Ring') or hasattr(ring, 'is_Field'):
            return True
            
        try:
            from sympy.polys.domains.ring import Ring
            if isinstance(ring, Ring):
                return True
        except ImportError:
            pass
            
        return False

    try:
        h1 = is_noetherian(R)
    except Exception:
        h1 = False

    # H_2: I is an ideal of R
    def is_ideal(ideal, ring):
        if hasattr(ideal, 'ring'):
            if ideal.ring == ring:
                return True
        try:
            from sympy.polys.agca.ideals import Ideal
            if isinstance(ideal, Ideal):
                if ideal.ring == ring:
                    return True
        except ImportError:
            pass
            
        if isinstance(ideal, (list, tuple, set)):
            try:
                # Check if all generators of the ideal belong to the ring
                if all(elem in ring for elem in ideal):
                    return True
            except Exception:
                pass
        return False

    try:
        h2 = is_ideal(I, R)
    except Exception:
        h2 = False

    # ¬Q: The quotient ring R/I is NOT a Noetherian ring
    def is_quotient_noetherian(ring, ideal):
        if hasattr(ring, 'quotient_ring'):
            try:
                Q = ring.quotient_ring(ideal)
                return is_noetherian(Q)
            except Exception:
                pass
        try:
            from sympy.polys.domains.quotientring import QuotientRing
            from sympy.polys.agca.ideals import Ideal
            if not isinstance(ideal, Ideal) and isinstance(ideal, (list, tuple, set)):
                ideal_obj = ring.ideal(*ideal)
            else:
                ideal_obj = ideal
            Q = QuotientRing(ring, ideal_obj)
            return is_noetherian(Q)
        except Exception:
            pass
        
        # Mathematically, if R is a Noetherian ring and I is an ideal, R/I is always Noetherian.
        # If we cannot explicitly construct the quotient but the hypotheses hold, 
        # the quotient is Noetherian by the fundamental theorem.
        if h1 and h2:
            return True
        return False

    try:
        q = is_quotient_noetherian(R, I)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: I is an ideal of R",
    "¬Q: The quotient ring R/I is not a Noetherian ring"
]

N_HYP = 2
NEG_Q_INDEX = 2