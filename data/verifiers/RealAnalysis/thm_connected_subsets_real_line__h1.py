import sympy

# Top-level setup
x, y, z = sympy.symbols('x y z')

def is_interval(witness):
    """
    Checks if the witness is mathematically an interval in the real line.
    """
    if witness == sympy.S.EmptySet:
        return True
    if isinstance(witness, sympy.Interval):
        return True
    if isinstance(witness, sympy.FiniteSet) and len(witness) == 1:
        elem = list(witness)[0]
        if hasattr(elem, 'is_real') and elem.is_real:
            return True
        return False
    if witness == sympy.S.Reals:
        return True
    return False

def is_connected(witness):
    """
    Checks if the witness is a connected set.
    """
    if witness == sympy.S.EmptySet:
        return True
    if isinstance(witness, sympy.FiniteSet):
        return len(witness) <= 1
    if isinstance(witness, sympy.Interval):
        return True
    if witness == sympy.S.Reals:
        return True
    if isinstance(witness, sympy.ProductSet):
        return all(is_connected(factor) for factor in witness.args)
    if isinstance(witness, sympy.Union):
        # SymPy automatically simplifies unions of overlapping intervals.
        # If it remains a Union, its components are disjoint.
        return False
    
    # Handle regions in the complex plane
    if type(witness).__name__ == 'ComplexRegion':
        return is_connected(witness.sets)
        
    # Handle standard geometry objects which are connected
    geom_types = ('Curve', 'Ellipse', 'Polygon', 'Segment', 'Ray', 'Line', 'Circle', 'Triangle')
    if type(witness).__name__ in geom_types:
        return True
        
    for base in type(witness).__bases__:
        if base.__name__ in geom_types:
            return True

    return False

def conditions(witness):
    try:
        # Hypothesis 1: ℝ is equipped with the standard topology
        # This is a contextual hypothesis that holds for the space itself.
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # Conclusion: S is connected if and only if S is an interval
        connected = is_connected(witness)
        interval = is_interval(witness)
        q = (connected == interval)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: ℝ is equipped with the standard topology",
    "¬Q: S is connected but not an interval, or S is an interval but not connected"
]

N_HYP = 1
NEG_Q_INDEX = 1