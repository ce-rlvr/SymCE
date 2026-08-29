import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def extract_witness(witness):
    if isinstance(witness, dict):
        G = witness.get('G', witness.get('G_elements', []))
        H = witness.get('H', witness.get('H_elements', []))
        
        G_elements = list(G.generate()) if hasattr(G, 'generate') else list(G)
        H_elements = list(H.generate()) if hasattr(H, 'generate') else list(H)
        
        opG = witness.get('opG')
        if opG is None:
            opG = lambda x, y: x * y
            
        opH = witness.get('opH')
        if opH is None:
            opH = lambda x, y: x * y
            
        eG = witness.get('eG')
        if eG is None:
            eG = G.identity if hasattr(G, 'identity') else G_elements[0]
            
        eH = witness.get('eH')
        if eH is None:
            eH = H.identity if hasattr(H, 'identity') else H_elements[0]
            
        phi = witness.get('phi')
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        elif isinstance(phi, list):
            phi_dict = dict(phi)
            phi_func = lambda x: phi_dict[x]
        else:
            phi_func = phi
            
        return G_elements, H_elements, opG, opH, eG, eH, phi_func
        
    elif isinstance(witness, tuple) and len(witness) == 3:
        G, H, phi = witness
        G_elements = list(G.generate()) if hasattr(G, 'generate') else list(G)
        H_elements = list(H.generate()) if hasattr(H, 'generate') else list(H)
        opG = lambda x, y: x * y
        opH = lambda x, y: x * y
        eG = G.identity if hasattr(G, 'identity') else G_elements[0]
        eH = H.identity if hasattr(H, 'identity') else H_elements[0]
        
        if isinstance(phi, dict):
            phi_func = lambda x: phi[x]
        elif isinstance(phi, list):
            phi_dict = dict(phi)
            phi_func = lambda x: phi_dict[x]
        else:
            phi_func = phi
            
        return G_elements, H_elements, opG, opH, eG, eH, phi_func
    else:
        raise ValueError("Unknown witness format")

def conditions(witness) -> list[bool]:
    try:
        G_elements, H_elements, opG, opH, eG, eH, phi_func = extract_witness(witness)
    except Exception:
        return [False, False]
        
    # H1: phi is a group homomorphism
    try:
        h1_ok = True
        # Check phi maps G to H
        for x in G_elements:
            if phi_func(x) not in H_elements:
                h1_ok = False
                break
        
        # Check homomorphism property
        if h1_ok:
            for x in G_elements:
                for y in G_elements:
                    if phi_func(opG(x, y)) != opH(phi_func(x), phi_func(y)):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
                    
        # Check identity mapping
        if h1_ok:
            if phi_func(eG) != eH:
                h1_ok = False
                
    except Exception:
        h1_ok = False

    # neg_Q: phi is injective iff ker(phi) == {eG} is FALSE
    try:
        kernel = [x for x in G_elements if phi_func(x) == eH]
        is_kernel_trivial = (len(kernel) == 1 and kernel[0] == eG)
        
        is_injective = True
        seen = []
        for x in G_elements:
            fx = phi_func(x)
            if fx in seen:
                is_injective = False
                break
            seen.append(fx)
            
        neg_q = (is_injective != is_kernel_trivial)
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is a group homomorphism",
    "¬Q: phi is injective if and only if ker(phi) = {e_G} is false"
]

N_HYP = 1
NEG_Q_INDEX = 1