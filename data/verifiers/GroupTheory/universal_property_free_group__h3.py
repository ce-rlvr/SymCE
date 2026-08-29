import sympy
from sympy.combinatorics import PermutationGroup, Permutation, free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: F is a free group on a set S",
    "H_2: G is a group",
    "¬Q: There does not exist a unique group homomorphism from F to G that extends f"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        F, S, G, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a free group on a set S
    try:
        if type(F).__name__ == 'FreeGroup':
            if isinstance(S, str):
                S_elements = S.replace(',', ' ').split()
            else:
                S_elements = list(S)
            S_strs = {str(s) for s in S_elements}
            F_gen_strs = {str(g) for g in F.generators}
            h1 = (S_strs == F_gen_strs) or (set(S_elements) == set(F.generators))
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: G is a group
    try:
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False
        
    # ¬Q: There does not exist a unique group homomorphism from F to G that extends f
    try:
        if not (type(F).__name__ == 'FreeGroup' and isinstance(G, PermutationGroup)):
            return [h1, h2, False]
            
        S_list = list(F.generators)
        G_elements = list(G.generate())
        if not G_elements:
            return [h1, h2, False]
            
        G_identity = G_elements[0] * ~G_elements[0]
        
        if isinstance(f, dict):
            items_to_check = list(f.items())
        elif callable(f):
            items_to_check = []
            for s in S_list:
                try:
                    items_to_check.append((s, f(s)))
                except Exception:
                    try:
                        items_to_check.append((s, f(str(s))))
                    except Exception:
                        pass
        elif isinstance(f, (list, tuple, set)):
            items_to_check = list(f)
        else:
            items_to_check = []
            
        def evaluate_word(w, A, G_identity):
            if hasattr(w, 'array_form'):
                res = G_identity
                for gen, power in w.array_form:
                    val = A[gen]
                    if power > 0:
                        for _ in range(power):
                            res = res * val
                    elif power < 0:
                        val_inv = ~val
                        for _ in range(-power):
                            res = res * val_inv
                return res
            elif w in A:
                return A[w]
            elif str(w) in A:
                return A[str(w)]
            else:
                raise ValueError("Cannot evaluate")

        extension_count = 0
        for prod in itertools.product(G_elements, repeat=len(S_list)):
            A = {}
            for s, g_val in zip(S_list, prod):
                A[s] = g_val
                A[str(s)] = g_val
                if hasattr(s, 'array_form') and len(s.array_form) == 1:
                    symb = s.array_form[0][0]
                    A[symb] = g_val
                    
            extends = True
            for k, v in items_to_check:
                try:
                    if evaluate_word(k, A, G_identity) != v:
                        extends = False
                        break
                except Exception:
                    extends = False
                    break
            if extends:
                extension_count += 1
                if extension_count > 1:
                    break
                    
        neg_q = (extension_count != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]