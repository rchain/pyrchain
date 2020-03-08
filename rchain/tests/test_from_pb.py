import random
import string
from dataclasses import dataclass, field
from typing import List
from unittest.mock import Mock

from ..meta import from_pb

try:
    # python3.6 doesn't have it
    from unittest.mock import seal
except ImportError:
    def seal(obj):
        return obj



@from_pb
@dataclass
class Class1:
    value1: str
    value2: int
    value3: List[str]
    value4: float


@from_pb
@dataclass
class ClassEmbedded:
    value2: str
    value1: Class1 = field(default_factory=Class1)


@from_pb
@dataclass
class ClassEmbeddedList:
    value1: str
    value2: int
    value3: List[str]
    value4: float
    value5: List[Class1] = field(default_factory=Class1)


def generate_Class1_pb():
    obj = Mock()
    obj.value1 = random.choice(string.ascii_lowercase)
    obj.value2 = random.randint(0, 1000)
    obj.value3 = [random.choice(string.ascii_lowercase) for _ in range(5)]
    obj.value4 = random.randint(1, 10000) / 10.0
    seal(obj)
    return obj


def generate_ClassEmbedded_pb():
    obj = Mock()
    obj.value1 = generate_Class1_pb()
    obj.value2 = random.choice(string.ascii_lowercase)
    seal(obj)
    return obj


def generate_ClassEmbeddedList_pb():
    obj = Mock()
    obj.value1 = random.choice(string.ascii_lowercase)
    obj.value2 = random.randint(0, 1000)
    obj.value3 = [random.choice(string.ascii_lowercase) for _ in range(5)]
    obj.value4 = random.randint(1, 10000) / 10.0
    obj.value5 = [generate_Class1_pb() for _ in range(2)]
    seal(obj)
    return obj


def test_simple_gen_from_pb():
    c1_pb = generate_Class1_pb()
    c1 = Class1.from_pb(c1_pb)
    assert c1.value1 == c1_pb.value1
    assert c1.value2 == c1_pb.value2
    assert c1.value3 == c1_pb.value3
    assert c1.value4 == c1_pb.value4


def test_gen_from_pb_embedded():
    embedded_pb = generate_ClassEmbedded_pb()
    c = ClassEmbedded.from_pb(embedded_pb)
    assert c.value1.value1 == embedded_pb.value1.value1
    assert c.value1.value2 == embedded_pb.value1.value2
    assert c.value1.value3 == embedded_pb.value1.value3
    assert c.value1.value4 == embedded_pb.value1.value4
    assert c.value2 == embedded_pb.value2


def test_gen_from_pb_embedded_list():
    embedded_pb = generate_ClassEmbeddedList_pb()
    embedded_obj = ClassEmbeddedList.from_pb(embedded_pb)
    assert embedded_obj.value1 == embedded_pb.value1
    assert embedded_obj.value2 == embedded_pb.value2
    assert embedded_obj.value3 == embedded_pb.value3
    assert embedded_obj.value4 == embedded_pb.value4
    for i in range(len(embedded_pb.value5)):
        assert embedded_obj.value5[i].value1 == embedded_pb.value5[i].value1
        assert embedded_obj.value5[i].value2 == embedded_pb.value5[i].value2
        assert embedded_obj.value5[i].value3 == embedded_pb.value5[i].value3
        assert embedded_obj.value5[i].value4 == embedded_pb.value5[i].value4
