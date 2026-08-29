import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a dictionary with keys:
      'G': list of group elements
      'op': callable for group operation f(g1, g2)
      'X': list of set elements
      'action': callable for group action f(g, x)
      'x': an element
    Alternatively, it can be a SymPy PermutationGroup or a tuple (PermutationGroup, x).
    """
    try:
        if hasattr(witness, 'is_abelian') and hasattr(witness, 'degree'):
            G_elems = list(witness.elements)
            witness_dict = {
                'G': G_elems,
                'op': lambda g1, g2: g1 * g2,
                'X': list(range(witness.degree)),
                'action': lambda g, p: g(p),
                'x': 0
            }
        elif isinstance(witness, tuple) and len(witness) == 2 and hasattr(witness[0], 'is_abelian'):
            G_elems = list(witness[0].elements)
            witness_dict = {
                'G': G_elems,
                'op': lambda g1, g2: g1 * g2,
                'X': list(range(witness[0].degree)),
                'action': lambda g, p: g(p),
                'x': witness[1]
            }
        else:
            witness_dict = witness
            
        G = witness_dict['G']
        op = witness_dict['op']
        X = witness_dict['X']
        action = witness_dict['action']
        x_elem = witness_dict['x']
    except Exception:
        return [False, False, False, False]

    # Find identity for G
    identity = None
    try:
        for e in G:
            is_id = True
            for g in G:
                if op(e, g) != g or op(g, e) != g:
                    is_id = False
                    break
            if is_id:
                identity = e
                break
    except Exception:
        pass

    # H1: G is an abelian group
    h1 = False
    try:
        closure = True
        for g1 in G:
            for g2 in G:
                if op(g1, g2) not in G:
                    closure = False
                    break
            if not closure: break
            
        if closure and identity is not None:
            assoc = True
            for g1 in G:
                for g2 in G:
                    for g3 in G:
                        if op(g1, op(g2, g3)) != op(op(g1, g2), g3):
                            assoc = False
                            break
                    if not assoc: break
                if not assoc: break
                
            if assoc:
                inv = True
                for g in G:
                    has_inv = False
                    for h in G:
                        if op(g, h) == identity and op(h, g) == identity:
                            has_inv = True
                            break
                    if not has_inv:
                        inv = False
                        break
                        
                if inv:
                    abelian = True
                    for g1 in G:
                        for g2 in G:
                            if op(g1, g2) != op(g2, g1):
                                abelian = False
                                break
                        if not abelian: break
                    h1 = abelian
    except Exception:
        h1 = False

    # H2: G acts transitively on X
    h2 = False
    try:
        if X and identity is not None:
            wd = True
            for g in G:
                for x in X:
                    if action(g, x) not in X:
                        wd = False
                        break
                if not wd: break
                
            if wd:
                id_acts_trivially = True
                for x in X:
                    if action(identity, x) != x:
                        id_acts_trivially = False
                        break
                        
                if id_acts_trivially:
                    compat = True
                    for g1 in G:
                        for g2 in G:
                            for x in X:
                                if action(g1, action(g2, x)) != action(op(g1, g2), x):
                                    compat = False
                                    break
                            if not compat: break
                        if not compat: break
                        
                    if compat:
                        transitive = True
                        for x1 in X:
                            for x2 in X:
                                reachable = False
                                for g in G:
                                    if action(g, x1) == x2:
                                        reachable = True
                                        break
                                if not reachable:
                                    transitive = False
                                    break
                            if not transitive: break
                        h2 = transitive
    except Exception:
        h2 = False

    # H3: x is an element of X
    h3 = False
    try:
        h3 = x_elem in X
    except Exception:
        h3 = False

    # neg_Q: G_x != Kernel
    neg_q = False
    try:
        G_x = []
        for g in G:
            if action(g, x_elem) == x_elem:
                G_x.append(g)
                
        kernel = []
        for g in G:
            acts_trivially = True
            for y in X:
                if action(g, y) != y:
                    acts_trivially = False
                    break
            if acts_trivially:
                kernel.append(g)
                
        G_x_in_kernel = True
        for g in G_x:
            if g not in kernel:
                G_x_in_kernel = False
                break
                
        kernel_in_G_x = True
        for g in kernel:
            if g not in G_x:
                kernel_in_G_x = False
                break
                
        neg_q = not (G_x_in_kernel and kernel_in_G_x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "H_2: G acts transitively on X",
    "H_3: x is an element of X",
    "¬Q: The point stabilizer G_x is not equal to the kernel of the action of G on X"
]

N_HYP = 3
NEG_Q_INDEX = 3