import sympy
from sympy import Poly, Symbol
from sympy.polys.domains import Domain
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over F",
    "H_2: c is a non-zero element of F",
    "H_3: K is the splitting field of f(x) over F",
    "¬Q: K is NOT the splitting field of the polynomial c * f(x) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict) and 'neg_Q' in witness:
        return [
            bool(witness.get('h1', False)),
            bool(witness.get('h2', False)),
            bool(witness.get('h3', False)),
            bool(witness.get('neg_Q', False))
        ]
    
    if hasattr(witness, 'neg_Q'):
        try:
            return [
                bool(getattr(witness, 'h1', False)),
                bool(getattr(witness, 'h2', False)),
                bool(getattr(witness, 'h3', False)),
                bool(getattr(witness, 'neg_Q', False))
            ]
        except Exception:
            pass

    h1, h2, h3, neg_q = False, False, False, False

    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                F, f, c, K = witness
            elif len(witness) == 2:
                f, c = witness
                F = getattr(f, 'domain', None)
                K = "implicit_splitting_field"
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            F = witness.get('F')
            f = witness.get('f')
            c = witness.get('c')
            K = witness.get('K')
        else:
            F = getattr(witness, 'F', None)
            f = getattr(witness, 'f', None)
            c = getattr(witness, 'c', None)
            K = getattr(witness, 'K', None)
            
        if F is None or f is None or c is None or K is None:
            return [False, False, False, False]

        try:
            if isinstance(f, Poly):
                h1 = (f.domain == F) or (F == getattr(f, 'domain', None))
            else:
                poly_f = Poly(f)
                h1 = True
        except Exception:
            h1 = False

        try:
            c_nonzero = bool(c != 0)
            if hasattr(F, 'contains'):
                h2 = c_nonzero and F.contains(c)
            elif hasattr(F, '__contains__'):
                h2 = c_nonzero and (c in F)
            else:
                h2 = c_nonzero
        except Exception:
            h2 = False

        try:
            if K == "implicit_splitting_field":
                h3 = True
            elif hasattr(K, 'is_splitting_field'):
                h3 = bool(K.is_splitting_field(f, F))
            else:
                poly_f = Poly(f)
                if poly_f.is_zero:
                    h3 = (K == F)
                else:
                    factors = poly_f.set_domain(K).factor_list()
                    h3 = all(fac.degree() == 1 for fac, mult in factors[1])
        except Exception:
            h3 = False

        try:
            if K == "implicit_splitting_field":
                neg_q = False
            else:
                cf = c * f
                if hasattr(K, 'is_splitting_field'):
                    neg_q = not K.is_splitting_field(cf, F)
                else:
                    poly_cf = Poly(cf)
                    if poly_cf.is_zero:
                        neg_q = (K != F)
                    else:
                        factors_cf = poly_cf.set_domain(K).factor_list()
                        splits_cf = all(fac.degree() == 1 for fac, mult in factors_cf[1])
                        neg_q = not splits_cf
        except Exception:
            neg_q = False

    except Exception:
        pass

    return [h1, h2, h3, neg_q]