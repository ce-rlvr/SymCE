import sympy

Z = sympy.S.Integers
Q = sympy.S.Rationals
R_field = sympy.S.Reals
C = sympy.S.Complexes
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Witness is expected to be a tuple: (R, S, A, f)
    where R and S are rings (iterables or SymPy sets like Z),
    A is a subring of R (iterable),
    and f is a dict or callable mapping elements of R to S.
    """
    try:
        R, S, A, f = witness
    except Exception:
        return [False, False, False]
    
    def is_ring(ring):
        if ring in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            return True
        try:
            ring_list = list(ring)
        except TypeError:
            return False
        if not ring_list:
            return False
        for x in ring_list:
            for y in ring_list:
                if (x + y) not in ring_list: return False
                if (x - y) not in ring_list: return False
                if (x * y) not in ring_list: return False
        return True

    def is_subring(sub, ring):
        try:
            sub_list = list(sub)
        except TypeError:
            return False
        if not sub_list:
            return False
        
        if ring in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            if not all(a in ring for a in sub_list):
                return False
        else:
            try:
                ring_list = list(ring)
            except TypeError:
                return False
            if not all(a in ring_list for a in sub_list):
                return False
                
        for x in sub_list:
            for y in sub_list:
                if (x + y) not in sub_list: return False
                if (x - y) not in sub_list: return False
                if (x * y) not in sub_list: return False
        return True

    # H1: R and S are rings
    try:
        h1_ok = is_ring(R) and is_ring(S)
    except Exception:
        h1_ok = False

    # H2: A is a subring of R
    try:
        h2_ok = is_subring(A, R)
    except Exception:
        h2_ok = False

    # neg_Q: The image f(A) is NOT a subring of S
    try:
        if isinstance(f, dict):
            img = [f[a] for a in A]
        elif callable(f):
            img = [f(a) for a in A]
        else:
            raise ValueError("f must be a dict or callable")
        
        # Remove duplicates without requiring elements to be hashable
        img_unique = []
        for item in img:
            if item not in img_unique:
                img_unique.append(item)
                
        neg_q_ok = not is_subring(img_unique, S)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: A is a subring of R",
    "¬Q: The image f(A) is not a subring of S"
]

N_HYP = 2
NEG_Q_INDEX = 2