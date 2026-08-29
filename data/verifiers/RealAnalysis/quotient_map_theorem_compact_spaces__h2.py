import itertools

def conditions(witness):
    try:
        # Normalize elements to strings to handle mixed types and JSON parsing artifacts
        X = sorted(list(set(str(x) for x in witness['X'])))
        Y = sorted(list(set(str(y) for y in witness['Y'])))
        
        def normalize(topology):
            normalized = []
            for s in topology:
                s_list = sorted(list(set(str(x) for x in s)))
                if s_list not in normalized:
                    normalized.append(s_list)
            return sorted(normalized)
            
        tau_X_norm = normalize(witness['tau_X'])
        tau_Y_norm = normalize(witness['tau_Y'])
        
        f = {str(k): str(v) for k, v in witness['f'].items()}
        
        # H1: X is a compact metric space
        # A finite topological space is a compact metric space if and only if it has the discrete topology.
        h1 = False
        if len(X) > 0:
            if len(tau_X_norm) == 2**len(X):
                all_subsets = []
                for r in range(len(X) + 1):
                    for combo in itertools.combinations(X, r):
                        all_subsets.append(sorted(list(combo)))
                if normalize(all_subsets) == tau_X_norm:
                    h1 = True
                    
        # H2: f: X -> Y is a continuous function
        h2 = False
        def is_topology(points, topology_norm):
            empty_set = []
            if empty_set not in topology_norm: return False
            full_set = sorted(list(points))
            if full_set not in topology_norm: return False
            for s1 in topology_norm:
                for s2 in topology_norm:
                    union = sorted(list(set(s1) | set(s2)))
                    if union not in topology_norm: return False
                    intersection = sorted(list(set(s1) & set(s2)))
                    if intersection not in topology_norm: return False
            return True
            
        if is_topology(Y, tau_Y_norm):
            if set(f.keys()) == set(X) and all(v in Y for v in f.values()):
                continuous = True
                for U in tau_Y_norm:
                    preimage = sorted([x for x in X if f[x] in U])
                    if preimage not in tau_X_norm:
                        continuous = False
                        break
                if continuous:
                    h2 = True
                    
        # H3: f is a surjective mapping
        h3 = False
        if set(f.values()) == set(Y):
            h3 = True
            
        # neg_Q: f is NOT a quotient map
        # f is a quotient map iff for every U subset of Y: U is open in Y <==> f^{-1}(U) is open in X.
        # Since f is continuous, U open in Y ==> f^{-1}(U) open in X.
        # Thus, f is NOT a quotient map if there exists U subset of Y such that
        # f^{-1}(U) is open in X, BUT U is NOT open in Y.
        neg_q = False
        for r in range(len(Y) + 1):
            for combo in itertools.combinations(Y, r):
                U = sorted(list(combo))
                preimage = sorted([x for x in X if f[x] in U])
                if preimage in tau_X_norm and U not in tau_Y_norm:
                    neg_q = True
                    break
            if neg_q:
                break
                
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: X is a compact metric space",
    "H_2: f: X -> Y is a continuous function",
    "H_3: f is a surjective mapping",
    "¬Q: f is not a quotient map"
]

N_HYP = 3
NEG_Q_INDEX = 3