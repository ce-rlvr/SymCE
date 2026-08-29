import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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

def get_elements(G):
    if hasattr(G, 'generate'):
        return list(G.generate())
    elif hasattr(G, 'elements'):
        return list(G.elements)
    else:
        return list(G)

def apply_map(f, x):
    if isinstance(f, dict):
        return f[x]
    return f(x)

def is_homomorphism_to_aut(H, N, phi):
    H_els = get_elements(H)
    N_els = get_elements(N)
    
    # Check if phi is a homomorphism from H to Aut(N)
    for h1 in H_els:
        for h2 in H_els:
            h12 = h1 * h2
            for n in N_els:
                if apply_map(apply_map(phi, h12), n) != apply_map(apply_map(phi, h1), apply_map(apply_map(phi, h2), n)):
                    return False
                    
    # Check if phi(h) is an automorphism of N for all h
    for h in H_els:
        img = []
        for n in N_els:
            try:
                pn = apply_map(apply_map(phi, h), n)
                img.append(pn)
            except Exception:
                return False
        if len(set(img)) != len(N_els):
            return False
        for n in img:
            if n not in N_els:
                return False
        for n1 in N_els:
            for n2 in N_els:
                if apply_map(apply_map(phi, h), n1 * n2) != apply_map(apply_map(phi, h), n1) * apply_map(apply_map(phi, h), n2):
                    return False
    return True

def is_valid_beta(H, N_els, phi, psi, beta):
    H_els = get_elements(H)
    img = []
    for h in H_els:
        try:
            bh = apply_map(beta, h)
            img.append(bh)
        except Exception:
            return False
            
    if len(set(img)) != len(H_els):
        return False
    for h in img:
        if h not in H_els:
            return False
            
    for h1 in H_els:
        for h2 in H_els:
            if apply_map(beta, h1 * h2) != apply_map(beta, h1) * apply_map(beta, h2):
                return False
                
    for h in H_els:
        bh = apply_map(beta, h)
        for n in N_els:
            if apply_map(apply_map(psi, h), n) != apply_map(apply_map(phi, bh), n):
                return False
    return True

def build_cayley_table(N_els, H_els, phi):
    elements = list(itertools.product(N_els, H_els))
    idx = {e: i for i, e in enumerate(elements)}
    n_tot = len(elements)
    table = [[0] * n_tot for _ in range(n_tot)]
    for i, (n1, h1) in enumerate(elements):
        for j, (n2, h2) in enumerate(elements):
            phi_h1_n2 = apply_map(apply_map(phi, h1), n2)
            n_res = n1 * phi_h1_n2
            h_res = h1 * h2
            table[i][j] = idx[(n_res, h_res)]
    return table

def cayley_to_permgroup(table):
    perms = [Permutation(row) for row in table]
    return PermutationGroup(perms)

def check_isomorphism(table1, table2):
    G1 = cayley_to_permgroup(table1)
    G2 = cayley_to_permgroup(table2)
    return G1.is_isomorphic(G2)

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness.get('N'), witness.get('H'), witness.get('phi'), witness.get('psi'), witness.get('beta')
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 4:
            return witness[0], witness[1], witness[2], witness[3], None
        elif len(witness) >= 5:
            return witness[0], witness[1], witness[2], witness[3], witness[4]
    return None, None, None, None, None

def conditions(witness) -> list[bool]:
    N, H, phi, psi, beta = parse_witness(witness)
    
    if N is None or H is None or phi is None or psi is None:
        return [False, False, False]
        
    # H_1: phi, psi are homomorphisms H -> Aut(N)
    try:
        h1_ok = is_homomorphism_to_aut(H, N, phi) and is_homomorphism_to_aut(H, N, psi)
    except Exception:
        h1_ok = False
        
    # H_2: exists beta in Aut(H) such that psi = phi o beta
    try:
        N_els = get_elements(N)
        H_els = get_elements(H)
        h2_ok = False
        if beta is not None:
            h2_ok = is_valid_beta(H, N_els, phi, psi, beta)
        else:
            if len(H_els) <= 8:
                for p in itertools.permutations(H_els):
                    beta_cand = dict(zip(H_els, p))
                    if is_valid_beta(H, N_els, phi, psi, beta_cand):
                        h2_ok = True
                        break
            else:
                h2_ok = False
    except Exception:
        h2_ok = False
        
    # neg_Q: N rtimes_phi H and N rtimes_psi H are NOT isomorphic
    try:
        N_els = get_elements(N)
        H_els = get_elements(H)
        table_phi = build_cayley_table(N_els, H_els, phi)
        table_psi = build_cayley_table(N_els, H_els, psi)
        is_iso = check_isomorphism(table_phi, table_psi)
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi and psi are homomorphisms from H to Aut(N)",
    "H_2: there exists an automorphism beta of H such that psi = phi o beta",
    "¬Q: the semidirect products N rtimes_phi H and N rtimes_psi H are not isomorphic"
]

N_HYP = 2
NEG_Q_INDEX = 2