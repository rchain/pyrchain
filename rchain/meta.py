from dataclasses import (
    _FIELD, _FIELD_INITVAR, _FIELDS, _HAS_DEFAULT_FACTORY, MISSING, Field,
    _create_fn, _set_new_attribute,
)
from typing import List

_PB_PARAM = "PB"
_FROM_PB = "__from_pb"


def _make_from_pb_fn(fields: List[Field]):
    globals = {'MISSING': MISSING,
               '_HAS_DEFAULT_FACTORY': _HAS_DEFAULT_FACTORY}
    locals = {f'_type_{f.name}': f.type for f in fields}
    globals.update({f'_pb_type_{f.name}': f.default_factory for f in fields if f.default_factory != MISSING})
    body_lines = []
    for field in fields:
        field_type_name = getattr(field.type, "_name", None)
        if field_type_name == "List":
            if field.default_factory != MISSING:
                body_lines.append(
                    "{}=[_pb_type_{}.from_pb(_pb) for _pb in {}.{}],".format(field.name, field.name, _PB_PARAM,
                                                                             field.name))
            else:
                body_lines.append("{}=[i for i in {}.{}],".format(field.name, _PB_PARAM, field.name))
        elif getattr(field.type, _FROM_PB, None):
            if field.default_factory == MISSING:
                raise ValueError("from pb class must provide a default factory")
            else:
                body_lines.append(
                    "{}=_pb_type_{}.from_pb({}.{}),".format(field.name, field.name, _PB_PARAM, field.name))
        else:
            body_lines.append("{}={}.{},".format(field.name, _PB_PARAM, field.name))
    body_lines.insert(0, "return cls(")
    body_lines.append(")")
    return _create_fn("from_pb", ["cls", _PB_PARAM], body_lines, globals=globals,
                      locals=locals)


def _process_cls(cls):
    fields = getattr(cls, _FIELDS, {})
    flds = [f for f in fields.values()
            if f._field_type in (_FIELD, _FIELD_INITVAR)]
    fn = _make_from_pb_fn(flds)
    _set_new_attribute(cls, "from_pb", classmethod(fn))
    _set_new_attribute(cls, _FROM_PB, True)
    return cls


def from_pb(_cls):
    """
    Make sure _cls is a wrap by dataclass.
    Generate a from_pb class method for the dataclass based
    on the dataclass definition.
    """

    def wrap(cls):
        return _process_cls(cls)

    if _cls is None:
        return wrap

    return wrap(_cls)
