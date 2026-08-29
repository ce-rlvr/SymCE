import sympy
from sympy import fraction, cancel, Poly, lcm, gcd, groebner, reduced
from sympy.abc import x, y, z, t, u, v, w
from functools import reduce

def is_rational_function(g, symbols):
    try:
        n, d = fraction(cancel(g))
        if not symbols:
            # If there are no symbols, it must be a rational number
            if not (n.is_rational and d.is_rational):
                return False
            return True
        # If symbols exist, ensure it's a rational function over QQ
        Poly(n, *symbols, domain='QQ')
        Poly(d, *symbols, domain='QQ')
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a list of generators for the submodule M
        if not isinstance(witness, (list, tuple)):
            return [False, False, False]
        gens = list(witness)
        if len(gens) == 0:
            return [False, False, False]
        
        # Infer the polynomial ring R = QQ[symbols] from the generators
        symbols = list(set().union(*[g.free_symbols for g in gens]))
        symbols = sorted(symbols, key=lambda s: s.name)
        
        # H_1: K is the field of fractions of R
        # This is satisfied by our setup where R = QQ[symbols] and K = QQ(symbols)
        h1_ok = True
        
        # H_2: M is a finitely generated R-submodule of K
        # True if all generators are valid elements of K
        h2_ok = all(is_rational_function(g, symbols) for g in gens)
        
        # ¬Q: M is NOT a cyclic R-module
        # M is cyclic iff its associated fractional ideal is principal.
        if not h2_ok:
            neg_q = False
        else:
            if not symbols:
                # Over QQ (a field), any finitely generated submodule is a vector space.
                # Since it's a submodule of QQ, its dimension is at most 1, so it's always cyclic.
                neg_q = False
            else:
                # Find the common denominator D of all generators
                denoms = [fraction(cancel(g))[1] for g in gens]
                D = reduce(lcm, denoms)
                
                # Compute the generators of the corresponding ideal in R
                f_list = [cancel(g * D) for g in gens]
                f_polys = []
                for f in f_list:
                    n, d = fraction(f)
                    f_polys.append(n)
                
                # The ideal is principal iff the GCD of the generators is in the ideal
                h = reduce(gcd, f_polys)
                
                # Check ideal membership using Groebner bases over QQ
                GB = groebner(f_polys, *symbols, domain='QQ')
                rem = reduced(h, GB, *symbols, domain='QQ')[1]
                
                is_cyclic = (rem == 0)
                neg_q = not is_cyclic
                
    except Exception:
        h1_ok = False
        h2_ok = False
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: M is a finitely generated R-submodule of K",
    "¬Q: M is not a cyclic R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2