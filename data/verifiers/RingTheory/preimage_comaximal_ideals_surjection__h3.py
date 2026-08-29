import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    def extract_params(w):
        n, m = 0, 0
        a, b = None, None
        
        if not isinstance(w, (dict, list, tuple)):
            w_dict = {}
            for key in ['R', 'S', 'I', 'J', 'n', 'm', 'a', 'b']:
                if hasattr(w, key):
                    w_dict[key] = getattr(w, key)
            if w_dict:
                w = w_dict

        if isinstance(w, dict):
            # Extract R
            R_val = w.get('R', w.get('n', 0))
            if R_val in (sympy.ZZ, 'Z', 'ZZ', sympy.QQ, 'Q', 'QQ'):
                n = 0
            else:
                try: n = int(R_val)
                except: pass
                
            # Extract S
            S_val = w.get('S', w.get('m', 0))
            if S_val in (sympy.ZZ, 'Z', 'ZZ', sympy.QQ, 'Q', 'QQ'):
                m = 0
            else:
                try: m = int(S_val)
                except: pass
                
            # Extract I
            I_val = w.get('I', w.get('a'))
            if hasattr(I_val, 'gens') and I_val.gens:
                a = I_val.gens[0]
            elif isinstance(I_val, (list, tuple, set)) and len(I_val) > 0:
                a = list(I_val)[0]
            else:
                a = I_val
                
            # Extract J
            J_val = w.get('J', w.get('b'))
            if hasattr(J_val, 'gens') and J_val.gens:
                b = J_val.gens[0]
            elif isinstance(J_val, (list, tuple, set)) and len(J_val) > 0:
                b = list(J_val)[0]
            else:
                b = J_val
                
        elif isinstance(w, (list, tuple)):
            if len(w) >= 4:
                try:
                    n, m = int(w[0]), int(w[1])
                    a, b = w[2], w[3]
                except:
                    pass
            elif len(w) == 2:
                a, b = w[0], w[1]
                    
        return n, m, a, b

    try:
        n, m, a, b = extract_params(witness)
        if a is None or b is None:
            return [False, False, False]
            
        # H1: R and S are rings
        h1 = (n >= 0 and m >= 0)
        
        # H2: f is a surjective ring homomorphism
        if m == 0:
            h2 = (n == 0)
        else:
            h2 = (n % m == 0)
            
        # Conclusion: f^{-1}(I) and f^{-1}(J) are comaximal in R
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        g = sympy.gcd(a_sym, b_sym)
        if m != 0:
            g = sympy.gcd(g, sympy.sympify(m))
            
        try:
            is_unit = (abs(int(g)) == 1)
        except Exception:
            is_unit = getattr(g, 'is_number', False) and g != 0
            
        neg_q = not is_unit
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f is a surjective ring homomorphism",
    "¬Q: f^{-1}(I) and f^{-1}(J) are not comaximal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2