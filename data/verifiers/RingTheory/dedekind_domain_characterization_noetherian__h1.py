import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer
from sympy.abc import x, y, z

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    # H_1: R is integrally closed in its field of fractions
    try:
        h1 = False
        if isinstance(witness, dict) and 'is_integrally_closed' in witness:
            h1 = bool(witness['is_integrally_closed'])
        elif hasattr(witness, 'is_integrally_closed'):
            val = witness.is_integrally_closed
            h1 = bool(val() if callable(val) else val)
        elif isinstance(witness, str):
            s = witness.lower()
            if "algebraic integer" in s and ("all" in s or "infinite" in s or "closure" in s or "bar" in s):
                h1 = True
            elif "valuation ring" in s and "rank 1" in s:
                h1 = True
            elif "puiseux" in s:
                h1 = True
            elif "non-discrete valuation" in s or "nondiscrete valuation" in s:
                h1 = True
        else:
            try:
                from sympy.polys.domains import Domain
                if isinstance(witness, Domain):
                    if witness == sympy.polys.domains.ZZ or witness == sympy.polys.domains.QQ:
                        h1 = True
                    elif hasattr(witness, 'is_Poly') and witness.is_Poly:
                        h1 = True
            except Exception:
                pass
    except Exception:
        h1 = False

    # H_2: Every non-zero prime ideal of R is a maximal ideal
    try:
        h2 = False
        if isinstance(witness, dict) and 'every_nonzero_prime_is_maximal' in witness:
            h2 = bool(witness['every_nonzero_prime_is_maximal'])
        elif isinstance(witness, dict) and 'krull_dimension' in witness:
            h2 = (witness['krull_dimension'] <= 1)
        elif hasattr(witness, 'every_nonzero_prime_is_maximal'):
            val = witness.every_nonzero_prime_is_maximal
            h2 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'krull_dimension'):
            val = witness.krull_dimension
            val = val() if callable(val) else val
            h2 = (val <= 1)
        elif isinstance(witness, str):
            s = witness.lower()
            if "algebraic integer" in s and ("all" in s or "infinite" in s or "closure" in s or "bar" in s):
                h2 = True
            elif "valuation ring" in s and "rank 1" in s:
                h2 = True
            elif "puiseux" in s:
                h2 = True
            elif "non-discrete valuation" in s or "nondiscrete valuation" in s:
                h2 = True
        else:
            try:
                from sympy.polys.domains import Domain
                if isinstance(witness, Domain):
                    if witness == sympy.polys.domains.ZZ or witness == sympy.polys.domains.QQ:
                        h2 = True
                    elif hasattr(witness, 'is_Poly') and witness.is_Poly:
                        if witness.dom == sympy.polys.domains.QQ and len(witness.gens) == 1:
                            h2 = True
                        else:
                            h2 = False
            except Exception:
                pass
    except Exception:
        h2 = False

    # neg_Q: R is NOT a Dedekind domain
    try:
        neg_q = False
        if isinstance(witness, dict) and 'is_dedekind' in witness:
            neg_q = not bool(witness['is_dedekind'])
        elif isinstance(witness, dict) and 'is_dedekind_domain' in witness:
            neg_q = not bool(witness['is_dedekind_domain'])
        elif isinstance(witness, dict) and 'is_noetherian' in witness:
            neg_q = not bool(witness['is_noetherian'])
        elif hasattr(witness, 'is_dedekind'):
            val = witness.is_dedekind
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_dedekind_domain'):
            val = witness.is_dedekind_domain
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_noetherian'):
            val = witness.is_noetherian
            neg_q = not bool(val() if callable(val) else val)
        elif isinstance(witness, str):
            s = witness.lower()
            if "algebraic integer" in s and ("all" in s or "infinite" in s or "closure" in s or "bar" in s):
                neg_q = True
            elif "valuation ring" in s and "rank 1" in s:
                neg_q = True
            elif "puiseux" in s:
                neg_q = True
            elif "non-discrete valuation" in s or "nondiscrete valuation" in s:
                neg_q = True
        else:
            try:
                from sympy.polys.domains import Domain
                if isinstance(witness, Domain):
                    if witness == sympy.polys.domains.ZZ or witness == sympy.polys.domains.QQ:
                        neg_q = False
                    elif hasattr(witness, 'is_Poly') and witness.is_Poly:
                        if witness.dom == sympy.polys.domains.QQ and len(witness.gens) == 1:
                            neg_q = False
                        else:
                            neg_q = True
            except Exception:
                pass
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is integrally closed in its field of fractions",
    "H_2: Every non-zero prime ideal of R is a maximal ideal",
    "¬Q: R is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2