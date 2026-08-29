import sympy as sp
from sympy import eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: lambda is an eigenvalue of A
    try:
        if isinstance(witness, dict):
            A = witness['A']
            lam = witness.get('lambda', witness.get('lam'))
        elif isinstance(witness, (tuple, list)):
            if hasattr(witness[0], 'eigenvals') and not hasattr(witness[1], 'eigenvals'):
                A, lam = witness[0], witness[1]
            elif hasattr(witness[1], 'eigenvals') and not hasattr(witness[0], 'eigenvals'):
                A, lam = witness[1], witness[0]
            else:
                A, lam = witness[0], witness[1]
        else:
            A, lam = witness.A, witness.lam
            
        evs = A.eigenvals()
        h1_ok = False
        for ev in evs:
            if sp.simplify(ev - lam) == 0:
                h1_ok = True
                break
    except Exception:
        h1_ok = False

    # ¬Q: The sum of the dimensions of all Jordan blocks corresponding to lambda in the Jordan canonical form of A is NOT equal to the algebraic multiplicity of lambda.
    try:
        if isinstance(witness, dict):
            A = witness['A']
            lam = witness.get('lambda', witness.get('lam'))
        elif isinstance(witness, (tuple, list)):
            if hasattr(witness[0], 'eigenvals') and not hasattr(witness[1], 'eigenvals'):
                A, lam = witness[0], witness[1]
            elif hasattr(witness[1], 'eigenvals') and not hasattr(witness[0], 'eigenvals'):
                A, lam = witness[1], witness[0]
            else:
                A, lam = witness[0], witness[1]
        else:
            A, lam = witness.A, witness.lam
            
        evs = A.eigenvals()
        alg_mult = 0
        for ev, mult in evs.items():
            if sp.simplify(ev - lam) == 0:
                alg_mult += mult
                
        P, J = A.jordan_form()
        # The sum of the dimensions of all Jordan blocks corresponding to lambda is exactly
        # the number of times lambda appears on the diagonal of the Jordan canonical form J.
        sum_dim = sum(1 for i in range(J.rows) if sp.simplify(J[i, i] - lam) == 0)
        
        neg_q_ok = bool(sum_dim != alg_mult)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: lambda is an eigenvalue of A",
    "¬Q: The sum of the dimensions of all Jordan blocks corresponding to lambda is not equal to the algebraic multiplicity of lambda"
]

N_HYP = 1
NEG_Q_INDEX = 1