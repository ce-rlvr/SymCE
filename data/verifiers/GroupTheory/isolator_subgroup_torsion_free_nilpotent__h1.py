import sympy
from sympy import eye, zeros, Matrix
import itertools
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

class IsolatorWitness:
    """
    Witness for the Isolator of a Subgroup conjecture.
    Provide 2x2 matrices over Q.
    G_gens: list of matrices generating G
    H_gens: list of matrices generating H (use [] for trivial subgroup)
    x, y: matrices in G such that x^n_x in H and y^n_y in H, but xy not in I(H)
    n_x, n_y: positive integers
    """
    def __init__(self, G_gens, H_gens, x, n_x, y, n_y):
        self.G_gens = G_gens
        self.H_gens = H_gens
        self.x = x
        self.n_x = n_x
        self.y = y
        self.n_y = n_y

def conditions(witness):
    try:
        h1_ok = False
        neg_q_ok = False
        
        def is_finite_order(M):
            if M.shape != (2, 2):
                return False
            if M == eye(2) or M == -eye(2):
                return True
            d = M.det()
            t = M.trace()
            if d == 1 and t in [-1, 0, 1]:
                return True
            if d == -1 and t == 0:
                return True
            return False

        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
            if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
                h1_ok = H.is_subgroup(G)
                return [bool(h1_ok), False]

        G_gens = []
        H_gens = []
        x = None
        y = None
        n_x = 1
        n_y = 1

        if isinstance(witness, IsolatorWitness):
            G_gens = witness.G_gens
            H_gens = witness.H_gens
            x = witness.x
            n_x = witness.n_x
            y = witness.y
            n_y = witness.n_y
        elif isinstance(witness, dict):
            G_gens = witness.get('G_gens', [])
            H_gens = witness.get('H_gens', [])
            x = witness.get('x', None)
            n_x = witness.get('n_x', 1)
            y = witness.get('y', None)
            n_y = witness.get('n_y', 1)
        elif isinstance(witness, tuple) and len(witness) == 2:
            G_gens, H_gens = witness
            if not (isinstance(G_gens, list) and all(isinstance(g, Matrix) for g in G_gens)):
                return [False, False]
        else:
            return [False, False]

        # Check H_1
        h1_ok = all(h in G_gens or h == eye(2) for h in H_gens) or len(H_gens) == 0

        # Check neg_Q
        if x is not None and y is not None:
            def in_H(mat):
                if mat == eye(mat.shape[0]): return True
                if any(mat == h for h in H_gens): return True
                return False
                
            x_in_IH = in_H(x**n_x) and n_x >= 1
            y_in_IH = in_H(y**n_y) and n_y >= 1
            
            try:
                xy = x * y
                if xy.shape != (2, 2):
                    xy_not_in_IH = False
                elif all(h == eye(2) for h in H_gens):
                    xy_not_in_IH = not is_finite_order(xy)
                else:
                    xy_not_in_IH = False
            except Exception:
                xy_not_in_IH = False
                
            neg_q_ok = x_in_IH and y_in_IH and xy_not_in_IH

        elif len(H_gens) == 0 or all(h == eye(2) for h in H_gens):
            # Search for x, y
            inv_gens = []
            for g in G_gens:
                try:
                    inv_gens.append(g.inv())
                except Exception:
                    pass
            pool = G_gens + inv_gens
            words = list(pool)
            for a in pool:
                for b in pool:
                    try:
                        words.append(a * b)
                    except Exception:
                        pass
            torsion = [w for w in words if is_finite_order(w)]
            for tx in torsion:
                for ty in torsion:
                    try:
                        if not is_finite_order(tx * ty):
                            neg_q_ok = True
                            break
                    except Exception:
                        pass
                if neg_q_ok:
                    break

        return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: I(H) is not a subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1