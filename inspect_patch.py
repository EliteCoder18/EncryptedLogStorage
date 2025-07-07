import inspect
import collections

if not hasattr(inspect, 'getargspec'):
    def getargspec(func):
        sig = inspect.signature(func)
        args, varargs, keywords, defaults = [], None, None, []

        for p in sig.parameters.values():
            if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD):
                args.append(p.name)
                if p.default is not p.empty:
                    defaults.append(p.default)
            elif p.kind == p.VAR_POSITIONAL:
                varargs = p.name
            elif p.kind == p.VAR_KEYWORD:
                keywords = p.name

        return collections.namedtuple('ArgSpec', 'args varargs keywords defaults')(
            args, varargs, keywords, tuple(defaults) if defaults else None
        )

