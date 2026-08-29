import sympy
from sympy import Poly, ZZ, QQ, GF, isprime, resultant
from sympy.abc import x
import math

CONDITION_LABELS = [
    'H_1: R is a commutative ring with identity',
    'not Q: I is a maximal ideal of the polynomial ring over R iff R is a field is FALSE'
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I_gens = witness.get('I')
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I_gens = witness
        else:
            R = witness
            I_gens = [x]
            
        if not isinstance(I_gens, (list, tuple)):
            I_gens = [I_gens]
    except Exception:
        return [False, False]

    try:
        h1 = hasattr(R, 'is_Field') or hasattr(R, 'is_ring') or R in [ZZ, QQ]
        if not h1:
            h1 = 'Domain' in str(type(R)) or 'Ring' in str(type(R)) or 'Field' in str(type(R))
        h1_ok = bool(h1)
    except Exception:
        h1_ok = False

    try:
        if not I_gens:
            I_is_maximal = False
        elif getattr(R, 'is_Field', False):
            g = Poly(I_gens[0], x, domain=R)
            for f in I_gens[1:]:
                g = g.gcd(Poly(f, x, domain=R))
            
            if g.degree() <= 0:
                I_is_maximal = False
            else:
                I_is_maximal = g.is_irreducible
        elif R == ZZ:
            integers = []
            for f in I_gens:
                expr = f.as_expr() if hasattr(f, 'as_expr') else sympy.sympify(f)
                if expr.is_Integer:
                    integers.append(abs(int(expr)))
            
            for i in range(len(I_gens)):
                for j in range(i+1, len(I_gens)):
                    diff = sympy.sympify(I_gens[i]) - sympy.sympify(I_gens[j])
                    if diff.is_Integer:
                        integers.append(abs(int(diff)))
                        
            if len(I_gens) >= 2:
                for i in range(len(I_gens)):
                    for j in range(i+1, len(I_gens)):
                        try:
                            r = resultant(I_gens[i], I_gens[j], x)
                            if r != 0:
                                integers.append(abs(int(r)))
                        except Exception:
                            pass
            
            if not integers:
                I_is_maximal = False
            else:
                c = integers[0]
                for val in integers[1:]:
                    c = math.gcd(c, val)
                
                if c == 1 or not isprime(c):
                    I_is_maximal = False
                else:
                    p = c
                    Fp = GF(p)
                    g = Poly(0, x, domain=Fp)
                    contains_unit = False
                    for f in I_gens:
                        try:
                            pf = Poly(f, x, domain=Fp)
                        except Exception:
                            continue
                        if pf.is_zero:
                            continue
                        if pf.degree() == 0:
                            contains_unit = True
                            break
                        if g.is_zero:
                            g = pf
                        else:
                            g = g.gcd(pf)
                    
                    if contains_unit or g.degree() <= 0:
                        I_is_maximal = False
                    else:
                        I_is_maximal = g.is_irreducible
        else:
            I_is_maximal = None

        if I_is_maximal is not None:
            R_is_field = bool(getattr(R, 'is_Field', False))
            neg_q_ok = not (I_is_maximal == R_is_field)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]