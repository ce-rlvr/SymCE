import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a commutative ring and M is a flat R-module, then S^{-1}M is a flat S^{-1}R-module."
    
    The dropped hypothesis is that S must be a multiplicatively closed subset.
    If S is not multiplicatively closed, the localized structures are not well-defined,
    and thus S^{-1}M is not a flat module over S^{-1}R.
    """
    try:
        # Parse witness
        if isinstance(witness, tuple) and len(witness) == 3:
            R, M, S = witness
        else:
            # Default to Z if only S is provided
            R = sympy.ZZ
            M = sympy.ZZ
            S = witness
            
        # H_1: R is a commutative ring
        h1 = False
        try:
            if R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
                h1 = True
            elif hasattr(R, 'is_commutative') and R.is_commutative:
                h1 = True
            elif isinstance(R, str) and R in ['ZZ', 'QQ', 'RR', 'CC', 'Z', 'Q', 'R', 'C']:
                h1 = True
            elif hasattr(R, 'is_ring') and R.is_ring and R.is_commutative:
                h1 = True
        except Exception:
            pass
            
        # H_2: M is a flat R-module
        h2 = False
        try:
            if M == R:
                h2 = True
            elif str(M) == str(R):
                h2 = True
            elif M in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
                h2 = True
        except Exception:
            pass
            
        # neg_Q: S^{-1}M is not a flat S^{-1}R-module
        # This occurs when S is not multiplicatively closed.
        neg_q = False
        try:
            if isinstance(S, (set, list, tuple)):
                S_elements = list(S)
                container = S
            else:
                S_elements = []
                if hasattr(S, '__iter__'):
                    for idx, item in enumerate(S):
                        if idx > 100:  # Limit to prevent infinite loops
                            break
                        S_elements.append(item)
                elif hasattr(S, 'args') and S.args:
                    S_elements = list(S.args)
                else:
                    S_elements = [S]
                
                if hasattr(S, '__contains__'):
                    container = S
                else:
                    container = S_elements
                    
            if not S_elements:
                # Empty set is not multiplicatively closed (localization undefined)
                neg_q = True
            else:
                is_closed = True
                for a in S_elements:
                    for b in S_elements:
                        if (a * b) not in container:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                neg_q = not is_closed
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is a flat R-module",
    "¬Q: S^{-1}M is not a flat S^{-1}R-module (e.g., S is not multiplicatively closed)"
]

N_HYP = 2
NEG_Q_INDEX = 2