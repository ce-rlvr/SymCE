import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a UFD",
    "H_2: Variables are algebraically independent",
    "H_3: M is the matrix of variables",
    "¬Q: The determinant polynomial is not irreducible"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        h1 = True
        n = None
        is_matrix = False
        matrix_obj = None
        
        if isinstance(witness, (int, sp.Integer)) and not isinstance(witness, bool):
            n = int(witness)
        elif isinstance(witness, sp.Matrix):
            n = witness.shape[0]
            is_matrix = True
            matrix_obj = witness
            if witness.shape[1] != n:
                return [False, False, False, False]
        elif isinstance(witness, (tuple, list)):
            for item in witness:
                if isinstance(item, (int, sp.Integer)) and not isinstance(item, bool):
                    n = int(item)
                elif isinstance(item, sp.Matrix):
                    n = item.shape[0]
                    is_matrix = True
                    matrix_obj = item
                    if item.shape[1] != n:
                        return [False, False, False, False]
                elif hasattr(item, 'is_UFD'):
                    if item.is_UFD is False:
                        h1 = False
        elif isinstance(witness, dict):
            if 'n' in witness:
                n_val = witness['n']
                if isinstance(n_val, (int, sp.Integer)) and not isinstance(n_val, bool):
                    n = int(n_val)
            if 'M' in witness:
                m_val = witness['M']
                if isinstance(m_val, sp.Matrix):
                    n = m_val.shape[0]
                    is_matrix = True
                    matrix_obj = m_val
                    if m_val.shape[1] != n:
                        return [False, False, False, False]
            if 'R' in witness:
                r_val = witness['R']
                if hasattr(r_val, 'is_UFD'):
                    if r_val.is_UFD is False:
                        h1 = False
                        
        if n is None or n < 0:
            return [False, False, False, False]
            
        h2 = True
        if is_matrix and matrix_obj is not None:
            entries = list(matrix_obj)
            if len(set(entries)) != n**2:
                h2 = False
            if not all(isinstance(e, sp.Symbol) for e in entries):
                h2 = False
                
        h3 = True
        
        # The determinant of an empty matrix (n=0) is 1.
        # 1 is a unit in any ring, and units are by definition not irreducible.
        # For n >= 1, the generic determinant is irreducible over any UFD.
        neg_q = (n == 0)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]