import itertools

CONDITION_LABELS = [
    "H_1: Q_1 is a P_1-primary ideal in R",
    "H_2: Q_2 is a P_2-primary ideal in R",
    "H_3: P_1 is not contained in P_2",
    "H_4: P_2 is not contained in P_1",
    "¬Q: The intersection Q_1 \\cap Q_2 is a primary ideal"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        # If witness is a dictionary containing the pre-evaluated conditions
        if isinstance(witness, dict) and 'H_1' in witness:
            return [
                bool(witness.get('H_1', False)),
                bool(witness.get('H_2', False)),
                bool(witness.get('H_3', False)),
                bool(witness.get('H_4', False)),
                bool(witness.get('neg_Q', False))
            ]
            
        # If witness has a check method
        if hasattr(witness, 'check'):
            return witness.check()
            
        # Extract components
        if isinstance(witness, dict):
            R = witness.get('R')
            Q1 = witness.get('Q1')
            Q2 = witness.get('Q2')
            P1 = witness.get('P1')
            P2 = witness.get('P2')
        else:
            R = getattr(witness, 'R', None)
            Q1 = getattr(witness, 'Q1', None)
            Q2 = getattr(witness, 'Q2', None)
            P1 = getattr(witness, 'P1', None)
            P2 = getattr(witness, 'P2', None)

        # If R provides the necessary methods
        if R is not None and hasattr(R, 'is_primary'):
            h1 = R.is_primary(Q1, P1)
            h2 = R.is_primary(Q2, P2)
            h3 = not R.is_subset(P1, P2)
            h4 = not R.is_subset(P2, P1)
            Q_int = R.intersection(Q1, Q2)
            
            if hasattr(R, 'is_primary_ideal'):
                neg_q = R.is_primary_ideal(Q_int)
            elif hasattr(R, 'radical'):
                rad = R.radical(Q_int)
                neg_q = R.is_primary(Q_int, rad)
            else:
                neg_q = False
                
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
            
        # If witness provides the necessary methods
        if hasattr(witness, 'is_primary'):
            h1 = witness.is_primary(Q1, P1)
            h2 = witness.is_primary(Q2, P2)
            h3 = not witness.is_subset(P1, P2)
            h4 = not witness.is_subset(P2, P1)
            Q_int = witness.intersection(Q1, Q2)
            
            if hasattr(witness, 'is_primary_ideal'):
                neg_q = witness.is_primary_ideal(Q_int)
            elif hasattr(witness, 'radical'):
                rad = witness.radical(Q_int)
                neg_q = witness.is_primary(Q_int, rad)
            else:
                neg_q = False
                
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

    except Exception:
        pass

    return [False] * 5