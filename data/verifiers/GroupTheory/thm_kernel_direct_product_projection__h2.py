import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def check_q_holds(G1, G2, pi):
    if not hasattr(G1, 'identity') or not hasattr(G2, 'identity'):
        return False
    if not hasattr(G1, 'elements') or not hasattr(G2, 'elements'):
        return False
        
    e1 = G1.identity
    e2 = G2.identity
    
    def eval_pi(g1, g2):
        if isinstance(pi, dict):
            if (g1, g2) in pi:
                return pi[(g1, g2)]
            raise ValueError("Missing key")
        try:
            return pi(g1, g2)
        except TypeError:
            return pi((g1, g2))
            
    G1_elems = list(G1.elements)
    G2_elems = list(G2.elements)
    
    image = set()
    for g1 in G1_elems:
        for g2 in G2_elems:
            val = eval_pi(g1, g2)
            image.add(val)
            
    if image != set(G1_elems):
        return False
        
    for g1 in G1_elems:
        for h1 in G1_elems:
            for g2 in G2_elems:
                for h2 in G2_elems:
                    if eval_pi(g1*h1, g2*h2) != eval_pi(g1, g2) * eval_pi(h1, h2):
                        return False
                        
    kernel = set()
    for g1 in G1_elems:
        for g2 in G2_elems:
            if eval_pi(g1, g2) == e1:
                kernel.add((g1, g2))
                
    expected_kernel = set((e1, g2) for g2 in G2_elems)
    if kernel != expected_kernel:
        return False
        
    return True

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        G1, G2, pi = witness
    except Exception:
        return [False, False]

    try:
        h1 = hasattr(G1, 'elements') and hasattr(G2, 'elements') and \
             hasattr(G1, 'identity') and hasattr(G2, 'identity')
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = True
        else:
            q_holds = check_q_holds(G1, G2, pi)
            neg_q = not q_holds
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G_1 and G_2 are groups",
    "¬Q: pi is not a surjective group homomorphism with kernel {e_1} x G_2"
]

N_HYP = 1
NEG_Q_INDEX = 1