import sympy

x = sympy.Symbol('x')

def parse_element(u):
    if isinstance(u, dict):
        return {int(k): int(v) for k, v in u.items()}
    if isinstance(u, sympy.Expr):
        u = sympy.expand(u)
        d = u.as_coefficients_dict()
        res = {}
        for term, coeff in d.items():
            if term == 1:
                res[0] = int(coeff)
            elif isinstance(term, sympy.Symbol):
                res[1] = int(coeff)
            elif isinstance(term, sympy.Pow) and isinstance(term.base, sympy.Symbol):
                res[int(term.exp)] = int(coeff)
            else:
                raise ValueError(f"Unsupported term: {term}")
        return res
    raise ValueError("Unsupported element type")

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            n, M_type, u1, u2 = witness
        elif len(witness) == 3:
            n, u1, u2 = witness
            M_type = "N"
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = M_type in ["N", "Z"]
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = isinstance(n, int) and n >= 2
        u1_dict = parse_element(u1)
        u2_dict = parse_element(u2)
        if M_type == "N":
            if any(k < 0 for k in u1_dict.keys()) or any(k < 0 for k in u2_dict.keys()):
                h2_ok = False
    except Exception:
        h2_ok = False
        
    try:
        def clean(u):
            return {k: v % n for k, v in u.items() if v % n != 0}
            
        def multiply(a, b):
            res = {}
            for k1, v1 in a.items():
                for k2, v2 in b.items():
                    k = k1 + k2
                    res[k] = (res.get(k, 0) + v1 * v2) % n
            return clean(res)
            
        u1_clean = clean(u1_dict)
        u2_clean = clean(u2_dict)
        
        prod1 = multiply(u1_clean, u2_clean)
        prod2 = multiply(u2_clean, u1_clean)
        
        is_unit = (prod1 == {0: 1}) and (prod2 == {0: 1})
        
        not_form_um = len(u1_clean) > 1
        
        neg_q_ok = is_unit and not_form_um
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: M is a strictly totally ordered monoid",
    "H_2: The ring is the monoid ring of M over R",
    "¬Q: The group of units does not consist exactly of elements of the form u*m"
]

N_HYP = 2
NEG_Q_INDEX = 2