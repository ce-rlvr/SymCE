import sympy
from sympy import Interval, FiniteSet, Union, Intersection, S, oo

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: {K_n} is a sequence of non-empty subsets of X",
    "H_3: Each K_n is compact",
    "¬Q: The intersection is empty"
]

def conditions(witness):
    def get_set(w, n):
        if callable(w):
            return w(n)
        else:
            return w[n - 1]

    # H_1: (X, d) is a metric space
    # We assume the witness provides subsets of Reals, which is a metric space.
    try:
        # Verify we can get the first set to ensure witness is somewhat valid
        _ = get_set(witness, 1)
        h1 = True
    except Exception:
        h1 = False

    # H_2: {K_n} is a sequence of non-empty subsets of X
    h2 = True
    try:
        for n in range(1, 101):
            s = get_set(witness, n)
            if s.is_empty:
                h2 = False
                break
    except Exception:
        h2 = False

    # H_3: Each K_n is compact
    h3 = True
    try:
        for n in range(1, 101):
            s = get_set(witness, n)
            
            def is_compact(st):
                if st.is_empty:
                    return True
                if not st.is_subset(S.Reals):
                    return False
                if not (st.inf.is_finite and st.sup.is_finite):
                    return False
                
                def is_closed(st_inner):
                    if isinstance(st_inner, Interval):
                        return not st_inner.left_open and not st_inner.right_open
                    elif isinstance(st_inner, FiniteSet):
                        return True
                    elif isinstance(st_inner, Union):
                        return all(is_closed(arg) for arg in st_inner.args)
                    else:
                        try:
                            return st_inner.closure == st_inner
                        except Exception:
                            return False
                return is_closed(st)
                
            if not is_compact(s):
                h3 = False
                break
    except Exception:
        h3 = False

    # ¬Q: The intersection is empty
    neg_q = False
    try:
        inter = get_set(witness, 1)
        for n in range(2, 101):
            inter = Intersection(inter, get_set(witness, n))
            if inter.is_empty:
                break
        neg_q = (inter.is_empty == True)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]