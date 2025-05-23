from imagehat.tools.dict_comparer import DictComparer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

console = Console()


class MetadataComparison:
    """
    Compare multiple metadata dictionaries against a pivot (the first one).

    Usage:
        mc = MetadataComparison([dict1, dict2, dict3])
        diffs = mc.compare_dicts()
        counts = mc.count_summary(diffs)
        mc.print_summary(diffs)
        details = mc.detailed_summary(diffs)
    """

    def __init__(self, metadata_dicts):
        if not isinstance(metadata_dicts, list) or len(metadata_dicts) < 2:
            raise ValueError(
                "Provide a list of at least two metadata dictionaries to compare."
            )
        if not all(isinstance(d, dict) for d in metadata_dicts):
            raise TypeError("All items in metadata_dicts must be dicts.")
        self.dicts = metadata_dicts
        self.pivot = metadata_dicts[0]

    def compare_dicts(self):
        """
        Compare each dict against pivot and return a dict of diffs.
        Keys are 1-based indices of comparisons.
        Each diff has 'added', 'removed', and 'difference' keys.
        """
        diffs = {}
        for idx, d in enumerate(self.dicts[1:], start=1):
            diffs[idx] = DictComparer(self.pivot, d).diff()
        return diffs

    def count_summary(self, diffs):
        """
        Return counts of added, removed, and changed keys per comparison.
        {index: {'added': n, 'removed': m, 'changed': k}}
        """
        counts = {}
        for idx, diff in diffs.items():
            counts[idx] = {
                "added": len(diff.get("added", {})),
                "removed": len(diff.get("removed", {})),
                "changed": len(diff.get("difference", {})),
            }
        return counts

    def print_summary(self, diffs, examples=3):
        """
        Print a rich-formatted summary with counts and example keys,
        using flattened paths for better insight.
        """
        flat_diffs = self.detailed_summary(diffs)

        for idx, summary in flat_diffs.items():
            console.rule(f"[bold blue]Comparison {idx} Detailed Summary")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Change Type", justify="left")
            table.add_column("Count", justify="right")
            table.add_column("Example Paths", justify="left")

            for change_type in ["added", "removed", "changed"]:
                paths = summary[change_type]
                if not paths:
                    continue
                sample = ", ".join(paths[:examples])
                if len(paths) > examples:
                    sample += f" ... and {len(paths) - examples} more"
                table.add_row(change_type.capitalize(), str(len(paths)), sample)

            console.print(table)
            console.print()

    def print_rich_tree(self, diffs, max_depth=4):
        """
        Print nested diff structure as a rich tree for each comparison.
        """

        def walk(tree, d, level=0):
            if level > max_depth:
                tree.add("[dim]... (depth limit reached)")
                return
            for action in ("added", "removed", "difference"):
                if action not in d or not d[action]:
                    continue
                branch = tree.add(f"[bold]{action.upper()}[/bold]")
                for k, v in d[action].items():
                    if isinstance(v, dict) and any(
                        isinstance(val, dict) for val in v.values()
                    ):
                        sub = branch.add(f"[cyan]{k}[/cyan]")
                        walk(sub, v, level + 1)
                    elif isinstance(v, dict) and "from" in v and "to" in v:
                        branch.add(
                            f"[magenta]{k}[/magenta]: [red]{v['from']}[/red] → [green]{v['to']}[/green]"
                        )
                    else:
                        branch.add(f"[cyan]{k}[/cyan]")

        for idx, diff in diffs.items():
            tree = Tree(f"📁 [bold yellow]Comparison {idx}[/bold yellow]")
            walk(tree, diff)
            console.print(tree)

    def detailed_summary(self, diffs):
        """
        Return full nested key-paths of added, removed, and changed keys.
        {index: {'added': [...], 'removed': [...], 'changed': [...]}}

        Useful for fine-grained comparison.
        """

        def recurse(changes, prefix=""):
            result = {"added": [], "removed": [], "changed": []}
            for action in ("added", "removed", "difference"):
                entries = changes.get(action, {})
                for key, val in entries.items():
                    path = f"{prefix}{key}"
                    if action == "difference":
                        result["changed"].append(path)
                    else:
                        result[action].append(path)
                    if action == "difference" and isinstance(val, dict):
                        sub = recurse(val, prefix=path + ".")
                        for act in sub:
                            result[act].extend(sub[act])
            return result

        summary = {}
        for idx, diff in diffs.items():
            summary[idx] = recurse(diff)
        return summary
