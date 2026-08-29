import math

# Top-level setup
# (No specific named objects required for this domain; standard Python types are used)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (H1_dim, H2_dim, U, f, L)
    where:
      - H1_dim, H2_dim are non-negative integers representing the dimensions of the Hilbert spaces.
      - U is a list of tuples representing points in the domain of f.
      - f is a dictionary or list of pairs mapping points in U to points in H2.
      - L is a non-negative number representing the Lipschitz constant.
    """
    try:
        if len(witness) != 5:
            return [False, False, False]
        H1_dim, H2_dim, U, f, L = witness
    except Exception:
        return [False, False, False]
        
    # H1: H1 and H2 are Hilbert spaces
    try:
        h1_ok = isinstance(H1_dim, int) and H1_dim >= 0 and isinstance(H2_dim, int) and H2_dim >= 0
    except Exception:
        h1_ok = False
        
    # H2: f: U -> H2 is a Lipschitz continuous function with Lipschitz constant L
    try:
        h2_ok = True
        try:
            L_float = float(L)
            if L_float < 0:
                h2_ok = False
        except Exception:
            h2_ok = False
            
        if isinstance(f, dict):
            f_items = list(f.items())
        else:
            f_items = list(f)
            
        domain_f = [tuple(x) for x, y in f_items]
        try:
            U_tuples = [tuple(x) for x in U]
        except Exception:
            U_tuples = []
            h2_ok = False
        
        if set(U_tuples) != set(domain_f):
            h2_ok = False
            
        if U_tuples:
            k = len(U_tuples[0])
            for x in U_tuples:
                if len(x) != k:
                    h2_ok = False
                for val in x:
                    try:
                        float(val)
                    except Exception:
                        h2_ok = False
                        
        mapping = {}
        for x, y in f_items:
            if not isinstance(y, (tuple, list)):
                h2_ok = False
                continue
            if len(y) != H2_dim:
                h2_ok = False
            for val in y:
                try:
                    float(val)
                except Exception:
                    h2_ok = False
            x_tup = tuple(x)
            y_tup = tuple(y)
            if x_tup in mapping and mapping[x_tup] != y_tup:
                h2_ok = False
            mapping[x_tup] = y_tup
                    
        if h2_ok:
            items = list(mapping.items())
            for i in range(len(items)):
                for j in range(i, len(items)):
                    x1, y1 = items[i]
                    x2, y2 = items[j]
                    dist_x = math.sqrt(sum((float(a) - float(b))**2 for a, b in zip(x1, x2)))
                    dist_y = math.sqrt(sum((float(a) - float(b))**2 for a, b in zip(y1, y2)))
                    if dist_y > L_float * dist_x + 1e-9:
                        h2_ok = False
    except Exception:
        h2_ok = False
        
    # neg_Q: Conclusion fails
    try:
        neg_q = False
        # The conclusion states there exists F: H1 -> H2 extending f on U.
        # If U is not a subset of H1 (i.e. elements of U don't have dimension H1_dim),
        # then F cannot extend f on U because U is not in the domain of F.
        # If U is a subset of H1, Kirszbraun's theorem guarantees F exists, so conclusion holds.
        if U:
            if any(len(x) != H1_dim for x in U):
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H1 and H2 are Hilbert spaces",
    "H_2: f: U -> H2 is a Lipschitz continuous function with Lipschitz constant L",
    "¬Q: There does not exist F: H1 -> H2 extending f with Lipschitz constant L"
]

N_HYP = 2
NEG_Q_INDEX = 2