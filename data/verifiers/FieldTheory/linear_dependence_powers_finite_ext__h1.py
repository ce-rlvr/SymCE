import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n', 1)
            alpha = witness.get('alpha', 1)
        elif isinstance(witness, (tuple, list)):
            if len(witness) >= 2:
                n = witness[0]
                alpha = witness[1]
            else:
                n = 1
                alpha = witness[0]
        else:
            return [False, False, False]
            
        n = int(n)
        if n < 1:
            return [False, False, False]
            
        alpha = sp.sympify(alpha)
        
        x = sp.Symbol('x')
        if alpha.is_Rational:
            poly = sp.Poly(x - alpha, x, domain='QQ')
            deg_alpha = 1
        else:
            poly = sp.minpoly(alpha, x, polys=True)
            deg_alpha = poly.degree()
            
        h1 = (n % deg_alpha == 0)
        h2 = True
        
        vectors = set()
        curr = sp.Poly(1, x, domain='QQ')
        x_poly = sp.Poly(x, x, domain='QQ')
        
        for i in range(n + 1):
            _, rem = curr.div(poly)
            coeffs = rem.all_coeffs()
            coeffs = [0] * (deg_alpha - len(coeffs)) + coeffs
            vectors.add(tuple(coeffs))
            curr = curr * x_poly
            
        if len(vectors) == 0:
            is_dependent = False
        else:
            M = sp.Matrix(list(vectors))
            is_dependent = M.rank() < len(vectors)
            
        neg_q = not is_dependent
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: The degree of E over F is equal to n", "H_2: alpha is an element of E", "not Q: The set of elements is linearly independent over F"]

N_HYP = 2
NEG_Q_INDEX = 2