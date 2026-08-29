import sympy as sp
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I(P, R) is the incidence algebra of P over R",
    "H_3: f in I(P, R)",
    "¬Q: f is a unit in I(P, R) iff f(x, x) is a unit in R for all x in P is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            P, leq, R, f = witness
        elif isinstance(witness, dict):
            P = witness['P']
            leq = witness['leq']
            R = witness['R']
            f = witness['f']
        else:
            P = witness.P
            leq = witness.leq
            R = witness.R
            f = witness.f
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        if R in ['Z', sp.ZZ]:
            R_type = 'Z'
        elif R in ['Q', sp.QQ, 'R', sp.RR, 'C', sp.CC]:
            R_type = 'F'
        else:
            R_type = 'Unknown'
            
        h1 = R_type in ['Z', 'F']
    except Exception:
        h1 = False

    # H_2: I(P, R) is the incidence algebra of P over R
    # This requires P to be a set and leq to be a valid preorder (reflexive and transitive)
    try:
        h2 = True
        if not isinstance(P, (list, set, tuple)):
            h2 = False
        else:
            leq_set = set(leq)
            # check reflexive
            for elem in P:
                if (elem, elem) not in leq_set:
                    h2 = False
                    break
            # check transitive
            if h2:
                for a in P:
                    for b in P:
                        for c in P:
                            if (a, b) in leq_set and (b, c) in leq_set:
                                if (a, c) not in leq_set:
                                    h2 = False
                                    break
    except Exception:
        h2 = False

    # H_3: f \in I(P, R)
    try:
        h3 = True
        leq_set = set(leq)
        
        if callable(f):
            f_eval = {}
            for a in P:
                for b in P:
                    val = f(a, b)
                    if val != 0 or (a, b) in leq_set:
                        f_eval[(a, b)] = val
        elif isinstance(f, dict):
            f_eval = f
        else:
            h3 = False
            f_eval = None
            
        if h3:
            for pair, val in f_eval.items():
                if pair not in leq_set and val != 0:
                    h3 = False
                    break
            if h3:
                for pair in leq_set:
                    if pair not in f_eval:
                        h3 = False
                        break
                    val = f_eval[pair]
                    if R_type == 'Z' and not isinstance(val, (int, sp.Integer)):
                        h3 = False
                        break
                    elif R_type == 'F' and not isinstance(val, (int, float, complex, sp.Expr)):
                        h3 = False
                        break
    except Exception:
        h3 = False

    # ¬Q: f is a unit in I(P, R) iff f(x, x) is a unit in R for all x in P is FALSE
    try:
        if not h3:
            neg_q = False
        else:
            n = len(P)
            P_list = list(P)
            idx = {elem: i for i, elem in enumerate(P_list)}
            
            M = sp.zeros(n, n)
            for (a, b) in leq:
                M[idx[a], idx[b]] = f_eval[(a, b)]
                
            det_M = M.det()
            
            if R_type == 'Z':
                is_unit_f = (det_M == 1 or det_M == -1)
            else:
                is_unit_f = (sp.simplify(det_M) != 0)
                
            all_diag_units = True
            for elem in P:
                val = f_eval[(elem, elem)]
                if R_type == 'Z':
                    if val not in [1, -1]:
                        all_diag_units = False
                        break
                else:
                    if sp.simplify(val) == 0:
                        all_diag_units = False
                        break
                        
            neg_q = (is_unit_f != all_diag_units)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]