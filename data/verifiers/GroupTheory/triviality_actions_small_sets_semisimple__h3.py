import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
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

def conditions(witness):
    """
    witness is expected to be a tuple: (G, X, action_func)
    where:
      - G is a PermutationGroup
      - X is a list, tuple, or set representing the set
      - action_func is a callable f(g, x) -> x' defining the action
    """
    # H_1: G is a finite group
    try:
        G = witness[0]
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is a semisimple group
    try:
        G = witness[0]
        if not isinstance(G, PermutationGroup):
            h2 = False
        elif G.order() > 2000:
            # Guard against large groups to ensure fast verification
            h2 = False
        else:
            h2 = True
            # A finite group is semisimple if it has no non-trivial abelian normal subgroups
            for N in G.normal_subgroups():
                if N.order() > 1 and N.is_abelian:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # H_3: The cardinality of X is less than or equal to 4
    try:
        X = witness[1]
        h3 = isinstance(X, (list, tuple, set)) and len(X) <= 4
    except Exception:
        h3 = False

    # H_4: G acts on the set X
    try:
        G = witness[0]
        X = list(witness[1])
        action_func = witness[2]
        
        if not isinstance(G, PermutationGroup) or G.order() > 2000:
            h4 = False
        else:
            elements = list(G.generate())
            identity = next((g for g in elements if getattr(g, 'is_Identity', False)), elements[0]**0)
            
            h4 = True
            # Check identity acts trivially
            for x in X:
                if action_func(identity, x) != x:
                    h4 = False
                    break
            
            # Check closure
            if h4:
                for g in elements:
                    for x in X:
                        if action_func(g, x) not in X:
                            h4 = False
                            break
                    if not h4:
                        break

            # Check homomorphism property (allow either left or right action)
            if h4:
                is_left = True
                is_right = True
                for g in elements:
                    for h in elements:
                        gh = g * h
                        for x in X:
                            if is_left:
                                try:
                                    if action_func(gh, x) != action_func(g, action_func(h, x)):
                                        is_left = False
                                except Exception:
                                    is_left = False
                            if is_right:
                                try:
                                    if action_func(gh, x) != action_func(h, action_func(g, x)):
                                        is_right = False
                                except Exception:
                                    is_right = False
                        if not is_left and not is_right:
                            break
                    if not is_left and not is_right:
                        break
                h4 = is_left or is_right
    except Exception:
        h4 = False

    # ¬Q: The action of G on X is not the trivial action
    try:
        G = witness[0]
        X = list(witness[1])
        action_func = witness[2]
        
        if not isinstance(G, PermutationGroup) or G.order() > 2000:
            neg_q = False
        else:
            elements = list(G.generate())
            is_trivial = True
            for g in elements:
                for x in X:
                    if action_func(g, x) != x:
                        is_trivial = False
                        break
                if not is_trivial:
                    break
            neg_q = not is_trivial
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: The cardinality of X is less than or equal to 4",
    "H_4: G acts on the set X",
    "¬Q: The action of G on X is not the trivial action"
]

N_HYP = 4
NEG_Q_INDEX = 4