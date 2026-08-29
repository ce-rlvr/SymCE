import sympy
from sympy import symbols, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "H_3: J is an ideal of R",
    "¬Q: S^{-1}(IJ) != (S^{-1}I)(S^{-1}J) as ideals in S^{-1}R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('ring')
            I = witness.get('I')
            J = witness.get('J')
            S = witness.get('S')
        elif isinstance(witness, tuple) and len(witness) == 4:
            R, I, J, S = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    h1 = False
    try:
        if hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif R in (sympy.ZZ, sympy.QQ):
            h1 = True
        elif isinstance(R, int) and R > 1:
            h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if h1:
            if hasattr(I, 'ring') and I.ring == R:
                h2 = True
            elif isinstance(R, int) and isinstance(I, (list, set, tuple)):
                I_set = set(i % R for i in I)
                if I_set:
                    add_closed = all((a + b) % R in I_set for a in I_set for b in I_set)
                    mult_closed = all((a * r) % R in I_set for a in I_set for r in range(R))
                    h2 = add_closed and mult_closed
    except Exception:
        pass

    h3 = False
    try:
        if h1:
            if hasattr(J, 'ring') and J.ring == R:
                h3 = True
            elif isinstance(R, int) and isinstance(J, (list, set, tuple)):
                J_set = set(j % R for j in J)
                if J_set:
                    add_closed = all((a + b) % R in J_set for a in J_set for b in J_set)
                    mult_closed = all((a * r) % R in J_set for a in J_set for r in range(R))
                    h3 = add_closed and mult_closed
    except Exception:
        pass

    neg_q = False
    try:
        if h1:
            if hasattr(R, 'is_commutative') or R in (sympy.ZZ, sympy.QQ):
                if isinstance(S, (list, set, tuple)) and len(S) > 0:
                    S_list = list(S)
                    try:
                        subset_of_R = all(a in R for a in S_list)
                    except Exception:
                        subset_of_R = True
                    
                    if not subset_of_R:
                        neg_q = True
                    else:
                        mult_closed = True
                        for a in S_list:
                            for b in S_list:
                                if (a * b) not in S_list:
                                    mult_closed = False
                                    break
                            if not mult_closed:
                                break
                        neg_q = not mult_closed
                else:
                    neg_q = True
            elif isinstance(R, int):
                if isinstance(S, (list, set, tuple)) and len(S) > 0:
                    S_set = set(s % R for s in S)
                    mult_closed = all((a * b) % R in S_set for a in S_set for b in S_set)
                    neg_q = not mult_closed
                else:
                    neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]