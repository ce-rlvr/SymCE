import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Symbol

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

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    The witness is expected to be a tuple (X, w), where:
      - X is a set of SymPy expressions (e.g., {x, x**-1}).
      - w is a list of tuples (g, sign) representing a reduced word in F(X),
        where g is in X and sign is 1 or -1.
    """
    # H_1: X is a set
    h1 = False
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            X, w = witness
            if isinstance(X, set):
                h1 = True
                # Verify all elements support the inverse operation
                for elem in X:
                    _ = elem**-1
    except Exception:
        h1 = False

    # H_2: w is an element of F(X)
    h2 = False
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            X, w = witness
            if isinstance(w, (list, tuple)):
                h2 = True
                for item in w:
                    if not isinstance(item, (list, tuple)) or len(item) != 2:
                        h2 = False
                        break
                    g, sign = item
                    if g not in X:
                        h2 = False
                        break
                    if sign not in {1, -1}:
                        h2 = False
                        break
                
                # Check if w is strictly reduced in the free group F(X)
                if h2:
                    for i in range(len(w) - 1):
                        if w[i][0] == w[i+1][0] and w[i][1] != w[i+1][1]:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # ¬Q: w CANNOT be uniquely represented by a reduced word over the alphabet X U X^-1
    neg_q = False
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            X, w = witness
            
            # Construct the unique candidate word over A = X U X^-1 that could evaluate to w.
            # Since any interpretation of a reduced word over A has no cancellations in F(X),
            # the length in F(X) equals the length in A. Furthermore, each letter in w uniquely
            # determines the corresponding letter in A.
            target_word = []
            for g, sign in w:
                if sign == 1:
                    target_word.append(g)
                else:
                    target_word.append(g**-1)
                    
            # Check if this unique candidate word is actually reduced over A.
            # If it is not reduced, then NO reduced word over A represents w.
            is_reduced = True
            for i in range(len(target_word) - 1):
                if target_word[i+1] == target_word[i]**-1:
                    is_reduced = False
                    break
                    
            # The conclusion fails (neg_q is True) if w is not uniquely represented.
            # This happens exactly when the unique candidate word is not reduced.
            neg_q = not is_reduced
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: w is an element of F(X)",
    "¬Q: w cannot be uniquely represented by a reduced word over X U X^-1"
]

N_HYP = 2
NEG_Q_INDEX = 2