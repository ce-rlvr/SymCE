import sympy
from sympy import S, Interval, FiniteSet, Union, Intersection, ProductSet

# Top-level setup
Reals = S.Reals
Naturals = S.Naturals
Integers = S.Integers
Rationals = S.Rationals
Complexes = S.Complexes
EmptySet = S.EmptySet

def _is_compact(witness):
    """Helper function to determine if a SymPy Set is compact in its standard topology."""
    if witness == S.EmptySet:
        return True
    if isinstance(witness, sympy.ProductSet):
        return all(_is_compact(arg) for arg in witness.args)
    if isinstance(witness, sympy.Set):
        if witness.is_subset(S.Reals) == True:
            # Boundedness
            bounded = False
            try:
                if witness.inf.is_finite and witness.sup.is_finite:
                    bounded = True
            except Exception:
                pass
            
            # Closedness
            closed = False
            try:
                if hasattr(witness, 'boundary') and witness.boundary is not None:
                    bnd = witness.boundary
                    if bnd.is_subset(witness) == True:
                        closed = True
                    elif bnd.is_subset(witness) == False:
                        closed = False
                    else:
                        raise ValueError("Cannot determine subset")
                else:
                    raise ValueError("No boundary")
            except Exception:
                # Fallback closedness checks
                if isinstance(witness, sympy.Interval):
                    closed = not witness.left_open and not witness.right_open
                elif isinstance(witness, sympy.FiniteSet):
                    closed = True
                elif witness in (S.Reals, S.Integers, S.Naturals):
                    closed = True
            
            return bounded and closed
        elif isinstance(witness, sympy.FiniteSet):
            return True
    return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    Remaining hypotheses:
      H_1: X is a metric space
      
    Conclusion to falsify:
      Q: X is a compact metric space
    """
    # H_1: X is a metric space
    try:
        h1 = False
        if isinstance(witness, sympy.Set):
            # Subsets of R or C, or their products, are standard metric spaces
            if witness.is_subset(S.Reals) == True or witness.is_subset(S.Complexes) == True:
                h1 = True
            elif isinstance(witness, sympy.ProductSet):
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: X is NOT a compact metric space
    try:
        neg_q = not _is_compact(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "¬Q: X is not a compact metric space"
]

N_HYP = 1
NEG_Q_INDEX = 1