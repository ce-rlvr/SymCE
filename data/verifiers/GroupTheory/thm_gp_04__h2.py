import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group with presentation <X | R>",
    "H_2: The sets of generators X and Y are disjoint",
    "¬Q: G * H is not isomorphic to <X U Y | R U S>"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False]

        X_str = [str(x) for x in witness.get('X', [])]
        Y_str = [str(y) for y in witness.get('Y', [])]
        R_str = [str(r) for r in witness.get('R', [])]
        S_str = [str(s) for s in witness.get('S', [])]

        H = witness.get('H', None)
        H_order_raw = witness.get('H_order', 1)
        if H is not None:
            try:
                H_order_raw = H.order()
            except Exception:
                pass
                
        if H_order_raw in [float('inf'), 'inf', sympy.oo, 'infinity']:
            H_order = float('inf')
        else:
            try:
                H_order = int(H_order_raw)
                if H_order < 1:
                    H_order = 1
            except Exception:
                H_order = 1

        def get_order(gens, rels):
            try:
                from sympy.combinatorics.free_groups import free_group
                from sympy.combinatorics.fp_groups import FpGroup
                if not gens:
                    return 1
                F = free_group(", ".join(gens))[0]
                gen_dict = {str(g): g for g in F.generators}
                parsed_rels = []
                for r in rels:
                    r_clean = str(r).replace('^', '**').strip()
                    if not r_clean or r_clean == '<identity>':
                        parsed_rels.append(F.identity)
                    else:
                        parsed_rels.append(eval(r_clean, {"__builtins__": {}}, gen_dict))
                G_fp = FpGroup(F, parsed_rels)
                return G_fp.order()
            except Exception:
                pass
            
            if not gens:
                return 1
            if len(gens) == 1:
                if not rels:
                    return float('inf')
                r = str(rels[0]).replace(' ', '').replace('^', '**')
                import re
                m = re.match(r'^[a-zA-Z_]+\*\*(\d+)$', r)
                if m:
                    return int(m.group(1))
                if r == gens[0]:
                    return 1
            return None

        G_order = get_order(X_str, R_str)
        h1 = G_order is not None

        try:
            h2 = set(X_str).isdisjoint(set(Y_str))
        except Exception:
            h2 = False

        try:
            if not h1:
                neg_q = False
            else:
                YS_order = get_order(Y_str, S_str)
                if YS_order is None:
                    neg_q = False
                else:
                    if G_order == 1:
                        pres_order = YS_order
                    elif YS_order == 1:
                        pres_order = G_order
                    else:
                        pres_order = float('inf')
                        
                    if G_order == 1:
                        GH_order = H_order
                    elif H_order == 1:
                        GH_order = G_order
                    else:
                        GH_order = float('inf')
                        
                    neg_q = (GH_order != pres_order)
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]