import math
import itertools
import functools

# Top-level setup
S3 = None
Z4 = None
I2 = None

def conditions(witness):
    try:
        x_n = witness['x_n']
        x = witness['x']
        f = witness['f']
        n_k = witness['n_k']
        
        d_X = witness.get('d_X', lambda a, b: abs(a - b))
        d_Y = witness.get('d_Y', lambda a, b: abs(a - b))
        
        # H1: (X, d_X) and (Y, d_Y) are metric spaces
        h1_ok = True
        try:
            pts_X = [x]
            try: pts_X.append(x_n(1))
            except Exception: pass
            try: pts_X.append(x_n(2))
            except Exception: pass
            if isinstance(x, (int, float)):
                pts_X.append(x + 1.0)
                if d_X(x, x + 1.0) < 1e-7:
                    h1_ok = False
                
            pts_Y = []
            for p in pts_X:
                try: pts_Y.append(f(p))
                except Exception: pass
                
            for a in pts_X:
                for b in pts_X:
                    if d_X(a, b) < -1e-7: h1_ok = False
                    if d_X(a, a) > 1e-7: h1_ok = False
                    if abs(d_X(a, b) - d_X(b, a)) > 1e-7: h1_ok = False
                    for c in pts_X:
                        if d_X(a, c) > d_X(a, b) + d_X(b, c) + 1e-7: h1_ok = False
                        
            for a in pts_Y:
                for b in pts_Y:
                    if d_Y(a, b) < -1e-7: h1_ok = False
                    if d_Y(a, a) > 1e-7: h1_ok = False
                    if abs(d_Y(a, b) - d_Y(b, a)) > 1e-7: h1_ok = False
                    for c in pts_Y:
                        if d_Y(a, c) > d_Y(a, b) + d_Y(b, c) + 1e-7: h1_ok = False
        except Exception:
            h1_ok = False

        # H2: x is a subsequential limit of (x_n)
        h2_ok = True
        try:
            prev_n = -1
            for k in range(1, 10):
                nk = n_k(k)
                if not isinstance(nk, int) or nk <= prev_n:
                    h2_ok = False
                    break
                prev_n = nk
                
            if h2_ok:
                converges = False
                k = 100
                for _ in range(20):
                    try:
                        nk = n_k(k)
                        val = x_n(nk)
                        if d_X(val, x) < 1e-2:
                            converges = True
                            break
                    except Exception:
                        pass
                    k *= 2
                if not converges:
                    h2_ok = False
        except Exception:
            h2_ok = False

        # H3: f is a continuous function
        h3_ok = True
        try:
            if isinstance(x, (int, float)):
                pt = x
                is_continuous_at_pt = True
                is_discrete = True
                for sign in [1, -1]:
                    sign_continuous = False
                    delta = 0.1
                    for _ in range(20):
                        try:
                            perturbed = pt + sign * delta
                            dist_x = d_X(perturbed, pt)
                            if dist_x > 0 and dist_x < 1e-3:
                                is_discrete = False
                                dist_y = d_Y(f(perturbed), f(pt))
                                if dist_y < 1e-2:
                                    sign_continuous = True
                                    break
                        except Exception:
                            pass
                        delta /= 10.0
                    if not is_discrete and not sign_continuous:
                        is_continuous_at_pt = False
                
                if not is_discrete and not is_continuous_at_pt:
                    h3_ok = False
        except Exception:
            h3_ok = False

        # neg_Q: f(x) is NOT a subsequential limit of (f(x_n)) in Y
        neg_q_ok = True
        try:
            fx = f(x)
            k = 100
            for _ in range(20):
                try:
                    nk = n_k(k)
                    if d_Y(f(x_n(nk)), fx) < 0.05:
                        neg_q_ok = False
                        break
                except Exception:
                    pass
                k *= 2
                    
            if neg_q_ok:
                for n in range(1000, 2000):
                    try:
                        if d_Y(f(x_n(n)), fx) < 0.05:
                            neg_q_ok = False
                            break
                    except Exception:
                        pass
        except Exception:
            neg_q_ok = False

        return [h1_ok, h2_ok, h3_ok, neg_q_ok]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: x is a subsequential limit of (x_n)",
    "H_3: f is a continuous function",
    "¬Q: f(x) is not a subsequential limit of (f(x_n))"
]

N_HYP = 3
NEG_Q_INDEX = 3