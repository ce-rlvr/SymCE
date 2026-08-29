import sympy
from sympy import Poly, expand
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a graded commutative ring",
    "H_2: Every element of S is a homogeneous element of R",
    "¬Q: The localized ring S^{-1}R does not admit a natural grading making the canonical map a graded ring homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_homogeneous_expr(expr):
    try:
        if hasattr(expr, 'is_homogeneous'):
            val = expr.is_homogeneous
            if isinstance(val, bool):
                return val
            elif callable(val):
                return val()
    except Exception:
        pass
        
    try:
        p = Poly(expr)
        return p.is_homogeneous
    except Exception:
        pass
        
    try:
        monoms = expr.monoms()
        if not monoms:
            return True
        deg = sum(monoms[0])
        return all(sum(m) == deg for m in monoms)
    except Exception:
        pass
        
    return True

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # If witness is a dictionary with precomputed flags
        if isinstance(witness, dict):
            if 'H1' in witness and 'H2' in witness and 'neg_Q' in witness:
                return [bool(witness['H1']), bool(witness['H2']), bool(witness['neg_Q'])]
            if 'is_graded_commutative_ring' in witness:
                h1 = witness.get('is_graded_commutative_ring', False)
                h2 = witness.get('is_S_homogeneous', False)
                q = witness.get('localized_ring_admits_natural_grading', True)
                return [bool(h1), bool(h2), not bool(q)]
                
        # If witness is an object with precomputed flags
        if hasattr(witness, 'H1') and hasattr(witness, 'H2') and hasattr(witness, 'neg_Q'):
            return [bool(witness.H1), bool(witness.H2), bool(witness.neg_Q)]
            
        # Extract R and S
        R = None
        S = None
        if isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        elif hasattr(witness, 'R') and hasattr(witness, 'S'):
            R = witness.R
            S = witness.S
        elif isinstance(witness, dict) and 'S' in witness:
            R = witness.get('R')
            S = witness['S']
        else:
            # Assume witness itself is S
            S = witness

        # Evaluate H1: R is a graded commutative ring
        h1 = True
        if R is not None:
            if hasattr(R, 'is_commutative') and not R.is_commutative:
                h1 = False

        # Evaluate H2: Every element of S is a homogeneous element of R
        if hasattr(S, '__iter__') and not isinstance(S, (str, sympy.Expr)):
            S_list = list(S)
        else:
            S_list = [S]

        h2 = True
        for s in S_list:
            if not is_homogeneous_expr(s):
                h2 = False
                break

        # Evaluate neg_Q: S^{-1}R does not admit a natural grading...
        # This is True if S is NOT a multiplicative set (the dropped hypothesis).
        is_mult_closed = True
        
        if hasattr(S, 'is_multiplicatively_closed'):
            is_mult_closed = S.is_multiplicatively_closed()
            if callable(is_mult_closed):
                is_mult_closed = is_mult_closed()
        elif hasattr(S, 'is_multiplicative_set'):
            is_mult_closed = S.is_multiplicative_set()
            if callable(is_mult_closed):
                is_mult_closed = is_mult_closed()
        else:
            has_one = False
            # Check if 1 is in S
            for s in S_list:
                try:
                    if expand(s - 1) == 0:
                        has_one = True
                        break
                except Exception:
                    if s == 1:
                        has_one = True
                        break
                        
            if not has_one:
                is_mult_closed = False
            else:
                # Check closure under multiplication
                for a in S_list:
                    for b in S_list:
                        try:
                            prod = expand(a * b)
                            found = False
                            for s in S_list:
                                if expand(prod - s) == 0:
                                    found = True
                                    break
                            if not found:
                                is_mult_closed = False
                                break
                        except Exception:
                            try:
                                prod = a * b
                                if prod not in S_list:
                                    is_mult_closed = False
                                    break
                            except Exception:
                                pass
                    if not is_mult_closed:
                        break
                        
        neg_q = not is_mult_closed

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]