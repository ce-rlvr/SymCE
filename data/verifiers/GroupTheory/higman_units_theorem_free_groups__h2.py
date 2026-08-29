import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, u, v = witness
            elif len(witness) == 2:
                F, u = witness
                v = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def _clean_dict(d):
        res = {}
        for g, c in d.items():
            try:
                val = int(c)
                if val != c:
                    raise ValueError
            except Exception:
                raise ValueError("Coefficients must be integers")
            if val != 0:
                res[g] = val
        return res

    # H1: F is a free group
    try:
        h1 = isinstance(F, FreeGroup)
    except Exception:
        h1 = False

    # H2: u is an invertible element in the group ring
    try:
        if not h1:
            h2 = False
        else:
            if v is None:
                if isinstance(u, dict):
                    try:
                        u_clean = _clean_dict(u)
                        if len(u_clean) == 1:
                            g, c = list(u_clean.items())[0]
                            if c in (1, -1):
                                v = {g**-1: c}
                    except Exception:
                        pass
            
            if not isinstance(u, dict) or not isinstance(v, dict):
                h2 = False
            else:
                u_clean = _clean_dict(u)
                v_clean = _clean_dict(v)
                
                valid_u = all(getattr(g, 'group', None) == F for g in u_clean.keys())
                valid_v = all(getattr(g, 'group', None) == F for g in v_clean.keys())
                
                if not (valid_u and valid_v):
                    h2 = False
                else:
                    def multiply(d1, d2):
                        res = {}
                        for g1, c1 in d1.items():
                            for g2, c2 in d2.items():
                                g = g1 * g2
                                res[g] = res.get(g, 0) + c1 * c2
                        return {g: c for g, c in res.items() if c != 0}
                    
                    prod1 = multiply(u_clean, v_clean)
                    prod2 = multiply(v_clean, u_clean)
                    
                    id_elem = F.identity
                    expected = {id_elem: 1}
                    
                    h2 = (prod1 == expected) and (prod2 == expected)
    except Exception:
        h2 = False

    # neg_Q: u != g and u != -g for all g in F
    try:
        if not isinstance(u, dict):
            neg_q = False
        else:
            u_clean = _clean_dict(u)
            if len(u_clean) != 1:
                neg_q = True
            else:
                val = list(u_clean.values())[0]
                if val not in (1, -1):
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: F is a free group", "H_2: u is an invertible element in the group ring", "¬Q: u is not of the form g or -g for any g in F"]
N_HYP = 2
NEG_Q_INDEX = 2