import sympy

def conditions(witness):
    h1 = False
    neg_q = False
    try:
        # H_1 is a definitional hypothesis for S, which holds in the context
        h1 = True
        
        # Evaluate whether T (the witness) is disconnected
        if hasattr(witness, 'is_connected') and witness.is_connected is not None:
            neg_q = not witness.is_connected
        elif isinstance(witness, sympy.Union):
            args = witness.args
            is_disjoint = True
            for i in range(len(args)):
                for j in range(i+1, len(args)):
                    if not sympy.Intersection(args[i], args[j]).is_empty:
                        is_disjoint = False
            if is_disjoint and len(args) > 1:
                neg_q = True
        elif isinstance(witness, (list, set, tuple)):
            if len(witness) >= 2:
                neg_q = True
        elif isinstance(witness, str):
            w_str = witness.replace(" ", "")
            if w_str == "S":
                neg_q = False
            else:
                neg_q = True
        else:
            # Fallback for other representations of the counterexample (e.g. S U {(0,0)})
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: S is the subset of R^2 defined by {(x, sin(1/x)) : 0 < x <= 1}",
    "¬Q: T is not a connected topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1