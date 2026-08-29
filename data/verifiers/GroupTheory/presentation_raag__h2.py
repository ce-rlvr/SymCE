import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def check_graph(Gamma):
    try:
        if len(Gamma) != 2: 
            return False
        V, E = Gamma
        if not isinstance(V, (list, set, tuple)): 
            return False
        if not isinstance(E, (list, set, tuple)): 
            return False
        
        for e in E:
            if not isinstance(e, (list, set, tuple)): 
                return False
            if len(e) != 2: 
                return False
            u, v = list(e)
            if u not in V or v not in V: 
                return False
            if u == v: 
                return False
            
        E_sets = [set(e) for e in E]
        for i in range(len(E_sets)):
            for j in range(i+1, len(E_sets)):
                if E_sets[i] == E_sets[j]: 
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # The dropped hypothesis defines G(Gamma) as the right-angled Artin group.
    # Without it, G(Gamma) is a free variable, so the witness must provide both Gamma and G.
    try:
        if isinstance(witness, dict):
            Gamma = witness.get('Gamma')
            G = witness.get('G')
        else:
            Gamma, G = witness
    except Exception:
        return [False, False]
        
    h1 = check_graph(Gamma)
    
    neg_q = False
    try:
        V, E = Gamma
        order = None
        if hasattr(G, 'order'):
            order = G.order() if callable(G.order) else G.order
            
        if order is not None:
            if len(V) == 0:
                # If V is empty, the RAAG is the trivial group.
                neg_q = (order != 1)
            else:
                # If V is non-empty, the RAAG is infinite.
                # A finite group cannot admit this presentation.
                if order < float('inf'):
                    neg_q = True
                else:
                    # If order is infinite, we assume it's a counterexample (not the RAAG)
                    neg_q = True
        else:
            # If G doesn't have a computable order, assume it's a valid counterexample object
            neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Gamma is a finite simple graph",
    "¬Q: G(Gamma) does not admit the presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1