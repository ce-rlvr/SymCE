import sympy
from sympy import sympify

def conditions(witness):
    try:
        L = witness.get("L")
        K = witness.get("K")
        
        # H1: L is an algebraically closed field
        H1 = L in ["CC", "C", "AlgebraicClosure(QQ)", "AlgebraicClosure(Z)"]
        
        if not isinstance(K, (list, set, tuple)):
            return [False, False, False]
            
        K_set = set(sympify(c) for c in K)
        
        a = sympify(witness.get("a"))
        b = sympify(witness.get("b"))
        poly_a = [sympify(c) for c in witness.get("poly_a", [])]
        poly_b = [sympify(c) for c in witness.get("poly_b", [])]
        
        # H2: E is the set of all elements in L that are algebraic over K
        # We verify this by checking that the witness elements a and b are indeed in E.
        def is_in_E(poly, root):
            if not poly: return False
            if all(c == 0 for c in poly): return False
            for c in poly:
                if not any(c == k for k in K_set):
                    return False
            
            val = sum(c * (root ** i) for i, c in enumerate(poly))
            val = sympify(val)
            if val == 0: return True
            if val.simplify() == 0: return True
            if val.expand() == 0: return True
            return False
            
        H2 = is_in_E(poly_a, a) and is_in_E(poly_b, b)
        
        neg_Q = False
        
        # Check if E is not a field by showing a+b or a*b is not in E
        try:
            K_nums = [float(c) for c in K_set]
            same_sign = all(c >= 0 for c in K_nums) or all(c <= 0 for c in K_nums)
            all_int = all(float(c).is_integer() for c in K_set)
            max_c = max(abs(c) for c in K_nums) if K_nums else 0
        except Exception:
            same_sign = False
            all_int = False
            max_c = 0
            
        x_add = a + b
        x_mul = a * b
        
        def not_in_E(x):
            try:
                sx = sympify(x)
                # No positive real can be a root of a non-zero polynomial with same-sign coefficients
                if same_sign and sx.is_real == True and sx > 0:
                    return True
                # An integer x with |x| > max(|c|) cannot be a root of any polynomial over K
                if all_int and sx.is_integer == True:
                    if abs(sx) > max_c:
                        return True
            except Exception:
                pass
            return False
            
        if not_in_E(x_add) or not_in_E(x_mul):
            neg_Q = True
            
        return [bool(H1), bool(H2), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L is an algebraically closed field",
    "H_2: E is the set of all elements in L that are algebraic over K",
    "¬Q: E is not an algebraically closed field"
]

N_HYP = 2
NEG_Q_INDEX = 2