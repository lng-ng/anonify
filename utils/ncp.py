import numpy as np
import bigtree as bt

def num_leaves(root, node_name):
    node = bt.find_name(root, node_name)
    if (node.is_leaf):
        return 0
    return np.sum(1 for _ in bt.find_name(root, node_name).leaves)

class NCP():
    __slots__ = ['trees', 'cache', 'qids']

    def __init__(self, trees):
        self.cache = {k: {t.name: num_leaves(t, t.name)} for k, t in trees.items()}
        self.trees = trees
        self.qids = trees.keys()

    def ncp(self, record):
        res = 0
        for qid in self.qids:
            tree = self.trees[qid]
            n_leaves = None
            try:
                n_leaves = self.cache[qid][record[qid]]
            except KeyError:
                pass
            if n_leaves is None:
                n_leaves = num_leaves(tree, record[qid])
                self.cache[qid][record[qid]] = n_leaves
            res += n_leaves / self.cache[qid][tree.name]
        return res