import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            X = witness.get('X')
            action = witness.get('action')
            if 'X_N' in witness:
                X_N = witness['X_N']
                provided_X_N = True
            else:
                provided_X_N = False
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                G, N, X, action, X_N = witness
                provided_X_N = True
            elif len(witness) == 4:
                G, N, X, action = witness
                provided_X_N = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        def apply_action(g, x):
            if isinstance(action, dict):
                return action[(g, x)]
            return action(g, x)

        def get_inv(g):
            try:
                return ~g
            except Exception:
                return g**-1

        def get_unique(lst):
            res = []
            for item in lst:
                if item not in res:
                    res.append(item)
            return res

        try:
            G_elements = list(G.elements) if hasattr(G, 'elements') else list(G)
            N_elements = list(N.elements) if hasattr(N, 'elements') else list(N)
        except Exception:
            return [False, False, False]

        # H1: N is a normal subgroup of G
        h1 = False
        try:
            if len(G_elements) == 0 or len(N_elements) == 0:
                is_subgroup = False
            else:
                is_subgroup = True
                for n1 in N_elements:
                    for n2 in N_elements:
                        if (n1 * n2) not in N_elements:
                            is_subgroup = False
                            break
                    if not is_subgroup: break
                
                if is_subgroup:
                    for n in N_elements:
                        if get_inv(n) not in N_elements:
                            is_subgroup = False
                            break
                
                if is_subgroup:
                    for n in N_elements:
                        if n not in G_elements:
                            is_subgroup = False
                            break
            
            is_normal = is_subgroup
            if is_normal:
                for g in G_elements:
                    g_inv = get_inv(g)
                    for n in N_elements:
                        conj = g * n * g_inv
                        if conj not in N_elements:
                            is_normal = False
                            break
                    if not is_normal: break
            h1 = is_normal
        except Exception:
            h1 = False

        # H2: X^N is the set of all x \in X such that n \cdot x = x for all n \in N
        h2 = False
        try:
            expected_X_N = []
            for x in X:
                invariant = True
                for n in N_elements:
                    if apply_action(n, x) != x:
                        invariant = False
                        break
                if invariant:
                    expected_X_N.append(x)
            
            if provided_X_N:
                def is_equal_sets(list1, list2):
                    l2 = list(list2)
                    for item in list1:
                        if item in l2:
                            l2.remove(item)
                        else:
                            return False
                    return len(l2) == 0
                
                h2 = is_equal_sets(get_unique(list(X_N)), get_unique(expected_X_N))
            else:
                X_N = expected_X_N
                h2 = True
        except Exception:
            h2 = False

        # neg_Q: The set X^N is NOT invariant under the action of G
        neg_q = False
        try:
            unique_X_N = get_unique(list(X_N))
            for g in G_elements:
                for x in unique_X_N:
                    if apply_action(g, x) not in unique_X_N:
                        neg_q = True
                        break
                if neg_q: break
        except Exception:
            neg_q = False

        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: X^N is the set of all x in X such that n \\cdot x = x for all n in N",
    "¬Q: The set X^N is not invariant under the action of G"
]

N_HYP = 2
NEG_Q_INDEX = 2