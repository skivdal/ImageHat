class DictComparer:
    """
    Compare two dictionaries and report differences.
    """

    def __init__(self, dict_a: dict, dict_b: dict):
        self.a = dict_a
        self.b = dict_b

    def keys_added(self) -> set:
        return set(self.b) - set(self.a)

    def keys_removed(self) -> set:
        return set(self.a) - set(self.b)

    def keys_shared(self) -> set:
        return set(self.a) & set(self.b)

    def changed(self) -> dict:
        diffs = {}
        for key in self.keys_shared():
            val_a, val_b = self.a[key], self.b[key]
            if isinstance(val_a, dict) and isinstance(val_b, dict):
                sub = DictComparer(val_a, val_b).diff()
                if sub:
                    diffs[key] = sub
            elif val_a != val_b:
                diffs[key] = {"from": val_a, "to": val_b}
        return diffs

    def diff(self) -> dict:
        return {
            "added": {k: self.b[k] for k in self.keys_added()},
            "removed": {k: self.a[k] for k in self.keys_removed()},
            "difference": self.changed(),
        }
