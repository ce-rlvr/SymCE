import sympy
from sympy import Interval, FiniteSet, Point, Polygon, Segment
from sympy.sets.sets import ProductSet
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = True  # p_K being the Minkowski functional is definitional
    neg_q = False
    
    try:
        # If witness is provided as a tuple (K, p_K), extract K
        if isinstance(witness, tuple) and len(witness) == 2:
            witness = witness[0]

        if isinstance(witness, Interval):
            h1 = (not witness.left_open) and (not witness.right_open) and witness.is_bounded
            a, b = witness.start, witness.end
            # 0 is in the interior iff a < 0 < b
            zero_in_int = (a < 0) and (b > 0)
            neg_q = not zero_in_int
            
        elif isinstance(witness, FiniteSet):
            # A finite set is closed and bounded. It is convex iff it has exactly 1 point.
            h1 = (len(witness) == 1)
            # A single point has empty interior in R^n (for n >= 1)
            zero_in_int = False
            neg_q = not zero_in_int
            
        elif isinstance(witness, ProductSet):
            h1 = True
            zero_in_int = True
            for s in witness.sets:
                if isinstance(s, Interval):
                    if s.left_open or s.right_open or not s.is_bounded:
                        h1 = False
                    if not (s.start < 0 and s.end > 0):
                        zero_in_int = False
                elif isinstance(s, FiniteSet):
                    if len(s) != 1:
                        h1 = False
                    zero_in_int = False
                else:
                    h1 = False
                    zero_in_int = False
            neg_q = not zero_in_int
            
        elif isinstance(witness, Polygon):
            h1 = witness.is_convex()
            dim = len(witness.vertices[0])
            origin = Point(*[0]*dim)
            # encloses_point returns True if the point is strictly inside (in the interior)
            zero_in_int = witness.encloses_point(origin)
            neg_q = not zero_in_int
            
        elif isinstance(witness, Segment):
            h1 = True
            # A segment in 2D or higher has empty interior
            zero_in_int = False
            neg_q = not zero_in_int
            
        elif isinstance(witness, Point):
            h1 = True
            zero_in_int = False
            neg_q = not zero_in_int
            
        elif isinstance(witness, dict):
            # Fallback for custom mock objects
            h1 = bool(witness.get("is_closed", False) and 
                      witness.get("is_bounded", False) and 
                      witness.get("is_convex", False))
            zero_in_int = bool(witness.get("zero_in_interior", False))
            neg_q = not zero_in_int

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a closed, bounded, and convex set",
    "H_2: p_K is the Minkowski functional",
    "not Q: p_K is not globally Lipschitz continuous on R^n"
]

N_HYP = 2
NEG_Q_INDEX = 2