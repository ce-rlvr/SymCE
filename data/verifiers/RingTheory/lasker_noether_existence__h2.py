import sympy
from sympy.abc import x, y, z, t
from sympy import QQ, ZZ

# Top-level setup
# No specific named bindings required for this domain beyond standard symbols and fields.

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        # Handle string-based known counterexamples
        if isinstance(witness, str):
            s = witness.lower()
            if "continuous" in s or "infinite" in s or "non-noetherian" in s or "k[x" in s:
                return [True, True, True]
            return [False, False, False]

        # Handle dictionary-based witness
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_commutative_ring_with_identity', False))
            h2 = bool(witness.get('is_proper_ideal', False))
            neg_q = not bool(witness.get('has_finite_primary_decomposition', True))
            return [h1, h2, neg_q]

        # Handle object-based or tuple-based witness
        R, I = None, None
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'I'):
            R = witness.R
            I = witness.I
            
        if R is not None and I is not None:
            # H1: R is a commutative ring with identity
            if type(R).__name__ in ('PolyRing', 'QuotientRing'):
                h1 = True
            else:
                if hasattr(R, 'is_commutative_ring_with_identity'):
                    val = R.is_commutative_ring_with_identity
                    h1 = bool(val() if callable(val) else val)
                elif hasattr(R, 'is_commutative') and hasattr(R, 'has_identity'):
                    comm = R.is_commutative
                    comm = comm() if callable(comm) else comm
                    ident = R.has_identity
                    ident = ident() if callable(ident) else ident
                    h1 = bool(comm and ident)

            # H2: I is a proper ideal of R
            if type(R).__name__ in ('PolyRing', 'QuotientRing') and 'Ideal' in type(I).__name__:
                try:
                    h2 = not I.contains(R.one)
                except Exception:
                    h2 = False
            else:
                if hasattr(I, 'is_proper_ideal'):
                    val = I.is_proper_ideal
                    h2 = bool(val() if callable(val) else val)
                elif hasattr(I, 'is_proper'):
                    val = I.is_proper
                    h2 = bool(val() if callable(val) else val)

            # neg_Q: I cannot be expressed as a finite intersection of primary ideals
            if type(R).__name__ in ('PolyRing', 'QuotientRing') and 'Ideal' in type(I).__name__:
                # Polynomial rings over fields in finitely many variables are Noetherian.
                # Thus, every proper ideal has a finite primary decomposition.
                neg_q = False
            else:
                if hasattr(I, 'has_finite_primary_decomposition'):
                    val = I.has_finite_primary_decomposition
                    neg_q = not bool(val() if callable(val) else val)
                elif hasattr(I, 'has_primary_decomposition'):
                    val = I.has_primary_decomposition
                    neg_q = not bool(val() if callable(val) else val)
                elif hasattr(witness, 'is_counterexample'):
                    val = witness.is_counterexample
                    neg_q = bool(val() if callable(val) else val)

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R",
    "¬Q: I cannot be expressed as a finite intersection of primary ideals of R"
]

N_HYP = 2
NEG_Q_INDEX = 2