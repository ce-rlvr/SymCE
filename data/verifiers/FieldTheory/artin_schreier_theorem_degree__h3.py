import sympy
from sympy.polys.domains import QQ, RR, CC

# Top-level setup
Q = QQ
R = RR
C = CC
QQbar = 'QQbar'

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the false conjecture.
    The witness should be a tuple of two fields (C, R), represented by SymPy domains or strings.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False, False]
        C_field, R_field = witness
    except Exception:
        return [False, False, False, False]
        
    def get_name(F):
        if isinstance(F, str):
            return F
        if hasattr(F, '__name__'):
            return F.__name__
        if hasattr(F, 'name'):
            return F.name
        return str(F)
        
    def is_alg_field(F):
        if isinstance(F, str):
            return 'AlgebraicField' in F or 'QQ<' in F
        if type(F).__name__ == 'AlgebraicField':
            return True
        if hasattr(F, 'is_AlgebraicField') and F.is_AlgebraicField:
            return True
        return False

    try:
        name_C = get_name(C_field)
        name_R = get_name(R_field)
    except Exception:
        return [False, False, False, False]
    
    # H1: C is an algebraically closed field
    try:
        h1 = name_C in ('CC', 'C', 'QQbar', 'Qbar', 'AlgebraicClosure(QQ)', 'AlgebraicClosure(Q)', 'Fpbar', 'F_p_bar', 'AlgebraicClosure(Fp)')
    except Exception:
        h1 = False
        
    # H2: R is a subfield of C
    try:
        h2 = False
        if name_C in ('CC', 'C'):
            if name_R in ('QQ', 'RR', 'CC', 'Q', 'R', 'C', 'QQbar', 'Qbar') or is_alg_field(R_field):
                h2 = True
        elif name_C in ('QQbar', 'Qbar', 'AlgebraicClosure(QQ)', 'AlgebraicClosure(Q)'):
            if name_R in ('QQ', 'Q', 'QQbar', 'Qbar') or is_alg_field(R_field):
                h2 = True
        elif name_C in ('RR', 'R'):
            if name_R in ('QQ', 'Q', 'RR', 'R') or is_alg_field(R_field):
                h2 = True
        elif name_C in ('Fpbar', 'F_p_bar', 'AlgebraicClosure(Fp)'):
            if name_R in ('Fp', 'F_p') or 'FiniteField' in name_R:
                h2 = True
    except Exception:
        h2 = False
        
    # H3: R is not equal to C
    try:
        same_field = False
        if name_C == name_R:
            same_field = True
        elif name_C in ('CC', 'C') and name_R in ('CC', 'C'):
            same_field = True
        elif name_C in ('QQbar', 'Qbar') and name_R in ('QQbar', 'Qbar'):
            same_field = True
        elif name_C in ('QQ', 'Q') and name_R in ('QQ', 'Q'):
            same_field = True
        elif name_C in ('RR', 'R') and name_R in ('RR', 'R'):
            same_field = True
            
        h3 = not same_field
    except Exception:
        h3 = False
        
    # neg_Q: The degree of the field extension C over R is not exactly 2
    try:
        deg = None
        if same_field:
            deg = 1
        elif name_C in ('CC', 'C'):
            if name_R in ('RR', 'R'):
                deg = 2
            elif name_R in ('QQ', 'Q', 'QQbar', 'Qbar') or is_alg_field(R_field):
                deg = float('inf')
        elif name_C in ('QQbar', 'Qbar', 'AlgebraicClosure(QQ)', 'AlgebraicClosure(Q)'):
            if name_R in ('QQ', 'Q') or is_alg_field(R_field):
                deg = float('inf')
        elif name_C in ('RR', 'R'):
            if name_R in ('QQ', 'Q') or is_alg_field(R_field):
                deg = float('inf')
        elif name_C in ('Fpbar', 'F_p_bar', 'AlgebraicClosure(Fp)'):
            if name_R in ('Fp', 'F_p') or 'FiniteField' in name_R:
                deg = float('inf')
                
        neg_q = (deg != 2) if deg is not None else False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: C is an algebraically closed field",
    "H_2: R is a subfield of C",
    "H_3: R is not equal to C",
    "¬Q: The degree of the field extension C over R is not exactly 2"
]

N_HYP = 3
NEG_Q_INDEX = 3