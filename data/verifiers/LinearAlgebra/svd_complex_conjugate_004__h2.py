import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    # H_1: A is an m \times n matrix over the complex numbers.
    try:
        h1_ok = bool(hasattr(witness, 'is_Matrix') and witness.is_Matrix)
        if h1_ok:
            for e in witness:
                if e.is_complex is False:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # ¬Q: The multiset of singular values of \bar{A} is NOT identical to the multiset of singular values of A.
    try:
        neg_q_ok = False
        if h1_ok:
            sv_A = witness.singular_values()
            sv_A_bar = witness.conjugate().singular_values()
            
            if len(sv_A) != len(sv_A_bar):
                neg_q_ok = True
            else:
                # Try numerical comparison first for speed and reliability on concrete matrices
                try:
                    sv_A_num = sorted([float(v.evalf()) for v in sv_A])
                    sv_A_bar_num = sorted([float(v.evalf()) for v in sv_A_bar])
                    for u, v in zip(sv_A_num, sv_A_bar_num):
                        if abs(u - v) > 1e-9:
                            neg_q_ok = True
                            break
                except Exception:
                    # Fallback to symbolic comparison for matrices with symbolic entries
                    sv_A_sym = list(sv_A)
                    sv_A_bar_sym = list(sv_A_bar)
                    
                    for v in sv_A_sym:
                        found = False
                        for i, v_bar in enumerate(sv_A_bar_sym):
                            diff = v - v_bar
                            if diff == 0 or diff.equals(0):
                                sv_A_bar_sym.pop(i)
                                found = True
                                break
                        if not found:
                            neg_q_ok = True
                            break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over the complex numbers",
    "¬Q: The multiset of singular values of \\bar{A} is NOT identical to the multiset of singular values of A"
]

N_HYP = 1
NEG_Q_INDEX = 1