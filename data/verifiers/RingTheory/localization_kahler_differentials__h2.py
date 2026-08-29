import sympy
from sympy import eye, zeros, Symbol
from sympy.abc import x, y, z

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The dropped hypothesis from the true theorem is that R is a commutative ring (or commutative A-algebra).
    """
    h1, h2, neg_q = False, False, False
    try:
        # Unpack witness
        if isinstance(witness, dict):
            A = witness.get('A')
            R = witness.get('R')
            S = witness.get('S')
        elif hasattr(witness, 'A') and hasattr(witness, 'R') and hasattr(witness, 'S'):
            A = witness.A
            R = witness.R
            S = witness.S
        else:
            A, R, S = witness

        # H_1: A is a commutative ring
        h1 = getattr(A, 'is_commutative', True)
        if h1 is None:
            h1 = True

        # H_2: S is a multiplicatively closed subset of R
        if hasattr(S, '__iter__'):
            S_list = list(S)
            h2 = True
            for a in S_list:
                for b in S_list:
                    try:
                        prod = a * b
                    except Exception:
                        h2 = False
                        break
                    
                    found = False
                    for s in S_list:
                        if prod == s:
                            found = True
                            break
                        try:
                            diff = prod - s
                            if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
                                found = True
                                break
                            if diff == 0:
                                found = True
                                break
                        except Exception:
                            pass
                    if not found:
                        h2 = False
                        break
                if not h2:
                    break
        else:
            h2 = False
            S_list = []

        # ¬Q: The isomorphism of S^{-1}R-modules fails
        # The isomorphism holds if R is commutative, or trivially if S contains 0 or only the identity.
        is_trivial_S = True
        has_zero = False
        for s in S_list:
            # Check if s is zero
            if s == 0:
                has_zero = True
            elif hasattr(s, 'is_zero') and s.is_zero:
                has_zero = True
            elif hasattr(s, 'is_zero_matrix') and s.is_zero_matrix:
                has_zero = True
                
            # Check if s is identity
            is_id = False
            if s == 1:
                is_id = True
            elif hasattr(s, 'is_Identity') and s.is_Identity:
                is_id = True
            elif hasattr(s, 'shape') and len(s.shape) == 2 and s.shape[0] == s.shape[1]:
                try:
                    if s == eye(s.shape[0]):
                        is_id = True
                except Exception:
                    pass
            
            if not is_id:
                is_trivial_S = False

        r_comm = getattr(R, 'is_commutative', True)
        if r_comm is None:
            r_comm = True

        if has_zero or is_trivial_S or len(S_list) == 0:
            neg_q = False
        else:
            neg_q = not r_comm

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The isomorphism of S^{-1}R-modules fails"
]

N_HYP = 2
NEG_Q_INDEX = 2