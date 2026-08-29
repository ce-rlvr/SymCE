import sympy
from sympy import Poly, Symbol, RootOf, AlgebraicNumber, sympify
from sympy.polys.polytools import factor_list
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
    "H_1: E is the set of all elements in K that are separable over F",
    "¬Q: E is NOT a normal extension of F"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness (expected to be a polynomial or a tuple containing a polynomial 
    that generates the extension K over F=QQ), checks if it satisfies the hypotheses 
    and falsifies the conclusion.
    """
    def to_poly(obj):
        if isinstance(obj, str):
            try:
                obj = sympify(obj)
            except Exception:
                pass
        try:
            if hasattr(obj, 'minpoly'):
                p = Poly(obj.minpoly, domain='QQ')
                if len(p.gens) == 1:
                    return p
        except Exception:
            pass
        try:
            p = Poly(obj, domain='QQ')
            if len(p.gens) == 1:
                return p
        except Exception:
            pass
        return None

    f_poly = None
    if isinstance(witness, tuple):
        for item in witness:
            p = to_poly(item)
            if p is not None and p.degree() >= 2:
                f_poly = p
                break
        if f_poly is None:
            for item in witness:
                p = to_poly(item)
                if p is not None:
                    f_poly = p
                    break
    else:
        f_poly = to_poly(witness)

    try:
        if f_poly is None:
            h1_ok = False
        else:
            # H1: E is the maximal separable subextension of K over F.
            # Assuming F=QQ, K=QQ[x]/(f_poly), E=K (since char 0).
            # We just need K to be a valid field extension, so f_poly must be irreducible.
            h1_ok = f_poly.is_irreducible
    except Exception:
        h1_ok = False

    try:
        if not h1_ok or f_poly is None:
            neg_q = False
        else:
            deg = f_poly.degree()
            if deg < 2:
                neg_q = False
            else:
                # Check if it has both real and non-real roots.
                # If an irreducible polynomial over QQ has a real root, its generated field 
                # can be embedded in RR. If it also has non-real roots, it cannot contain them,
                # hence it cannot be a normal extension.
                roots = f_poly.all_roots()
                real_roots = [r for r in roots if r.is_real]
                if 0 < len(real_roots) < deg:
                    neg_q = True
                else:
                    # Fallback: explicitly check if it splits completely over its own extension
                    r = RootOf(f_poly, 0)
                    ext = AlgebraicNumber(r)
                    factors = factor_list(f_poly, extension=ext)[1]
                    is_normal = all(fac[0].degree() == 1 for fac in factors)
                    neg_q = not is_normal
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(neg_q)]