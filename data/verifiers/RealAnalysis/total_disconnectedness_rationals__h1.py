import sympy
from sympy import Set, Interval, Union, Intersection, FiniteSet, S
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects required for this real analysis conjecture)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture.
    
    The conjecture claims that any space equipped with the subspace topology 
    inherited from the standard topology on ℝ (e.g., ℚ) is totally disconnected.
    While true for ℚ, it is false in general for arbitrary subsets of ℝ.
    """
    
    # H_1: The space is equipped with the subspace topology inherited from the standard topology on ℝ
    # We interpret this as the witness being a valid subset of the real numbers.
    try:
        h1 = isinstance(witness, Set) and witness.is_subset(S.Reals)
    except Exception:
        h1 = False

    # ¬Q: The space is NOT totally disconnected
    # A subset of ℝ is not totally disconnected if and only if it contains a non-degenerate interval.
    # In SymPy, this is generally equivalent to having a strictly positive Lebesgue measure.
    try:
        def contains_interval(s):
            # First, try to use the Lebesgue measure as a heuristic
            try:
                m = s.measure
                if m.is_extended_real:
                    if m > 0:
                        return True
                    elif m == 0:
                        return False
            except Exception:
                pass

            # Fallback to structural checks
            if isinstance(s, Interval):
                return s.start < s.end
            if isinstance(s, Union):
                return any(contains_interval(arg) for arg in s.args)
            if s == S.Reals:
                return True
            if isinstance(s, FiniteSet):
                return False
            if s in (S.Rationals, S.Integers, S.Naturals, S.Naturals0):
                return False
            
            return False

        neg_q = bool(contains_interval(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The space is equipped with the subspace topology inherited from the standard topology on ℝ",
    "¬Q: The space is not totally disconnected"
]

N_HYP = 1
NEG_Q_INDEX = 1