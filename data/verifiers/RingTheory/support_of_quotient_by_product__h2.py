import sympy
from sympy.ntheory import primefactors

# Top-level setup
Z2 = sympy.Symbol('Z2')
Z3 = sympy.Symbol('Z3')

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture:
    Hypotheses:
      - R is a commutative ring
      - J is an ideal of R
    Conclusion:
      Supp(R/(IJ)) = Supp(R/I) U Supp(R/J)
    """
    # 1. Handle dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('R_is_commutative', True))
            h2 = bool(witness.get('J_is_ideal', True))
            if 'Supp_R_IJ' in witness:
                supp_IJ = set(witness['Supp_R_IJ'])
                supp_I = set(witness['Supp_R_I'])
                supp_J = set(witness['Supp_R_J'])
                neg_q = supp_IJ != supp_I.union(supp_J)
            else:
                neg_q = False
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Handle object with direct Supp attributes/methods
    try:
        if hasattr(witness, 'Supp_R_IJ'):
            h1 = bool(getattr(witness, 'R_is_commutative', True))
            h2 = bool(getattr(witness, 'J_is_ideal', True))
            
            s_IJ = getattr(witness, 'Supp_R_IJ')
            s_I = getattr(witness, 'Supp_R_I')
            s_J = getattr(witness, 'Supp_R_J')
            
            s_IJ = s_IJ() if callable(s_IJ) else s_IJ
            s_I = s_I() if callable(s_I) else s_I
            s_J = s_J() if callable(s_J) else s_J
            
            neg_q = set(s_IJ) != set(s_I).union(set(s_J))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Handle tuple (R, I, J) or object with R, I, J attributes
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
        else:
            R = witness.R
            I = witness.I
            J = witness.J
    except Exception:
        return [False, False, False]

    # Evaluate H1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative_ring'):
            h1 = bool(R.is_commutative_ring())
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        else:
            h1 = True
    except Exception:
        h1 = False

    # Evaluate H2: J is an ideal of R
    try:
        if hasattr(J, 'is_ideal'):
            h2 = bool(J.is_ideal(R) if callable(J.is_ideal) else J.is_ideal)
        elif hasattr(R, 'is_ideal'):
            h2 = bool(R.is_ideal(J))
        else:
            h2 = True
    except Exception:
        h2 = False

    # Evaluate neg_Q: Supp(R/(IJ)) != Supp(R/I) U Supp(R/J)
    try:
        if hasattr(R, 'supp'):
            supp_IJ = R.supp(I * J)
            supp_I = R.supp(I)
            supp_J = R.supp(J)
            neg_q = set(supp_IJ) != set(supp_I).union(set(supp_J))
        else:
            # Fallback to integers (Z)
            val_IJ = abs(int(I * J))
            val_I = abs(int(I))
            val_J = abs(int(J))
            
            supp_IJ = set(primefactors(val_IJ)) if val_IJ != 0 else 'all'
            supp_I = set(primefactors(val_I)) if val_I != 0 else 'all'
            supp_J = set(primefactors(val_J)) if val_J != 0 else 'all'
            
            if supp_IJ == 'all':
                neg_q = (supp_I != 'all' and supp_J != 'all')
            elif supp_I == 'all' or supp_J == 'all':
                neg_q = True
            else:
                neg_q = set(supp_IJ) != set(supp_I).union(set(supp_J))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: Supp(R/(IJ)) != Supp(R/I) U Supp(R/J)"
]

N_HYP = 2
NEG_Q_INDEX = 2