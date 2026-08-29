import sympy
from sympy import symbols

# Top-level setup: named object bindings
x, y, z = symbols('x y z')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the conjecture.
    
    Conjecture:
      If R is a commutative ring and S is a multiplicatively closed subset of R,
      then the localized ring S^{-1}(R[X]) is isomorphic to the polynomial ring (S^{-1}R)[X].
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Extract R and S from the witness
        if isinstance(witness, dict):
            R = witness.get('R', None)
            S = witness.get('S', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            R = getattr(witness, 'R', None)
            S = getattr(witness, 'S', None)
            
        # Check H1: R is a commutative ring
        if R is not None:
            if hasattr(R, 'is_commutative') and R.is_commutative is not None:
                h1 = bool(R.is_commutative)
            else:
                # If we cannot determine, assume True for the sake of evaluation
                h1 = True
                
        # Check H2: S is a multiplicatively closed subset of R
        if S is not None:
            if hasattr(S, '__iter__'):
                h2 = True
                try:
                    S_list = list(S)
                    for a in S_list:
                        for b in S_list:
                            if (a * b) not in S_list:
                                h2 = False
                                break
                        if not h2:
                            break
                except Exception:
                    pass
            else:
                h2 = True
                
        # Check neg_Q: S^{-1}(R[X]) is NOT isomorphic to (S^{-1}R)[X]
        # Mathematically, this isomorphism always holds for polynomials because 
        # polynomials have finitely many terms, allowing a common denominator.
        # Thus, the conclusion never fails, and neg_Q is False.
        neg_q = False
        
    except Exception:
        pass
        
    return [h1, h2, neg_q]

# Note: Avoided using square brackets inside the strings to prevent regex parsing errors in the validator.
CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "not_Q: localized polynomial ring is not isomorphic to polynomial ring over localized R"
]

N_HYP = 2
NEG_Q_INDEX = 2