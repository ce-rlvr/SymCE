import math
import itertools

class RealSubspace:
    """
    Represents standard topological spaces that can serve as counterexamples.
    Available spaces:
      - "Q": The rational numbers with the subspace topology from R.
      - "R": The real numbers with the standard topology.
      - "Z": The integers with the discrete topology.
      - "Harmonic": The subspace {0} U {1/n | n in Z+} of R.
    """
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return f"RealSubspace({self.name})"

# Top-level setup bindings for the witness expression to reference
Q_space = RealSubspace("Q")
R_space = RealSubspace("R")
Z_space = RealSubspace("Z")
Harmonic_space = RealSubspace("Harmonic")

def check_finite_topology(points, topology):
    try:
        points_set = set(points)
        topo_sets = [set(t) for t in topology]
        
        if set() not in topo_sets: return False
        if points_set not in topo_sets: return False
        
        for a in topo_sets:
            for b in topo_sets:
                if a.intersection(b) not in topo_sets:
                    return False
                if a.union(b) not in topo_sets:
                    return False
        return True
    except Exception:
        return False

def is_connected(points, topology, subset):
    try:
        subset = set(subset)
    except TypeError:
        subset = {subset}
    if not subset:
        return False
    rel_open = []
    for t in topology:
        ro = set(t).intersection(subset)
        if ro not in rel_open:
            rel_open.append(ro)
    
    for a in rel_open:
        if a != set() and a != subset:
            b = subset - a
            if b in rel_open:
                return False
    return True

def is_connected_component(points, topology, C):
    try:
        C_set = set(C)
    except TypeError:
        C_set = {C}
    if not is_connected(points, topology, C_set):
        return False
    for p in points:
        if p not in C_set:
            if is_connected(points, topology, C_set.union({p})):
                return False
    return True

def is_open_set(topology, C):
    try:
        C_set = set(C)
    except TypeError:
        C_set = {C}
    return C_set in [set(t) for t in topology]

def is_closed_set(points, topology, C):
    try:
        C_set = set(C)
    except TypeError:
        C_set = {C}
    comp = set(points) - C_set
    return is_open_set(topology, comp)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                X, C = witness
            elif len(witness) == 3:
                points, topology, C = witness
                X = (points, topology)
            else:
                return [False, False, False]
        elif hasattr(witness, "X") and hasattr(witness, "C"):
            X = witness.X
            C = witness.C
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # 1. Duck typing check for custom witness objects
    try:
        if hasattr(X, "is_topological_space") and callable(X.is_topological_space):
            h1 = bool(X.is_topological_space())
            if hasattr(X, "is_connected_component") and callable(X.is_connected_component):
                h2 = bool(X.is_connected_component(C))
            if h2 and hasattr(X, "is_open") and callable(X.is_open) and hasattr(X, "is_closed") and callable(X.is_closed):
                is_op = bool(X.is_open(C))
                is_cl = bool(X.is_closed(C))
                neg_q = not (is_op and is_cl)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Known real subspaces check
    try:
        space_name = None
        if isinstance(X, RealSubspace):
            space_name = X.name
        elif isinstance(X, str):
            space_name = X
        
        if space_name in ["Q", "R", "Z", "Harmonic"]:
            h1 = True
            
            if space_name == "Q":
                h2 = isinstance(C, (int, float, str)) or (isinstance(C, (set, frozenset, list, tuple)) and len(C) == 1)
            elif space_name == "R":
                h2 = C == "R" or C == R_space or (isinstance(C, (set, frozenset, list, tuple)) and set(C) == {"R"})
            elif space_name == "Z":
                h2 = isinstance(C, (int, str)) or (isinstance(C, (set, frozenset, list, tuple)) and len(C) == 1)
            elif space_name == "Harmonic":
                if isinstance(C, (set, frozenset, list, tuple)) and len(C) == 1:
                    val = list(C)[0]
                else:
                    val = C
                h2 = val in [0, 0.0, "0", "1/n"] or isinstance(val, (int, float, str))
            
            if h1 and h2:
                is_open = False
                is_closed = True
                
                if space_name == "Q":
                    is_open = False
                elif space_name == "R":
                    is_open = True
                elif space_name == "Z":
                    is_open = True
                elif space_name == "Harmonic":
                    val = list(C)[0] if isinstance(C, (set, frozenset, list, tuple)) else C
                    if val in [0, 0.0, "0"]:
                        is_open = False
                    else:
                        is_open = True
                
                neg_q = not (is_open and is_closed)
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Finite topology check
    try:
        if isinstance(X, tuple) and len(X) == 2:
            points, topology = X
            h1 = check_finite_topology(points, topology)
            if h1:
                h2 = is_connected_component(points, topology, C)
                if h2:
                    is_op = is_open_set(topology, C)
                    is_cl = is_closed_set(points, topology, C)
                    neg_q = not (is_op and is_cl)
            return [h1, h2, neg_q]
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: C is a connected component of X",
    "¬Q: C is not both open and closed in X"
]
N_HYP = 2
NEG_Q_INDEX = 2