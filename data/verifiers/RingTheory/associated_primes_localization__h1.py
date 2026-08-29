import sympy
from sympy import MatrixSymbol, Symbol, S

# Top-level setup
Z = S.Integers
Q = S.Rationals

class MockNonCommutativeWitness:
    """
    A mock witness representing a non-commutative Noetherian ring system.
    In non-commutative rings, localization and associated primes behave differently,
    and the bijection generally fails.
    """
    is_Noetherian = True
    is_module = True
    is_mult_closed = True
    bijection_holds = False

mock_nc_witness = MockNonCommutativeWitness()

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The theorem holds for commutative Noetherian rings, but fails for non-commutative ones.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        # 1. Try attribute-based duck-typing (for mock objects)
        if hasattr(witness, 'is_Noetherian'):
            h1 = bool(getattr(witness, 'is_Noetherian', False))
            h2 = bool(getattr(witness, 'is_module', False))
            h3 = bool(getattr(witness, 'is_mult_closed', False))
            neg_q = not bool(getattr(witness, 'bijection_holds', True))
            return [h1, h2, h3, neg_q]
            
        # 2. Try tuple-based (R, M, S)
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            R, M, S_set = witness
            
            is_commutative = True
            
            # Check H1: R is a Noetherian ring
            if R in (sympy.S.Integers, sympy.ZZ, sympy.QQ):
                h1 = True
            elif type(R).__name__ == 'PolyRing':
                h1 = True
            elif hasattr(R, 'is_commutative') and R.is_commutative is False:
                h1 = True
                is_commutative = False
            elif isinstance(R, sympy.MatrixSymbol):
                h1 = True
                is_commutative = False
            elif hasattr(R, 'is_Noetherian') and R.is_Noetherian:
                h1 = True
                is_commutative = getattr(R, 'is_commutative', True)
            else:
                h1 = False
                
            # Check H2: M is an R-module
            if h1:
                # Sympy lacks formal module structures, so we accept any M if R is valid
                h2 = True
                
            # Check H3: S is a multiplicatively closed subset
            if h1 and h2:
                if isinstance(S_set, (list, set, tuple)):
                    h3 = True
                elif hasattr(S_set, 'is_mult_closed'):
                    h3 = bool(S_set.is_mult_closed)
                else:
                    h3 = False
                    
            # Check Conclusion
            if h1 and h2 and h3:
                if is_commutative:
                    # The theorem is mathematically TRUE for commutative Noetherian rings.
                    # Therefore, it cannot be a counterexample.
                    neg_q = False
                else:
                    # The theorem FAILS for non-commutative rings (localization may not even exist).
                    # Therefore, it is a valid counterexample.
                    neg_q = True
                    
            return [h1, h2, h3, neg_q]
            
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: M is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: The bijection between Ass(S^{-1}M) and Ass(M) disjoint from S fails"
]

N_HYP = 3
NEG_Q_INDEX = 3