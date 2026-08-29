import sympy as sp
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = ['H_1: f(x) = x^4 - x^3 - 1 over Q', '¬Q: degree of extension is not 24 or Galois group is not S4']

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    f_val = None
    E_degree = None
    Gal_E = None

    try:
        if isinstance(witness, dict):
            f_val = witness.get('f', witness.get('f_x', witness.get('polynomial')))
            E_degree = witness.get('E_degree', witness.get('degree'))
            Gal_E = witness.get('Gal_E', witness.get('galois_group'))
        elif isinstance(witness, tuple):
            f_val = witness[0]
            if len(witness) > 1:
                E_degree = witness[1]
            if len(witness) > 2:
                Gal_E = witness[2]
        elif hasattr(witness, 'is_Expr') and witness.is_Expr:
            f_val = witness
        else:
            f_val = getattr(witness, 'f', witness)
            E_degree = getattr(witness, 'E_degree', None)
            Gal_E = getattr(witness, 'Gal_E', None)
    except Exception:
        pass

    try:
        if f_val is not None:
            if hasattr(f_val, 'as_expr'):
                f_expr = f_val.as_expr()
            else:
                f_expr = f_val
            if isinstance(f_expr, str):
                f_expr = sp.sympify(f_expr)
            diff = sp.simplify(f_expr - (x**4 - x**3 - 1))
            h1 = bool(diff == 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if E_degree is None and Gal_E is None:
            neg_q = True
        else:
            q_deg = (E_degree == 24) if E_degree is not None else True
            
            if Gal_E is None:
                q_gal = True
            elif isinstance(Gal_E, str):
                q_gal = (Gal_E == 'S4' or Gal_E == 'SymmetricGroup(4)')
            elif hasattr(Gal_E, 'is_isomorphic'):
                q_gal = Gal_E.is_isomorphic(S4)
            elif Gal_E == S4:
                q_gal = True
            else:
                q_gal = False
                
            neg_q = not (q_deg and q_gal)
    except Exception:
        neg_q = False

    return [h1, neg_q]