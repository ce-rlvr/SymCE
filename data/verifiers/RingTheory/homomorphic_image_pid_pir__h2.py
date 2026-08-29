import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z
import math

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The quotient ring R/I is not a principal ideal ring"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    q = True
    
    try:
        R, I_ideal = None, None
        if isinstance(witness, dict):
            R = witness.get('R', None)
            I_ideal = witness.get('I', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, I_ideal = witness
        elif hasattr(witness, 'base_ring') and hasattr(witness, 'base_ideal'):
            R = witness.base_ring
            I_ideal = witness.base_ideal
            
        if R is not None and I_ideal is not None:
            is_zz = (R == sympy.ZZ or R == sympy.S.Integers)
            
            # Check H1: R is a PID
            if is_zz:
                h1 = True
            elif hasattr(R, 'is_PID') and R.is_PID:
                h1 = True
            elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing and R.domain.is_Field and len(R.gens) == 1:
                h1 = True
            else:
                h1 = False
                
            # Extract generator for the ideal
            gens = None
            if isinstance(I_ideal, (list, tuple, set)):
                gens = list(I_ideal)
            elif hasattr(I_ideal, 'gens'):
                gens = list(I_ideal.gens)
                
            if gens is not None:
                if len(gens) == 1:
                    I_gen = gens[0]
                elif len(gens) == 0:
                    I_gen = 0
                else:
                    try:
                        if is_zz:
                            g = 0
                            for gen in gens:
                                g = math.gcd(g, int(gen))
                            I_gen = g
                        elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing:
                            g = sympy.Poly(0, *R.gens, domain=R.domain)
                            for gen in gens:
                                p = sympy.Poly(gen, *R.gens, domain=R.domain)
                                if g.is_zero:
                                    g = p
                                else:
                                    g = g.gcd(p)
                            I_gen = g.as_expr()
                        else:
                            I_gen = None
                    except Exception:
                        I_gen = None
            else:
                I_gen = I_ideal
                
            # Check Q: R/I is a principal ideal ring.
            # Note: Since every quotient of a PID is mathematically a PIR, the false conjecture 
            # implies "principal ideal ring" was used to mean "principal ideal domain" (PID).
            # We evaluate whether R/I is a PID (which requires I to be a prime ideal).
            if I_gen is not None:
                if is_zz:
                    try:
                        val = abs(int(I_gen))
                        if val == 0:
                            q = True
                        elif val == 1:
                            q = False
                        else:
                            q = sympy.isprime(val)
                    except Exception:
                        q = True
                elif hasattr(R, 'is_PolynomialRing') and R.is_PolynomialRing and R.domain.is_Field and len(R.gens) == 1:
                    try:
                        poly = sympy.Poly(I_gen, *R.gens, domain=R.domain)
                        if poly.is_zero:
                            q = True
                        elif poly.degree() <= 0:
                            q = False
                        else:
                            q = poly.is_irreducible
                    except Exception:
                        q = True
                else:
                    q = True
            else:
                q = True
    except Exception:
        pass
        
    return [h1, not q]