import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_elements(group):
    if hasattr(group, 'elements'):
        try:
            return list(group.elements)
        except Exception:
            pass
    if hasattr(group, 'generate'):
        return list(group.generate())
    return list(group)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            N = witness.get('N')
            Phi = witness.get('Phi')
        else:
            G, N, Phi = witness
    except Exception:
        return [False, False, False]

    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False

    # neg_Q: The kernel of \Phi is NOT the centralizer C_G(N)
    try:
        G_elements = get_elements(G)
        N_elements = get_elements(N)
        
        G_identity = None
        for g in G_elements:
            if g * g == g:
                G_identity = g
                break
                
        if G_identity is None:
            return [h1, h2, False]

        # Compute C_G(N)
        C_G_N = set()
        for g in G_elements:
            if all(g * n == n * g for n in N_elements):
                C_G_N.add(g)
        
        ker_Phi = None
        
        if type(Phi).__name__ == 'GroupHomomorphism':
            try:
                ker_Phi = set(get_elements(Phi.kernel()))
            except Exception:
                pass
            
        if ker_Phi is None and isinstance(Phi, dict):
            try:
                id_target = Phi[G_identity]
                if all(g in Phi for g in G_elements):
                    ker_Phi = set(g for g in G_elements if Phi[g] == id_target)
            except Exception:
                pass
                
        if ker_Phi is None and callable(Phi):
            try:
                id_target = Phi(G_identity)
                if not callable(id_target):
                    valid = True
                    for g in G_elements:
                        try:
                            _ = Phi(g)
                        except Exception:
                            valid = False
                            break
                    if valid:
                        ker_Phi = set(g for g in G_elements if Phi(g) == id_target)
            except Exception:
                pass
                
        if ker_Phi is None:
            # Try as action
            id_acts_trivially = True
            for n in N_elements:
                phi_id_n = None
                if callable(Phi):
                    try:
                        phi_id_n = Phi(G_identity, n)
                    except Exception:
                        try:
                            phi_id_n = Phi(G_identity)(n)
                        except Exception:
                            pass
                elif isinstance(Phi, dict):
                    action_id = Phi.get(G_identity)
                    if callable(action_id):
                        try:
                            phi_id_n = action_id(n)
                        except Exception:
                            pass
                    elif isinstance(action_id, dict):
                        phi_id_n = action_id.get(n)
                if phi_id_n != n:
                    id_acts_trivially = False
                    break
            
            if id_acts_trivially:
                ker_Phi = set()
                for g in G_elements:
                    is_in_ker = True
                    for n in N_elements:
                        phi_g_n = None
                        if callable(Phi):
                            try:
                                phi_g_n = Phi(g, n)
                            except Exception:
                                try:
                                    phi_g_n = Phi(g)(n)
                                except Exception:
                                    pass
                        elif isinstance(Phi, dict):
                            action_g = Phi.get(g)
                            if callable(action_g):
                                try:
                                    phi_g_n = action_g(n)
                                except Exception:
                                    pass
                            elif isinstance(action_g, dict):
                                phi_g_n = action_g.get(n)
                        if phi_g_n != n:
                            is_in_ker = False
                            break
                    if is_in_ker:
                        ker_Phi.add(g)
                        
        if ker_Phi is not None:
            neg_q = (ker_Phi != C_G_N)
        else:
            neg_q = False
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: The kernel of \\Phi is not the centralizer C_G(N)"
]

N_HYP = 2
NEG_Q_INDEX = 2