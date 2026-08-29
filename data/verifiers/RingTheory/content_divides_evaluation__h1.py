import sympy

def conditions(witness):
    try:
        if isinstance(witness, dict):
            coeffs = witness.get('coeffs')
            a = witness.get('a')
            k = witness.get('k')
        else:
            coeffs, a, k = witness
            
        if not isinstance(k, int) or k == 0:
            return [False, False, False]
            
        h1 = isinstance(coeffs, list) and all(isinstance(c, int) and c % k == 0 for c in coeffs)
        h2 = isinstance(a, int) and a % k == 0
        
        if not (h1 and h2):
            return [False, False, False]
            
        C = sympy.gcd_list(coeffs)
        f_a = sum(c * (a ** i) for i, c in enumerate(coeffs))
        
        if C == 0:
            divides = (f_a == 0)
        else:
            if f_a % C != 0:
                divides = False
            else:
                q = f_a // C
                divides = (q % k == 0)
                
        neg_q = not divides
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is a polynomial over R",
    "H_2: a is an element of R",
    "not_Q: The content of f does not divide f(a) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2