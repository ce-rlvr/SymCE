import sympy as sp

# Top-level setup
# No specific named bindings needed for this domain.

def parse_element(expr):
    if isinstance(expr, (tuple, list)) and len(expr) == 2:
        try:
            return int(expr[0]), int(expr[1])
        except (ValueError, TypeError):
            pass
    try:
        expr = sp.sympify(expr)
        if expr.is_Integer:
            return int(expr), 0
        re, im = expr.as_real_imag()
        x_sym = sp.simplify(re)
        y_sym = sp.simplify(im / sp.sqrt(2))
        if x_sym.is_Integer and y_sym.is_Integer:
            return int(x_sym), int(y_sym)
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            a_parsed = parse_element(witness[0])
            b_parsed = parse_element(witness[1])
            
            if a_parsed is not None and b_parsed is not None:
                h1 = True
                a = a_parsed
                b = b_parsed
                
                if b != (0, 0):
                    b_norm = b[0]**2 + 2*b[1]**2
                    
                    real_num = a[0]*b[0] + 2*a[1]*b[1]
                    imag_num = a[1]*b[0] - a[0]*b[1]
                    
                    q1 = round(real_num / b_norm)
                    q2 = round(imag_num / b_norm)
                    
                    found_valid_r = False
                    for dq1 in [-2, -1, 0, 1, 2]:
                        for dq2 in [-2, -1, 0, 1, 2]:
                            cq1 = q1 + dq1
                            cq2 = q2 + dq2
                            
                            r0 = a[0] - (b[0]*cq1 - 2*b[1]*cq2)
                            r1 = a[1] - (b[0]*cq2 + b[1]*cq1)
                            
                            r_norm = r0**2 + 2*r1**2
                            if r_norm < b_norm:
                                found_valid_r = True
                                break
                        if found_valid_r:
                            break
                    
                    neg_q = not found_valid_r
                else:
                    neg_q = False
                return [h1, neg_q]
                
        if isinstance(witness, str):
            w_str = witness.replace(" ", "")
            if "sqrt(-2)" in w_str or w_str == "R":
                h1 = True
                neg_q = False
                return [h1, neg_q]
                
        if hasattr(witness, "__str__"):
            w_str = str(witness).replace(" ", "")
            if "sqrt(-2)" in w_str:
                h1 = True
                neg_q = False
                return [h1, neg_q]

    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is the ring Z adjoin sqrt(-2)",
    "neg_Q: R is not a Euclidean domain with Euclidean function N"
]
N_HYP = 1
NEG_Q_INDEX = 1