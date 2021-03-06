# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from .CasperMessage_pb2 import (
    PeekProto as CasperMessage_pb2___PeekProto,
)

from .RhoTypes_pb2 import (
    BindPattern as RhoTypes_pb2___BindPattern,
    ListParWithRandom as RhoTypes_pb2___ListParWithRandom,
    Par as RhoTypes_pb2___Par,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
    Text as typing___Text,
    Union as typing___Union,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode


class FindDeployQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    deployId = ... # type: builtin___bytes

    def __init__(self,
        *,
        deployId : typing___Optional[builtin___bytes] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> FindDeployQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> FindDeployQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"deployId",b"deployId"]) -> None: ...

class BlockQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    hash = ... # type: typing___Text

    def __init__(self,
        *,
        hash : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BlockQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> BlockQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"hash",b"hash"]) -> None: ...

class BlocksQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    depth = ... # type: builtin___int

    def __init__(self,
        *,
        depth : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BlocksQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> BlocksQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"depth",b"depth"]) -> None: ...

class BlocksQueryByHeight(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    startBlockNumber = ... # type: builtin___int
    endBlockNumber = ... # type: builtin___int

    def __init__(self,
        *,
        startBlockNumber : typing___Optional[builtin___int] = None,
        endBlockNumber : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BlocksQueryByHeight: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> BlocksQueryByHeight: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"endBlockNumber",b"endBlockNumber",u"startBlockNumber",b"startBlockNumber"]) -> None: ...

class DataAtNameQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    depth = ... # type: builtin___int

    @property
    def name(self) -> RhoTypes_pb2___Par: ...

    def __init__(self,
        *,
        depth : typing___Optional[builtin___int] = None,
        name : typing___Optional[RhoTypes_pb2___Par] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> DataAtNameQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> DataAtNameQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"name",b"name"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"depth",b"depth",u"name",b"name"]) -> None: ...

class ContinuationAtNameQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    depth = ... # type: builtin___int

    @property
    def names(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[RhoTypes_pb2___Par]: ...

    def __init__(self,
        *,
        depth : typing___Optional[builtin___int] = None,
        names : typing___Optional[typing___Iterable[RhoTypes_pb2___Par]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ContinuationAtNameQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ContinuationAtNameQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"depth",b"depth",u"names",b"names"]) -> None: ...

class VisualizeDagQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    depth = ... # type: builtin___int
    showJustificationLines = ... # type: builtin___bool
    startBlockNumber = ... # type: builtin___int

    def __init__(self,
        *,
        depth : typing___Optional[builtin___int] = None,
        showJustificationLines : typing___Optional[builtin___bool] = None,
        startBlockNumber : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> VisualizeDagQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> VisualizeDagQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"depth",b"depth",u"showJustificationLines",b"showJustificationLines",u"startBlockNumber",b"startBlockNumber"]) -> None: ...

class MachineVerifyQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    def __init__(self,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> MachineVerifyQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> MachineVerifyQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class PrivateNamePreviewQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    user = ... # type: builtin___bytes
    timestamp = ... # type: builtin___int
    nameQty = ... # type: builtin___int

    def __init__(self,
        *,
        user : typing___Optional[builtin___bytes] = None,
        timestamp : typing___Optional[builtin___int] = None,
        nameQty : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> PrivateNamePreviewQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> PrivateNamePreviewQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"nameQty",b"nameQty",u"timestamp",b"timestamp",u"user",b"user"]) -> None: ...

class LastFinalizedBlockQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    def __init__(self,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> LastFinalizedBlockQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> LastFinalizedBlockQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...

class IsFinalizedQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    hash = ... # type: typing___Text

    def __init__(self,
        *,
        hash : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> IsFinalizedQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> IsFinalizedQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"hash",b"hash"]) -> None: ...

class BondStatusQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    publicKey = ... # type: builtin___bytes

    def __init__(self,
        *,
        publicKey : typing___Optional[builtin___bytes] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BondStatusQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> BondStatusQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"publicKey",b"publicKey"]) -> None: ...

class ExploratoryDeployQuery(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    term = ... # type: typing___Text
    blockHash = ... # type: typing___Text
    usePreStateHash = ... # type: builtin___bool

    def __init__(self,
        *,
        term : typing___Optional[typing___Text] = None,
        blockHash : typing___Optional[typing___Text] = None,
        usePreStateHash : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ExploratoryDeployQuery: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ExploratoryDeployQuery: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"blockHash",b"blockHash",u"term",b"term",u"usePreStateHash",b"usePreStateHash"]) -> None: ...

class BondInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    validator = ... # type: typing___Text
    stake = ... # type: builtin___int

    def __init__(self,
        *,
        validator : typing___Optional[typing___Text] = None,
        stake : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BondInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> BondInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"stake",b"stake",u"validator",b"validator"]) -> None: ...

class JustificationInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    validator = ... # type: typing___Text
    latestBlockHash = ... # type: typing___Text

    def __init__(self,
        *,
        validator : typing___Optional[typing___Text] = None,
        latestBlockHash : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> JustificationInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> JustificationInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"latestBlockHash",b"latestBlockHash",u"validator",b"validator"]) -> None: ...

class DeployInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    deployer = ... # type: typing___Text
    term = ... # type: typing___Text
    timestamp = ... # type: builtin___int
    sig = ... # type: typing___Text
    sigAlgorithm = ... # type: typing___Text
    phloPrice = ... # type: builtin___int
    phloLimit = ... # type: builtin___int
    validAfterBlockNumber = ... # type: builtin___int
    cost = ... # type: builtin___int
    errored = ... # type: builtin___bool
    systemDeployError = ... # type: typing___Text

    def __init__(self,
        *,
        deployer : typing___Optional[typing___Text] = None,
        term : typing___Optional[typing___Text] = None,
        timestamp : typing___Optional[builtin___int] = None,
        sig : typing___Optional[typing___Text] = None,
        sigAlgorithm : typing___Optional[typing___Text] = None,
        phloPrice : typing___Optional[builtin___int] = None,
        phloLimit : typing___Optional[builtin___int] = None,
        validAfterBlockNumber : typing___Optional[builtin___int] = None,
        cost : typing___Optional[builtin___int] = None,
        errored : typing___Optional[builtin___bool] = None,
        systemDeployError : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> DeployInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> DeployInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"cost",b"cost",u"deployer",b"deployer",u"errored",b"errored",u"phloLimit",b"phloLimit",u"phloPrice",b"phloPrice",u"sig",b"sig",u"sigAlgorithm",b"sigAlgorithm",u"systemDeployError",b"systemDeployError",u"term",b"term",u"timestamp",b"timestamp",u"validAfterBlockNumber",b"validAfterBlockNumber"]) -> None: ...

class LightBlockInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    blockHash = ... # type: typing___Text
    sender = ... # type: typing___Text
    seqNum = ... # type: builtin___int
    sig = ... # type: typing___Text
    sigAlgorithm = ... # type: typing___Text
    shardId = ... # type: typing___Text
    extraBytes = ... # type: builtin___bytes
    version = ... # type: builtin___int
    timestamp = ... # type: builtin___int
    headerExtraBytes = ... # type: builtin___bytes
    parentsHashList = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text]
    blockNumber = ... # type: builtin___int
    preStateHash = ... # type: typing___Text
    postStateHash = ... # type: typing___Text
    bodyExtraBytes = ... # type: builtin___bytes
    blockSize = ... # type: typing___Text
    deployCount = ... # type: builtin___int
    faultTolerance = ... # type: builtin___float

    @property
    def bonds(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[BondInfo]: ...

    @property
    def justifications(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[JustificationInfo]: ...

    def __init__(self,
        *,
        blockHash : typing___Optional[typing___Text] = None,
        sender : typing___Optional[typing___Text] = None,
        seqNum : typing___Optional[builtin___int] = None,
        sig : typing___Optional[typing___Text] = None,
        sigAlgorithm : typing___Optional[typing___Text] = None,
        shardId : typing___Optional[typing___Text] = None,
        extraBytes : typing___Optional[builtin___bytes] = None,
        version : typing___Optional[builtin___int] = None,
        timestamp : typing___Optional[builtin___int] = None,
        headerExtraBytes : typing___Optional[builtin___bytes] = None,
        parentsHashList : typing___Optional[typing___Iterable[typing___Text]] = None,
        blockNumber : typing___Optional[builtin___int] = None,
        preStateHash : typing___Optional[typing___Text] = None,
        postStateHash : typing___Optional[typing___Text] = None,
        bodyExtraBytes : typing___Optional[builtin___bytes] = None,
        bonds : typing___Optional[typing___Iterable[BondInfo]] = None,
        blockSize : typing___Optional[typing___Text] = None,
        deployCount : typing___Optional[builtin___int] = None,
        faultTolerance : typing___Optional[builtin___float] = None,
        justifications : typing___Optional[typing___Iterable[JustificationInfo]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> LightBlockInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> LightBlockInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"blockHash",b"blockHash",u"blockNumber",b"blockNumber",u"blockSize",b"blockSize",u"bodyExtraBytes",b"bodyExtraBytes",u"bonds",b"bonds",u"deployCount",b"deployCount",u"extraBytes",b"extraBytes",u"faultTolerance",b"faultTolerance",u"headerExtraBytes",b"headerExtraBytes",u"justifications",b"justifications",u"parentsHashList",b"parentsHashList",u"postStateHash",b"postStateHash",u"preStateHash",b"preStateHash",u"sender",b"sender",u"seqNum",b"seqNum",u"shardId",b"shardId",u"sig",b"sig",u"sigAlgorithm",b"sigAlgorithm",u"timestamp",b"timestamp",u"version",b"version"]) -> None: ...

class BlockInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def blockInfo(self) -> LightBlockInfo: ...

    @property
    def deploys(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[DeployInfo]: ...

    def __init__(self,
        *,
        blockInfo : typing___Optional[LightBlockInfo] = None,
        deploys : typing___Optional[typing___Iterable[DeployInfo]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BlockInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> BlockInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"blockInfo",b"blockInfo"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"blockInfo",b"blockInfo",u"deploys",b"deploys"]) -> None: ...

class DataWithBlockInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def postBlockData(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[RhoTypes_pb2___Par]: ...

    @property
    def block(self) -> LightBlockInfo: ...

    def __init__(self,
        *,
        postBlockData : typing___Optional[typing___Iterable[RhoTypes_pb2___Par]] = None,
        block : typing___Optional[LightBlockInfo] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> DataWithBlockInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> DataWithBlockInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"block",b"block"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"block",b"block",u"postBlockData",b"postBlockData"]) -> None: ...

class ContinuationsWithBlockInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def postBlockContinuations(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[WaitingContinuationInfo]: ...

    @property
    def block(self) -> LightBlockInfo: ...

    def __init__(self,
        *,
        postBlockContinuations : typing___Optional[typing___Iterable[WaitingContinuationInfo]] = None,
        block : typing___Optional[LightBlockInfo] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ContinuationsWithBlockInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ContinuationsWithBlockInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"block",b"block"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"block",b"block",u"postBlockContinuations",b"postBlockContinuations"]) -> None: ...

class WaitingContinuationInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def postBlockPatterns(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[RhoTypes_pb2___BindPattern]: ...

    @property
    def postBlockContinuation(self) -> RhoTypes_pb2___Par: ...

    def __init__(self,
        *,
        postBlockPatterns : typing___Optional[typing___Iterable[RhoTypes_pb2___BindPattern]] = None,
        postBlockContinuation : typing___Optional[RhoTypes_pb2___Par] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> WaitingContinuationInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> WaitingContinuationInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"postBlockContinuation",b"postBlockContinuation"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"postBlockContinuation",b"postBlockContinuation",u"postBlockPatterns",b"postBlockPatterns"]) -> None: ...

class ReportProduceProto(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def channel(self) -> RhoTypes_pb2___Par: ...

    @property
    def data(self) -> RhoTypes_pb2___ListParWithRandom: ...

    def __init__(self,
        *,
        channel : typing___Optional[RhoTypes_pb2___Par] = None,
        data : typing___Optional[RhoTypes_pb2___ListParWithRandom] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ReportProduceProto: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ReportProduceProto: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"channel",b"channel",u"data",b"data"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"channel",b"channel",u"data",b"data"]) -> None: ...

class ReportConsumeProto(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def channels(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[RhoTypes_pb2___Par]: ...

    @property
    def patterns(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[RhoTypes_pb2___BindPattern]: ...

    @property
    def peeks(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[CasperMessage_pb2___PeekProto]: ...

    def __init__(self,
        *,
        channels : typing___Optional[typing___Iterable[RhoTypes_pb2___Par]] = None,
        patterns : typing___Optional[typing___Iterable[RhoTypes_pb2___BindPattern]] = None,
        peeks : typing___Optional[typing___Iterable[CasperMessage_pb2___PeekProto]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ReportConsumeProto: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ReportConsumeProto: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"channels",b"channels",u"patterns",b"patterns",u"peeks",b"peeks"]) -> None: ...

class ReportCommProto(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def consume(self) -> ReportConsumeProto: ...

    @property
    def produces(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ReportProduceProto]: ...

    def __init__(self,
        *,
        consume : typing___Optional[ReportConsumeProto] = None,
        produces : typing___Optional[typing___Iterable[ReportProduceProto]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ReportCommProto: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ReportCommProto: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"consume",b"consume"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"consume",b"consume",u"produces",b"produces"]) -> None: ...

class ReportProto(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def produce(self) -> ReportProduceProto: ...

    @property
    def consume(self) -> ReportConsumeProto: ...

    @property
    def comm(self) -> ReportCommProto: ...

    def __init__(self,
        *,
        produce : typing___Optional[ReportProduceProto] = None,
        consume : typing___Optional[ReportConsumeProto] = None,
        comm : typing___Optional[ReportCommProto] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> ReportProto: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> ReportProto: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"comm",b"comm",u"consume",b"consume",u"produce",b"produce",u"report",b"report"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"comm",b"comm",u"consume",b"consume",u"produce",b"produce",u"report",b"report"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"report",b"report"]) -> typing_extensions___Literal["produce","consume","comm"]: ...

class SingleReport(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def events(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[ReportProto]: ...

    def __init__(self,
        *,
        events : typing___Optional[typing___Iterable[ReportProto]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SingleReport: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SingleReport: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"events",b"events"]) -> None: ...

class DeployInfoWithEventData(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def deployInfo(self) -> DeployInfo: ...

    @property
    def report(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[SingleReport]: ...

    def __init__(self,
        *,
        deployInfo : typing___Optional[DeployInfo] = None,
        report : typing___Optional[typing___Iterable[SingleReport]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> DeployInfoWithEventData: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> DeployInfoWithEventData: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"deployInfo",b"deployInfo"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"deployInfo",b"deployInfo",u"report",b"report"]) -> None: ...

class BlockEventInfo(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def blockInfo(self) -> LightBlockInfo: ...

    @property
    def deploys(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[DeployInfoWithEventData]: ...

    def __init__(self,
        *,
        blockInfo : typing___Optional[LightBlockInfo] = None,
        deploys : typing___Optional[typing___Iterable[DeployInfoWithEventData]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> BlockEventInfo: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> BlockEventInfo: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"blockInfo",b"blockInfo"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"blockInfo",b"blockInfo",u"deploys",b"deploys"]) -> None: ...
