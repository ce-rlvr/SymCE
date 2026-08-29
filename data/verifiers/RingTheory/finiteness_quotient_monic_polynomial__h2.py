import sympy
from sympy import Poly, Matrix
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, dict):
            I_gens = witness.get('I_gens', [])
            n = witness.get('n', 0)
            var = witness.get('var', x)
            is_ideal = witness.get('is_ideal', False)
        elif isinstance(witness, (tuple, list)):
            I_gens = witness[0] if len(witness) > 0 else []
            n = witness[1] if len(witness) > 1 else 0
            var = witness[2] if len(witness) > 2 else x
            is_ideal = witness[3] if len(witness) > 3 else False
        else:
            I_gens = getattr(witness, 'I_gens', [])
            n = getattr(witness, 'n', 0)
            var = getattr(witness, 'var', x)
            is_ideal = getattr(witness, 'is_ideal', False)
    except Exception:
        return [False, False, False]
        
    h1 = True
    
    h2 = False
    try:
        n = int(n)
        if n >= 1:
            for p in I_gens:
                p_poly = Poly(p, var)
                if p_poly.degree() == n and p_poly.LC() == 1:
                    h2 = True
                    break
    except Exception:
        pass
                
    neg_q = False
    try:
        if is_ideal:
            neg_q = False
        else:
            basis = list(I_gens) + [var**i for i in range(n)]
            if not I_gens:
                max_deg = max(0, n - 1)
            else:
                max_deg = max([Poly(p, var).degree() for p in I_gens] + [n - 1, 0])
            
            target = var**(max_deg + 1)
            
            polys = [Poly(p, var) for p in basis]
            target_poly = Poly(target, var)
            
            mat = []
            for p in polys:
                coeffs = p.all_coeffs()
                coeffs = [0]*(max_deg + 2 - len(coeffs)) + coeffs
                mat.append(coeffs)
                
            target_coeffs = target_poly.all_coeffs()
            target_coeffs = [0]*(max_deg + 2 - len(target_coeffs)) + target_coeffs
            
            M = Matrix(mat)
            M_aug = Matrix(mat + [target_coeffs])
            
            if M.rank() < M_aug.rank():
                neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I contains a monic polynomial of degree n >= 1",
    "¬Q: The quotient ring is NOT generated as an R-module by the images of 1, x, ..., x^{n-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2