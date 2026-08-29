import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            p, q = witness
            if isinstance(p, int) and isinstance(q, int) and p >= 0 and q >= 0 and p + q > 0:
                h1 = True
                neg_q = (p > 0 and q > 0)
        elif isinstance(witness, int):
            if witness > 0:
                h1 = True
                neg_q = False
        elif isinstance(witness, str):
            s = witness.strip().replace(" ", "")
            if s.startswith("O(") and s.endswith(")"):
                inner = s[2:-1]
                if "," in inner:
                    parts = inner.split(",")
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        p, q = int(parts[0]), int(parts[1])
                        if p >= 0 and q >= 0 and p + q > 0:
                            h1 = True
                            neg_q = (p > 0 and q > 0)
                else:
                    if inner.isdigit():
                        n = int(inner)
                        if n > 0:
                            h1 = True
                            neg_q = False
        else:
            if isinstance(witness, list):
                witness = sp.Matrix(witness)
            
            if hasattr(witness, 'is_square') and witness.is_square:
                if witness == witness.T and witness.det() != 0:
                    h1 = True
                    is_pos = witness.is_positive_definite
                    is_neg = witness.is_negative_definite
                    if is_pos is None or is_neg is None:
                        evals = witness.eigenvals()
                        pos = any(sp.re(e) > 0 for e in evals)
                        neg = any(sp.re(e) < 0 for e in evals)
                        is_definite = (pos and not neg) or (neg and not pos)
                        neg_q = not is_definite
                    else:
                        neg_q = not (is_pos or is_neg)
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Consider O(n) as a subspace of R^{n x n} equipped with the standard Euclidean topology",
    "¬Q: The set O(n) is not a compact topological space"
]

N_HYP = 1
NEG_Q_INDEX = 1