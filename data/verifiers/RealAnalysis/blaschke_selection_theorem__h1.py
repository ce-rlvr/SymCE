import sympy

# Top-level setup
Reals = sympy.S.Reals
Integers = sympy.S.Integers
Naturals = sympy.S.Naturals
Rationals = sympy.S.Rationals
EmptySet = sympy.S.EmptySet

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for any metric space X, the space of its non-empty 
    compact subsets K(X) with the Hausdorff metric is compact.
    This is false if X itself is not compact.
    """
    try:
        # Allow witness to be just the space (a sympy Set) or a tuple (Space, Metric)
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], sympy.Set):
            space = witness[0]
        else:
            space = witness
            
        # H1: K(X) is the set of all non-empty compact subsets of X
        # We interpret this as X being a valid metric space. 
        # For our purposes, any subset of Reals is a valid metric space.
        h1 = isinstance(space, sympy.Set) and (space.is_subset(sympy.S.Reals) == True)
    except Exception:
        h1 = False

    # H2: K(X) is equipped with the Hausdorff metric d_H induced by d
    # This is definitional and holds for any valid metric space X.
    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            # neg_Q: The metric space (K(X), d_H) is NOT compact.
            # For a metric space X, K(X) is compact iff X is compact.
            # A subset of Reals is compact iff it is closed and bounded.
            is_compact = True
            if space == sympy.S.EmptySet:
                is_compact = True
            else:
                inf = getattr(space, 'inf', None)
                sup = getattr(space, 'sup', None)
                
                # Check boundedness
                if inf is None or sup is None:
                    is_compact = False
                elif inf.is_infinite or sup.is_infinite:
                    is_compact = False
                else:
                    # Check closedness
                    try:
                        if space.boundary.is_subset(space) != True:
                            is_compact = False
                    except Exception:
                        # If we cannot determine closedness, assume not compact
                        is_compact = False
                        
            neg_q = not is_compact
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    r"H_1: \mathcal{K}(X) is the set of all non-empty compact subsets of X",
    r"H_2: \mathcal{K}(X) is equipped with the Hausdorff metric d_H induced by d",
    r"¬Q: The metric space (\mathcal{K}(X), d_H) is not compact"
]

N_HYP = 2
NEG_Q_INDEX = 2