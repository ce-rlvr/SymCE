import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: T is a normal operator on V",
    "¬Q: The singular values of T are not the absolute values of the eigenvalues of T"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        H_1_ok = False
        if hasattr(witness, 'H') and hasattr(witness, 'shape'):
            if len(witness.shape) == 2 and witness.shape[0] == witness.shape[1]:
                diff = witness.H * witness - witness * witness.H
                if diff.is_zero_matrix == True:
                    H_1_ok = True
                else:
                    is_zero_num = True
                    try:
                        for e in diff:
                            if abs(complex(e)) > 1e-9:
                                is_zero_num = False
                                break
                    except Exception:
                        is_zero_num = None
                    
                    if is_zero_num is False:
                        H_1_ok = False
                    else:
                        if all(sympy.simplify(e) == 0 for e in diff):
                            H_1_ok = True
    except Exception:
        H_1_ok = False

    try:
        neg_Q_ok = False
        if hasattr(witness, 'singular_values') and hasattr(witness, 'eigenvals'):
            sv = witness.singular_values()
            evs = witness.eigenvals()
            
            # Determine if the operator is on a real vector space
            is_real_matrix = True
            for entry in witness:
                if not entry.is_real:
                    is_real_matrix = False
                    break
            
            abs_evs = []
            for ev, mult in evs.items():
                if is_real_matrix:
                    # For a real vector space, eigenvalues must be real
                    if ev.is_real:
                        abs_evs.extend([sympy.Abs(ev)] * mult)
                else:
                    # For a complex vector space, all complex eigenvalues are included
                    abs_evs.extend([sympy.Abs(ev)] * mult)
            
            if len(sv) != len(abs_evs):
                neg_Q_ok = True
            else:
                used = [False] * len(abs_evs)
                matched_all = True
                for s in sv:
                    matched = False
                    for i, a in enumerate(abs_evs):
                        if not used[i]:
                            diff = s - a
                            is_zero = False
                            try:
                                if abs(complex(diff)) < 1e-9:
                                    is_zero = True
                            except Exception:
                                pass
                            
                            if not is_zero:
                                diff_simp = sympy.simplify(diff)
                                if diff_simp == 0:
                                    is_zero = True
                                else:
                                    try:
                                        if abs(complex(diff_simp)) < 1e-9:
                                            is_zero = True
                                    except Exception:
                                        pass
                            
                            if is_zero:
                                used[i] = True
                                matched = True
                                break
                    if not matched:
                        matched_all = False
                        break
                neg_Q_ok = not matched_all
    except Exception:
        neg_Q_ok = False

    return [H_1_ok, neg_Q_ok]