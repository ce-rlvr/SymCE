import sympy

class AbstractRing:
    def __init__(self, name, is_ufd):
        self.name = name
        self.is_ufd = is_ufd
        self.one = 1
        self.zero = 0
        
    def __repr__(self):
        return self.name

# Predefined rings for potential witnesses
Z_sqrt_minus_5 = AbstractRing("Z[sqrt(-5)]", is_ufd=False)
Z = AbstractRing("Z", is_ufd=True)

def conditions(witness) -> list[bool]:
    # Extract R and S from the witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = witness.R
            S = witness.S
    except Exception:
        return [False, False, False]

    # H_1: S is a multiplicatively closed subset of R
    try:
        if hasattr(S, 'is_mult_closed'):
            h1 = bool(S.is_mult_closed())
        else:
            h1 = True
            for a in S:
                for b in S:
                    if a * b not in S:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: 0 is not an element of S
    try:
        if hasattr(S, 'contains_zero'):
            h2 = not bool(S.contains_zero())
        else:
            h2 = True
            if 0 in S:
                h2 = False
            elif hasattr(R, 'zero') and R.zero in S:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: The localization S^{-1}R is not a unique factorization domain
    try:
        if hasattr(witness, 'localization_is_ufd'):
            is_ufd = bool(witness.localization_is_ufd())
        else:
            # Determine if R is a UFD
            if hasattr(R, 'is_UFD'):
                r_ufd = bool(R.is_UFD)
            else:
                r_ufd = bool(R.is_ufd)
            
            # Check if S is the trivial multiplicative set {1}
            try:
                is_trivial_S = False
                if hasattr(S, '__len__') and len(S) == 1:
                    elem = next(iter(S))
                    if elem == 1 or (hasattr(R, 'one') and elem == R.one):
                        is_trivial_S = True
            except Exception:
                is_trivial_S = False
                
            # Check if S contains 0 (localization becomes the zero ring, which is not a domain)
            try:
                has_zero = 0 in S or (hasattr(R, 'zero') and R.zero in S)
            except Exception:
                has_zero = False

            if is_trivial_S:
                is_ufd = r_ufd
            elif has_zero:
                is_ufd = False
            else:
                # For non-trivial S, we default to True to avoid false positive counterexamples
                is_ufd = True
                
        neg_q = not is_ufd
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: S is a multiplicatively closed subset of R",
    "H_2: 0 is not an element of S",
    "¬Q: The localization S^{-1}R is not a unique factorization domain"
]

N_HYP = 2
NEG_Q_INDEX = 2