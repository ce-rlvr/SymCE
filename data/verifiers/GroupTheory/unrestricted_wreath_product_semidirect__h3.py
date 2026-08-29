import sympy
from sympy.combinatorics import PermutationGroup, Permutation, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def extract(witness):
    if isinstance(witness, tuple):
        if len(witness) == 4:
            A, B, Omega, action = witness
            return A, B, list(Omega), action
        if len(witness) == 2:
            A, B = witness
            Omega = list(range(B.degree))
            # Default to a left action (SymPy's natural action w^b is a right action, 
            # so w^(b**-1) gives a left action)
            action = lambda b, w: w ^ (b**-1)
            return A, B, Omega, action
    raise ValueError("Witness must be (A, B) or (A, B, Omega, action)")

def conditions(witness):
    try:
        A, B, Omega, action = extract(witness)
    except Exception:
        return [False, False, False]
        
    # H1: A and B are groups
    def is_group(G):
        return hasattr(G, 'elements') and hasattr(G, 'identity')
        
    try:
        h1_ok = is_group(A) and is_group(B)
    except Exception:
        h1_ok = False
        
    # H2: B acts on a set Omega
    try:
        e = B.identity
        h2_ok = True
        for w in Omega:
            if action(e, w) != w:
                h2_ok = False
                break
        if h2_ok:
            is_left = True
            is_right = True
            for b in B.elements:
                for c in B.elements:
                    for w in Omega:
                        bc = b * c
                        if action(bc, w) != action(b, action(c, w)):
                            is_left = False
                        if action(bc, w) != action(c, action(b, w)):
                            is_right = False
            h2_ok = is_left or is_right
    except Exception:
        h2_ok = False
        
    # neg_Q: The conclusion fails
    try:
        e = B.identity
        
        # The conclusion fails if B does not act faithfully on Omega.
        # In this case, the permutation wreath product A Wr_\Omega B is isomorphic 
        # to (A^\Omega \rtimes B) / K, which is not isomorphic to A^\Omega \rtimes B.
        is_faithful = True
        for b in B.elements:
            if b == e:
                continue
            if all(action(b, w) == w for w in Omega):
                is_faithful = False
                break
                
        # The conclusion also fails if the action is a right action but not a left action.
        # In this case, the specified \phi_b(f)(\omega) = f(b^{-1} \cdot \omega) 
        # is not a valid left action on A^\Omega, making the semidirect product undefined.
        is_left = True
        for b in B.elements:
            for c in B.elements:
                for w in Omega:
                    bc = b * c
                    if action(bc, w) != action(b, action(c, w)):
                        is_left = False
                        break
                if not is_left: break
            if not is_left: break
            
        neg_q_ok = (not is_faithful) or (not is_left)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "H_2: B acts on a set Omega",
    "¬Q: The unrestricted wreath product is not isomorphic to the semidirect product"
]

N_HYP = 2
NEG_Q_INDEX = 2