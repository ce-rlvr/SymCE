import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the conjecture.
    Returns [H_1, H_2, H_3, neg_Q].
    """
    h1 = False
    h2 = False
    h3 = False
    neg_q = False

    # Approach 1: Witness is a dictionary
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get("is_commutative_ring", False))
            h2 = bool(witness.get("is_ascending_chain", False))
            h3 = bool(witness.get("is_P_primary_chain", False))
            neg_q = not bool(witness.get("union_is_P_primary", True))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Approach 2: Witness is a tuple/list (R, P, Q_list, Q_union) or (R, Q_list, Q_union)
    try:
        if isinstance(witness, (tuple, list)) and len(witness) in (3, 4):
            if len(witness) == 4:
                R, P, Q_list, Q_union = witness
            else:
                R, Q_list, Q_union = witness
                P = Q_list[0].radical()
                
            try:
                h1 = bool(R.is_commutative())
            except Exception:
                h1 = False
                
            try:
                h2 = True
                for i in range(len(Q_list) - 1):
                    is_sub = False
                    if hasattr(Q_list[i], 'issubset'):
                        is_sub = Q_list[i].issubset(Q_list[i+1])
                    else:
                        is_sub = (Q_list[i] <= Q_list[i+1])
                    if not is_sub:
                        h2 = False
                        break
            except Exception:
                h2 = False
                
            try:
                h3 = True
                for Q in Q_list:
                    if not Q.is_primary() or Q.radical() != P:
                        h3 = False
                        break
            except Exception:
                h3 = False
                
            try:
                neg_q = not (Q_union.is_primary() and Q_union.radical() == P)
            except Exception:
                neg_q = False
                
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Approach 3: Witness has attributes R, P, Q_list, Q_union
    try:
        R = witness.R
        Q_list = witness.Q_list
        Q_union = witness.Q_union
        P = getattr(witness, 'P', None)
        if P is None:
            P = Q_list[0].radical()
            
        try:
            h1 = bool(R.is_commutative())
        except Exception:
            h1 = False
            
        try:
            h2 = True
            for i in range(len(Q_list) - 1):
                is_sub = False
                if hasattr(Q_list[i], 'issubset'):
                    is_sub = Q_list[i].issubset(Q_list[i+1])
                else:
                    is_sub = (Q_list[i] <= Q_list[i+1])
                if not is_sub:
                    h2 = False
                    break
        except Exception:
            h2 = False
            
        try:
            h3 = True
            for Q in Q_list:
                if not Q.is_primary() or Q.radical() != P:
                    h3 = False
                    break
        except Exception:
            h3 = False
            
        try:
            neg_q = not (Q_union.is_primary() and Q_union.radical() == P)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # Approach 4: Witness is an object with specific boolean methods/attributes
    try:
        h1 = bool(witness.is_commutative_ring())
    except Exception:
        try:
            h1 = bool(witness.is_commutative_ring)
        except Exception:
            h1 = False

    try:
        h2 = bool(witness.is_ascending_chain())
    except Exception:
        try:
            h2 = bool(witness.is_ascending_chain)
        except Exception:
            h2 = False

    try:
        h3 = bool(witness.is_P_primary_chain())
    except Exception:
        try:
            h3 = bool(witness.is_P_primary_chain)
        except Exception:
            h3 = False

    try:
        neg_q = not bool(witness.union_is_P_primary())
    except Exception:
        try:
            neg_q = not bool(witness.union_is_P_primary)
        except Exception:
            neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q_1 \\subseteq Q_2 \\subseteq \\dots is an ascending chain of ideals in R",
    "H_3: For all i \\geq 1, Q_i is a P-primary ideal",
    "¬Q: The union \\bigcup_{i=1}^\\infty Q_i is not a P-primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3