import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard groups
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

def make_word(word_tuple, F, names):
    """Helper to construct a free group word from a tuple of (generator_name, power)."""
    w = F.identity
    for gen_name, power in word_tuple:
        g = F.generators[names.index(gen_name)]
        w = w * (g ** power)
    return w

def check_H1(witness):
    if not isinstance(witness, dict): return False
    X = witness.get('X')
    R = witness.get('R')
    if not isinstance(X, list) or not all(isinstance(x, str) and x.isalnum() for x in X): return False
    if not isinstance(R, list): return False
    for word in R:
        if not isinstance(word, tuple): return False
        for gen, power in word:
            if gen not in X or not isinstance(power, int): return False
    return True

def check_H2(witness):
    X = witness.get('X')
    A = witness.get('A')
    B = witness.get('B')
    if not isinstance(A, list) or not isinstance(B, list): return False
    for word in A + B:
        if not isinstance(word, tuple): return False
        for gen, power in word:
            if gen not in X or not isinstance(power, int): return False
    return True

def check_H3(witness):
    A = witness.get('A')
    B = witness.get('B')
    alpha = witness.get('alpha')
    if not isinstance(alpha, dict): return False
    if set(alpha.keys()) != set(A): return False
    if set(alpha.values()) != set(B): return False
    return True

def check_neg_Q(witness):
    X_names = witness['X']
    
    # Construct the true HNN extension
    s_name = 's'
    while s_name in X_names:
        s_name += '_'
    true_names = X_names + [s_name]
    F_true = free_group(','.join(true_names))[0]
    
    R_true = [make_word(r, F_true, true_names) for r in witness['R']]
    s_gen = F_true.generators[-1]
    
    for a_tuple in witness['A']:
        a_mapped = make_word(a_tuple, F_true, true_names)
        alpha_a_mapped = make_word(witness['alpha'][a_tuple], F_true, true_names)
        rel = s_gen * a_mapped * (s_gen**-1) * (alpha_a_mapped**-1)
        R_true.append(rel)
        
    G_true = FpGroup(F_true, R_true)
    
    # Construct the presentation given in the conclusion
    if 't' not in X_names:
        c_names = X_names + ['t']
    else:
        c_names = X_names
        
    F_c = free_group(','.join(c_names))[0]
    
    R_c = [make_word(r, F_c, c_names) for r in witness['R']]
    t_gen = F_c.generators[c_names.index('t')]
    
    for a_tuple in witness['A']:
        a_mapped = make_word(a_tuple, F_c, c_names)
        alpha_a_mapped = make_word(witness['alpha'][a_tuple], F_c, c_names)
        rel = t_gen * a_mapped * (t_gen**-1) * (alpha_a_mapped**-1)
        R_c.append(rel)
        
    G_c = FpGroup(F_c, R_c)
    
    # If the groups are not isomorphic, their abelian invariants will differ
    inv_true = G_true.abelian_invariants()
    inv_c = G_c.abelian_invariants()
    
    return inv_true != inv_c

def conditions(witness):
    try:
        h1 = check_H1(witness)
    except Exception:
        h1 = False
        
    try:
        h2 = check_H2(witness)
    except Exception:
        h2 = False
        
    try:
        h3 = check_H3(witness)
    except Exception:
        h3 = False
        
    try:
        neg_q = check_neg_Q(witness)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group with presentation <X | R>",
    "H_2: A and B are subgroups of G",
    "H_3: alpha: A -> B is a group isomorphism",
    "¬Q: The presentation in the conclusion does not define the HNN extension"
]

N_HYP = 3
NEG_Q_INDEX = 3