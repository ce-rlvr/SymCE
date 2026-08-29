import sympy
from sympy import symbols

# Top-level setup: Named objects and classes for the witness expression
# The conjecture fails for non-commutative integral domains.
# We provide a Free Algebra over a field (which is a non-commutative domain)
# and a specific module M = R/Rx \oplus R/Ry where the torsion subset is not a submodule.

class FreeAlgebraElement:
    """An element of the free algebra Z<x, y>."""
    def __init__(self, terms):
        self.terms = {}
        for k, v in terms.items():
            if v != 0:
                if isinstance(k, str):
                    if k == '':
                        k = ()
                    else:
                        k = tuple(k)
                elif isinstance(k, tuple):
                    pass
                else:
                    k = tuple(k)
                self.terms[k] = v

    def __add__(self, other):
        if not isinstance(other, FreeAlgebraElement):
            return NotImplemented
        res = self.terms.copy()
        for k, v in other.terms.items():
            res[k] = res.get(k, 0) + v
        return FreeAlgebraElement(res)

    def __mul__(self, other):
        if not isinstance(other, FreeAlgebraElement):
            return NotImplemented
        res = {}
        for k1, v1 in self.terms.items():
            for k2, v2 in other.terms.items():
                k = k1 + k2
                res[k] = res.get(k, 0) + v1 * v2
        return FreeAlgebraElement(res)

    def is_zero(self):
        return len(self.terms) == 0

    def __eq__(self, other):
        if not isinstance(other, FreeAlgebraElement):
            return False
        return self.terms == other.terms

    def __repr__(self):
        return f"FreeAlgebraElement({self.terms})"

class FreeAlgebraModuleElement:
    """An element of the module M = R/Rx \oplus R/Ry."""
    def __init__(self, p1, p2):
        if isinstance(p1, FreeAlgebraElement):
            p1_terms = p1.terms
        else:
            p1_terms = FreeAlgebraElement(p1).terms
            
        if isinstance(p2, FreeAlgebraElement):
            p2_terms = p2.terms
        else:
            p2_terms = FreeAlgebraElement(p2).terms
            
        # Reduce modulo the left ideal Rx (remove terms starting with 'x')
        self.p1 = FreeAlgebraElement({k: v for k, v in p1_terms.items() if not (len(k) > 0 and k[0] == 'x')})
        # Reduce modulo the left ideal Ry (remove terms starting with 'y')
        self.p2 = FreeAlgebraElement({k: v for k, v in p2_terms.items() if not (len(k) > 0 and k[0] == 'y')})

    def __add__(self, other):
        if not isinstance(other, FreeAlgebraModuleElement):
            return NotImplemented
        res = FreeAlgebraModuleElement({}, {})
        res.p1 = self.p1 + other.p1
        res.p2 = self.p2 + other.p2
        return res

    def __rmul__(self, r):
        if not isinstance(r, FreeAlgebraElement):
            return NotImplemented
        return FreeAlgebraModuleElement(r * self.p1, r * self.p2)

    def is_zero(self):
        return self.p1.is_zero() and self.p2.is_zero()

    def __eq__(self, other):
        if not isinstance(other, FreeAlgebraModuleElement):
            return False
        return self.p1 == other.p1 and self.p2 == other.p2

    def __repr__(self):
        return f"FreeAlgebraModuleElement({self.p1}, {self.p2})"

# Standard generators for the witness to use
x_elem = FreeAlgebraElement({('x',): 1})
y_elem = FreeAlgebraElement({('y',): 1})
one_elem = FreeAlgebraElement({(): 1})
zero_elem = FreeAlgebraElement({})

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        # H_1: R is an integral domain
        h1 = bool(witness.get('R_is_domain', False))
        
        # H_2: M is an R-module
        h2 = bool(witness.get('M_is_module', False))
        
        m1 = witness.get('m1')
        m2 = witness.get('m2')
        r1 = witness.get('r1')
        r2 = witness.get('r2')
        
        if not isinstance(m1, FreeAlgebraModuleElement) or not isinstance(m2, FreeAlgebraModuleElement):
            return [h1, h2, False]
        if not isinstance(r1, FreeAlgebraElement) or not isinstance(r2, FreeAlgebraElement):
            return [h1, h2, False]
            
        # To prove T is not a submodule, the witness must provide m1, m2 in T
        # which means there exist non-zero r1, r2 in R such that r1*m1 = 0 and r2*m2 = 0.
        if r1.is_zero() or r2.is_zero():
            return [h1, h2, False]
            
        if not (r1 * m1).is_zero() or not (r2 * m2).is_zero():
            return [h1, h2, False]
            
        # And we must check that m1 + m2 is NOT in T.
        # In this specific module R/Rx \oplus R/Ry, an element (p1, p2) is in T 
        # if and only if p1 = 0 or p2 = 0. 
        # Thus, it is NOT in T if and only if BOTH components are non-zero.
        m3 = m1 + m2
        if not m3.p1.is_zero() and not m3.p2.is_zero():
            neg_q = True
        else:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is an R-module",
    "¬Q: T is not a submodule of M"
]

N_HYP = 2
NEG_Q_INDEX = 2