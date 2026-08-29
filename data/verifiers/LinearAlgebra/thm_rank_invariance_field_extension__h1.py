import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.polys.domains import QQ, ZZ, RR, CC, GF
from sympy.polys.matrices import DomainMatrix

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def in_domain(val, domain):
    try:
        from sympy import sympify
        val_sym = sympify(val)
        dom_val = domain.from_sympy(val_sym)
        return domain.to_sympy(dom_val) == val_sym
    except Exception:
        return False

def get_rank(A, domain):
    try:
        if hasattr(domain, 'characteristic') and domain.characteristic > 0:
            p = domain.characteristic
            from sympy import fraction
            def map_val(val):
                n, d = fraction(val)
                return (int(n) * pow(int(d), -1, int(p))) % int(p)
            try:
                A_mapped = A.applyfunc(map_val)
                dM = DomainMatrix.from_Matrix(A_mapped).convert_to(domain)
                return dM.rank()
            except Exception:
                pass
                
        dM = DomainMatrix.from_Matrix(A)
        dM = dM.convert_to(domain)
        return dM.rank()
    except Exception:
        return None

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            F = witness.get('F', QQ)
            K = witness.get('K')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                A, F, K = witness
            elif len(witness) == 2:
                A, K = witness
                F = QQ
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        from sympy import MatrixBase
        if isinstance(A, DomainMatrix):
            A = A.to_Matrix()
            
        if not isinstance(A, MatrixBase):
            h1 = False
        else:
            h1 = all(in_domain(e, F) for e in A)
    except Exception:
        h1 = False

    try:
        rank_F = get_rank(A, F)
        rank_K = get_rank(A, K)
        if rank_F is not None and rank_K is not None:
            neg_q = (rank_F != rank_K)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix with entries in F",
    "¬Q: The rank of A considered as a matrix over F is not equal to the rank of A considered as a matrix over K"
]

N_HYP = 1
NEG_Q_INDEX = 1