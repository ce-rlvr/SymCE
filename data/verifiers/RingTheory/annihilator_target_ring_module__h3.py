import itertools

def conditions(witness):
    """
    Given a witness (R, S, f), checks the hypotheses and the negated conclusion.
    R and S are expected to be iterables of elements supporting +, *, and ==.
    f is expected to be a callable mapping elements of R to elements of S.
    """
    try:
        R, S, f = witness
    except Exception:
        return [False, False, False, False]

    # Helper functions to find zero and identity elements
    def get_zero(ring):
        for e in ring:
            if all(x + e == x for x in ring) and all(e + x == x for x in ring):
                return e
        return None

    def get_one(ring):
        for e in ring:
            if all(x * e == x for x in ring) and all(e * x == x for x in ring):
                return e
        return None

    # H1: R and S are rings with identity
    try:
        zero_R = get_zero(R)
        one_R = get_one(R)
        zero_S = get_zero(S)
        one_S = get_one(S)
        
        h1 = (zero_R is not None) and (one_R is not None) and \
             (zero_S is not None) and (one_S is not None)
    except Exception:
        h1 = False

    # H2: f is a ring homomorphism from R to S
    try:
        h2 = True
        for x in R:
            for y in R:
                if f(x + y) != f(x) + f(y):
                    h2 = False
                if f(x * y) != f(x) * f(y):
                    h2 = False
    except Exception:
        h2 = False

    # H3: S is equipped with a left R-module structure defined by r * s = f(r)s
    # We check the basic module axioms (distributivity and associativity of action).
    try:
        h3 = True
        for r in R:
            for s1 in S:
                for s2 in S:
                    if f(r) * (s1 + s2) != (f(r) * s1) + (f(r) * s2):
                        h3 = False
        for r1 in R:
            for r2 in R:
                for s in S:
                    if f(r1 + r2) * s != (f(r1) * s) + (f(r2) * s):
                        h3 = False
                    if f(r1 * r2) * s != f(r1) * (f(r2) * s):
                        h3 = False
    except Exception:
        h3 = False

    # neg_Q: The annihilator of S as an R-module is exactly the kernel of f (must FAIL)
    # The conclusion asserts Ann_R(S) == ker(f).
    # It also implicitly asserts that S is a valid (unital) R-module.
    # If S is not a unital R-module, the premise of the conclusion fails, making it false.
    try:
        # Check if S is a unital R-module
        is_unital_module = True
        if one_R is not None:
            for s in S:
                if f(one_R) * s != s:
                    is_unital_module = False

        # Compute Ann_R(S)
        ann_R = []
        for r in R:
            if all(f(r) * s == zero_S for s in S):
                ann_R.append(r)
                
        # Compute ker(f)
        ker_f = []
        for r in R:
            if f(r) == zero_S:
                ker_f.append(r)
                
        # Check set equality
        ann_in_ker = all(any(a == k for k in ker_f) for a in ann_R)
        ker_in_ann = all(any(k == a for a in ann_R) for k in ker_f)
        sets_equal = ann_in_ker and ker_in_ann
        
        # The conclusion fails if the sets are not equal OR if S is not a valid unital R-module
        neg_q = (not sets_equal) or (not is_unital_module)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: S is equipped with a left R-module structure defined by r * s = f(r)s",
    "¬Q: The annihilator of S as an R-module is NOT exactly the kernel of f (or S is not a valid unital R-module)"
]

N_HYP = 3
NEG_Q_INDEX = 3