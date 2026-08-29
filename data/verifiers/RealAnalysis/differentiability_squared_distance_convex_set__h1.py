import sympy
from sympy import Set, Interval, Union, FiniteSet
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample.
    The witness should be a set K in R^n, represented as a list/tuple of points,
    or a sympy Set.
    """
    try:
        h1 = False
        neg_q = False
        
        # Check if it's a single sympy Point
        if hasattr(witness, 'is_Point'):
            is_pt = witness.is_Point() if callable(witness.is_Point) else witness.is_Point
            if is_pt:
                # A single point is a non-empty set, and its distance function is differentiable
                return [True, False]
                
        # Check if it's a sympy geometry object with an is_convex property/method
        if hasattr(witness, 'is_convex'):
            try:
                convex = witness.is_convex() if callable(witness.is_convex) else witness.is_convex
                if isinstance(convex, bool):
                    # If it's convex, d_K^2 is differentiable (neg_q = False)
                    # If it's not convex, d_K^2 is not differentiable everywhere (neg_q = True)
                    return [True, not convex]
            except Exception:
                pass
                
        # Check if it's a sympy Set
        if isinstance(witness, Set):
            is_emp = witness.is_empty
            if is_emp is True:
                return [False, False]
            h1 = True
            
            # For 1D sets, convexity determines differentiability of the squared distance
            if isinstance(witness, Interval):
                neg_q = False
            elif isinstance(witness, FiniteSet):
                neg_q = len(witness) > 1
            elif isinstance(witness, Union):
                neg_q = True
            else:
                # Default fallback for other sets: assume non-convex if not explicitly an Interval
                neg_q = True
            return [h1, neg_q]
            
        # Reject strings to avoid treating them as iterables of characters
        if isinstance(witness, str):
            return [False, False]
            
        # Try to treat the witness as an iterable of points
        try:
            points = list(witness)
        except TypeError:
            return [False, False]
            
        if len(points) == 0:
            return [False, False]
            
        normalized_points = []
        for pt in points:
            if isinstance(pt, (int, float)):
                normalized_points.append((float(pt),))
            elif isinstance(pt, (list, tuple)):
                normalized_points.append(tuple(float(x) for x in pt))
            else:
                try:
                    normalized_points.append((float(pt),))
                except Exception:
                    try:
                        normalized_points.append(tuple(float(x) for x in pt))
                    except Exception:
                        return [False, False]
                        
        # Ensure all points have the same dimension
        dim = len(normalized_points[0])
        if not all(len(pt) == dim for pt in normalized_points):
            return [False, False]
            
        h1 = True
        
        # For a finite set of points, the squared distance function is continuously
        # differentiable everywhere if and only if the set contains exactly 1 point (i.e. is convex).
        unique_points = set(normalized_points)
        neg_q = len(unique_points) >= 2
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: K is a non-empty set in R^n",
    "¬Q: d_K^2 is not continuously differentiable everywhere"
]

N_HYP = 1
NEG_Q_INDEX = 1