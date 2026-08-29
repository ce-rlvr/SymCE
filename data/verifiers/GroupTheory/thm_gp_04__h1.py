import sympy
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

def get_exp_sums(rel, gens):
    if isinstance(rel, dict):
        return {g: rel.get(g, 0) for g in gens}
    elif isinstance(rel, str):
        s = rel.replace('**', '^').replace(' ', '')
        parts = s.split('*')
        exp_sums = {g: 0 for g in gens}
        for part in parts:
            if not part: continue
            if '^' in part:
                g, exp = part.split('^')
                if g in exp_sums:
                    exp_sums[g] += int(exp)
            else:
                g = part
                if g in exp_sums:
                    exp_sums[g] += 1
        return exp_sums
    else:
        return {g: 0 for g in gens}

def abelian_invariants_from_presentation(gens, rels):
    if not gens:
        return []
    matrix_data = []
    for r in rels:
        exp_sums = get_exp_sums(r, gens)
        row = [exp_sums[g] for g in gens]
        matrix_data.append(row)
    
    if not matrix_data:
        return [0] * len(gens)
        
    M = sympy.Matrix(matrix_data)
    try:
        snf = M.smith_normal_form()
        invs = [snf[i, i] for i in range(min(snf.rows, snf.cols))]
        if len(gens) > snf.rows:
            invs.extend([0] * (len(gens) - snf.rows))
        pos = sorted([int(x) for x in invs if x > 1 or x < -1])
        zeros = [0] * len([x for x in invs if x == 0])
        return pos + zeros
    except Exception:
        return []

def get_group_abelian_invariants(G):
    if hasattr(G, 'abelian_invariants'):
        invs = G.abelian_invariants()
        pos = sorted([int(x) for x in invs if x > 1 or x < -1])
        zeros = [0] * len([x for x in invs if x == 0])
        return pos + zeros
    return []

def combine_abelian_invariants(inv1, inv2):
    elements = list(inv1) + list(inv2)
    if not elements:
        return []
    M = sympy.diag(*elements)
    snf = M.smith_normal_form()
    invs = [snf[i, i] for i in range(min(snf.rows, snf.cols))]
    pos = sorted([int(x) for x in invs if x > 1 or x < -1])
    zeros = [0] * len([x for x in invs if x == 0])
    return pos + zeros

def conditions(witness) -> list[bool]:
    # Normalize inputs to lists
    X = witness.get('X', [])
    if isinstance(X, str): X = [X]
    else: X = list(X)
    
    R = witness.get('R', [])
    if isinstance(R, str): R = [R]
    else: R = list(R)
    
    Y = witness.get('Y', [])
    if isinstance(Y, str): Y = [Y]
    else: Y = list(Y)
    
    S = witness.get('S', [])
    if isinstance(S, str): S = [S]
    else: S = list(S)
    
    # H1: Let H be a group with presentation <Y | S>
    try:
        h1 = isinstance(Y, list) and isinstance(S, list)
    except Exception:
        h1 = False

    # H2: The sets of generators X and Y are disjoint
    try:
        h2 = set(X).isdisjoint(set(Y)) and len(set(X)) == len(X) and len(set(Y)) == len(Y)
    except Exception:
        h2 = False

    # neg_Q: G * H is NOT isomorphic to <X U Y | R U S>
    try:
        # Get G's abelian invariants
        if 'G' in witness:
            G_ab = get_group_abelian_invariants(witness['G'])
        else:
            G_gens = witness.get('G_gens', [])
            if isinstance(G_gens, str): G_gens = [G_gens]
            else: G_gens = list(G_gens)
            
            G_rels = witness.get('G_rels', [])
            if isinstance(G_rels, str): G_rels = [G_rels]
            else: G_rels = list(G_rels)
            
            G_ab = abelian_invariants_from_presentation(G_gens, G_rels)
            
        # Get H's abelian invariants
        H_ab = abelian_invariants_from_presentation(Y, S)
            
        # Abelian invariants of G * H
        GH_ab = combine_abelian_invariants(G_ab, H_ab)
        
        # Abelian invariants of <X U Y | R U S>
        XY_gens = list(X) + list(Y)
        XY_rels = list(R) + list(S)
        XY_ab = abelian_invariants_from_presentation(XY_gens, XY_rels)
        
        # If their abelianizations are not isomorphic, the groups are not isomorphic.
        neg_q = (GH_ab != XY_ab)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Let H be a group with presentation <Y | S>",
    "H_2: The sets of generators X and Y are disjoint",
    "¬Q: G * H is not isomorphic to <X U Y | R U S>"
]

N_HYP = 2
NEG_Q_INDEX = 2