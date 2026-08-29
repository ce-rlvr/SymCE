import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    h1_ok = False
    try:
        if isinstance(witness, Poly) and len(witness.gens) == 1:
            if hasattr(witness.domain, 'characteristic'):
                p = witness.domain.characteristic
                if p > 0 and witness.domain.is_Field:
                    h1_ok = True
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if h1_ok:
            p = witness.domain.characteristic
            degrees = [monom[0] for monom in witness.monoms()]
            
            if not degrees or max(degrees) == 0:
                conclusion_holds = False
            else:
                k = 0
                while True:
                    if all(d % p == 0 for d in degrees):
                        degrees = [d // p for d in degrees]
                        k += 1
                    else:
                        break
                
                if k == 0:
                    conclusion_holds = False
                else:
                    g_dict = { (d,): c for d, c in zip(degrees, witness.coeffs()) }
                    g = Poly(g_dict, witness.gens[0], domain=witness.domain)
                    
                    if not g.is_irreducible:
                        conclusion_holds = False
                    else:
                        g_diff = g.diff(witness.gens[0])
                        if g_diff.is_zero:
                            conclusion_holds = False
                        else:
                            conclusion_holds = True
            neg_q_ok = not conclusion_holds
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: f is a polynomial over a field F of characteristic p > 0", "¬Q: f cannot be written as g(x^(p^k)) for k >= 1 and separable irreducible g"]
N_HYP = 1
NEG_Q_INDEX = 1