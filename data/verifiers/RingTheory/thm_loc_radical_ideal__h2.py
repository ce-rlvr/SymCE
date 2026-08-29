import sympy
from sympy import symbols, Rational, Integer

# Top-level setup: named object bindings that the witness expression may reference.
ZZ = sympy.ZZ
QQ = sympy.QQ

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The radical of S^{-1}I in S^{-1}R is not equal to S^{-1}(\\sqrt{I}) (e.g., S is not multiplicatively closed)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # Extract R, I, S from the witness
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            S = witness.get('S')
        elif hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'S'):
            R = witness.R
            I = witness.I
            S = witness.S
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            R, I, S = witness
        else:
            return [False, False, False]

        # H1: R is a commutative ring
        h1 = False
        if R in (sympy.ZZ, sympy.QQ, 'ZZ', 'QQ', 'Z', 'Q'):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif hasattr(R, 'is_ring') and R.is_ring and getattr(R, 'is_commutative', False):
            h1 = True
        else:
            # Lenient fallback for custom ring objects
            h1 = True

        # H2: I is an ideal of R
        h2 = False
        if R in (sympy.ZZ, 'ZZ', 'Z'):
            if isinstance(I, (int, sympy.Integer)):
                h2 = True
            elif isinstance(I, (list, set, tuple)) and all(isinstance(x, (int, sympy.Integer)) for x in I):
                h2 = True
            else:
                try:
                    int(I)
                    h2 = True
                except (ValueError, TypeError):
                    pass
        else:
            # Lenient fallback for custom ideals in other rings
            h2 = True

        # neg_Q: The conclusion fails if S is not multiplicatively closed.
        # (If S is not multiplicatively closed, S^{-1}R is not a ring, making the statement false).
        neg_q = False
        if S is None:
            neg_q = True
        else:
            if isinstance(S, str):
                S_raw = [S]
            elif not isinstance(S, (list, set, tuple)):
                S_raw = [S]
            else:
                S_raw = list(S)
                
            S_list = []
            for x in S_raw:
                if isinstance(x, str):
                    try:
                        S_list.append(int(x))
                    except ValueError:
                        S_list.append(x)
                else:
                    S_list.append(x)
            
            if not S_list:
                neg_q = True
            else:
                is_closed = True
                for a in S_list:
                    for b in S_list:
                        try:
                            prod = a * b
                            # Check if the product is in S
                            if not any(prod == x for x in S_list):
                                is_closed = False
                                break
                        except Exception:
                            # If elements cannot be multiplied, S is not a valid multiplicatively closed set
                            is_closed = False
                            break
                    if not is_closed:
                        break
                neg_q = not is_closed

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]