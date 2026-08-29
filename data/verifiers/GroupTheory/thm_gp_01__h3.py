import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def in_group(p, H):
    if hasattr(H, 'contains'):
        try:
            return H.contains(p)
        except Exception:
            pass
    try:
        return p in H
    except Exception:
        return False

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      - 'G': an optional sympy FpGroup (if provided, X and R are extracted from it)
      - 'X': list of strings (generators) - used if G is not provided
      - 'R': list of lists of strings (words, e.g. ['x', 'y^-1']) - used if G is not provided
      - 'H': a group object (e.g., PermutationGroup)
      - 'f': dict mapping generators to elements
    """
    try:
        G = witness.get('G')
        if G is not None and hasattr(G, 'generators') and hasattr(G, 'relators'):
            X = list(G.generators)
            R = list(G.relators)
            h1_ok = True
        else:
            X = witness.get('X')
            R = witness.get('R')
            h1_ok = False
            if isinstance(X, list) and all(isinstance(x, str) for x in X):
                if isinstance(R, list):
                    h1_ok = True
                    for word in R:
                        if not isinstance(word, list):
                            h1_ok = False
                            break
                        for token in word:
                            g = token[:-3] if token.endswith('^-1') else token
                            if g not in X:
                                h1_ok = False
                                break
    except Exception:
        h1_ok = False
        X = []
        R = []

    try:
        H = witness.get('H')
        h2_ok = hasattr(H, 'identity') and (hasattr(H, 'contains') or hasattr(H, '__contains__'))
    except Exception:
        h2_ok = False

    try:
        f = witness.get('f')
        h3_ok = False
        if isinstance(f, dict):
            f_norm = {str(k): v for k, v in f.items()}
            if all(str(x) in f_norm for x in X):
                identity = H.identity
                h3_ok = True
                for word in R:
                    val = identity
                    if hasattr(word, 'array_form'):
                        for gen, exp in word.array_form:
                            p = f_norm[str(gen)]
                            if exp > 0:
                                for _ in range(exp):
                                    val = val * p
                            else:
                                p_inv = p**-1
                                for _ in range(-exp):
                                    val = val * p_inv
                    else:
                        for token in word:
                            if token.endswith('^-1'):
                                g = token[:-3]
                                p = f_norm[str(g)]**-1
                            else:
                                g = token
                                p = f_norm[str(g)]
                            val = val * p
                    if val != identity:
                        h3_ok = False
                        break
    except Exception:
        h3_ok = False

    try:
        f = witness.get('f')
        f_norm = {}
        if isinstance(f, dict):
            for k, v in f.items():
                f_norm[str(k)] = v
                
        neg_q_ok = False
        hom_exists = True
        
        # A unique homomorphism phi: G -> H with phi(x) = f(x) exists iff 
        # f(x) is in H for all x AND f(r) evaluates to the identity in H for all r in R.
        for x in X:
            if str(x) not in f_norm or not in_group(f_norm[str(x)], H):
                hom_exists = False
                break
        
        if hom_exists:
            identity = H.identity
            for word in R:
                val = identity
                if hasattr(word, 'array_form'):
                    for gen, exp in word.array_form:
                        p = f_norm[str(gen)]
                        if exp > 0:
                            for _ in range(exp):
                                val = val * p
                        else:
                            p_inv = p**-1
                            for _ in range(-exp):
                                val = val * p_inv
                else:
                    for token in word:
                        if token.endswith('^-1'):
                            g = token[:-3]
                            p = f_norm[str(g)]**-1
                        else:
                            g = token
                            p = f_norm[str(g)]
                        val = val * p
                if val != identity:
                    hom_exists = False
                    break
                    
        neg_q_ok = not hom_exists
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group defined by the presentation <X | R>",
    "H_2: H is a group",
    "H_3: For every word r in R, the substitution of f(x) for each x in X in r yields the identity element in H",
    "¬Q: There does not exist a unique group homomorphism phi: G -> H such that phi(x) = f(x) for all x in X"
]

N_HYP = 3
NEG_Q_INDEX = 3