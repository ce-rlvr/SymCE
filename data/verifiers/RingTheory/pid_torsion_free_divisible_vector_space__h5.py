import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.abc import x

# Top-level setup
# ZZ, QQ, RR, CC, S, and x are imported and available for the witness.

def to_domain(obj):
    """Convert SymPy singleton sets to their corresponding domains if needed."""
    if obj is S.Integers: return ZZ
    if obj is S.Rationals: return QQ
    if obj is S.Reals: return RR
    if obj is S.Complexes: return CC
    return obj

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness into R, K, M
        if isinstance(witness, dict):
            R = witness.get('R')
            K = witness.get('K')
            M = witness.get('M')
            R = to_domain(R)
            M = to_domain(M)
            if K is None and R is not None:
                try:
                    K = R.get_field()
                except Exception:
                    pass
            else:
                K = to_domain(K)
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, K, M = witness
                R = to_domain(R)
                K = to_domain(K)
                M = to_domain(M)
            elif len(witness) == 2:
                R, M = witness
                R = to_domain(R)
                M = to_domain(M)
                try:
                    K = R.get_field()
                except Exception:
                    K = None
            else:
                return [False] * 5
        else:
            # If only a single object is provided, assume it is M over R=ZZ
            M = to_domain(witness)
            R = ZZ
            K = QQ

        # H1: R is a principal ideal domain
        try:
            h1 = getattr(R, 'is_PID', False)
        except Exception:
            h1 = False

        # H2: K is the field of fractions of R
        try:
            h2 = (K == R.get_field())
        except Exception:
            h2 = False

        # H3: M is an R-module
        # In the context of SymPy domains, M is an R-module if R can be embedded in M.
        try:
            h3 = (R.unify(M) == M)
        except Exception:
            h3 = False

        # H4: M is torsion-free
        # If M is an integral domain and R is a subring, M has no zero divisors,
        # hence it is torsion-free over R.
        try:
            h4 = h3 and hasattr(M, 'get_field')
        except Exception:
            h4 = False

        # ¬Q: M does not admit a unique K-vector space structure extending its R-module structure
        # For a torsion-free module M over a PID R, it admits a K-vector space structure
        # if and only if it is divisible by R (which means K is a subring of M).
        # If it is divisible, the structure is unique.
        # Thus, it fails to admit a unique structure iff it is NOT divisible by R.
        try:
            is_divisible = (K.unify(M) == M)
            neg_q = not is_divisible
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: K is the field of fractions of R",
    "H_3: M is an R-module",
    "H_4: M is torsion-free",
    "¬Q: M does not admit a unique K-vector space structure extending its R-module structure"
]

N_HYP = 4
NEG_Q_INDEX = 4