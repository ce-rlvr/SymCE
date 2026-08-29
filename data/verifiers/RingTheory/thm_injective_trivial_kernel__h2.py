import sympy
from sympy import symbols

# Standard finite rings (represented by their underlying sets, with 0 as the zero element)
Z2 = [0, 1]
Z3 = [0, 1, 2]
Z4 = [0, 1, 2, 3]
Z5 = [0, 1, 2, 3, 4]
Z6 = [0, 1, 2, 3, 4, 5]

def parse_witness(witness):
    """
    Helper to extract R, S, and the function dictionary from the witness.
    Supports witness as (R, S, f) or just f as a dictionary.
    """
    if isinstance(witness, (tuple, list)) and len(witness) == 3:
        R, S, f = witness
        if callable(f):
            f_dict = {x: f(x) for x in R}
        elif isinstance(f, dict):
            f_dict = f
        else:
            return None, None, None
        return R, S, f_dict
    elif isinstance(witness, dict):
        f_dict = witness
        R = list(f_dict.keys())
        S = list(set(f_dict.values()) | {0})
        return R, S, f_dict
    return None, None, None

def conditions(witness) -> list[bool]:
    # H_1: R and S are rings (we check they are valid domains containing 0) 
    # and f is a well-defined function from R to S.
    try:
        R, S, f_dict = parse_witness(witness)
        if R is None:
            h1 = False
        else:
            h1 = (0 in R) and (0 in S) and (set(f_dict.keys()) == set(R)) and all(v in S for v in f_dict.values())
    except Exception:
        h1 = False

    # ¬Q: The equivalence (f is injective iff ker(f) = {0_R}) FAILS.
    try:
        R, S, f_dict = parse_witness(witness)
        if R is None:
            neg_q = False
        else:
            # Check if f is injective
            is_injective = len(set(f_dict.values())) == len(R)
            
            # Check if ker(f) == {0_R}
            ker_f = {x for x in R if f_dict[x] == 0}
            ker_is_zero = (ker_f == {0})
            
            # The conclusion is the equivalence of the two
            q = (is_injective == ker_is_zero)
            
            # We want the conclusion to FAIL
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R and S are rings and f is a function from R to S",
    "¬Q: The equivalence (f is injective iff ker(f) = {0_R}) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1