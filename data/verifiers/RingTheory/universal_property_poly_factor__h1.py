import sympy

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("h1", False))
            h2 = bool(witness.get("h2", False))
            neg_q = bool(witness.get("neg_q", False))
            return [h1, h2, neg_q]
            
        if isinstance(witness, tuple) and len(witness) == 3:
            R, f, A = witness
            
            h1 = hasattr(f, 'subs') or isinstance(f, (sympy.Poly, sympy.Expr))
            
            if hasattr(A, 'is_commutative'):
                h2 = A.is_commutative is not False
            elif isinstance(A, (sympy.MatrixBase, sympy.MatrixSymbol)):
                h2 = False
            else:
                h2 = True
                
            if hasattr(R, 'is_commutative'):
                r_comm = R.is_commutative is not False
            elif isinstance(R, (sympy.MatrixBase, sympy.MatrixSymbol)):
                r_comm = False
            else:
                r_comm = True
                
            neg_q = not r_comm
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        return [False, False, False]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is a polynomial over R",
    "H_2: A is a commutative R-algebra",
    "not_Q: The natural bijection fails"
]

N_HYP = 2
NEG_Q_INDEX = 2