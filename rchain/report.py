from dataclasses import dataclass
from typing import List, Optional, Tuple

from .pb.DeployServiceCommon_pb2 import DeployInfo, SingleReport
from .pb.RhoTypes_pb2 import Par, ParWithRandom


@dataclass
class Report:
    precharge: SingleReport
    user: SingleReport
    refund: SingleReport

@dataclass
class Transaction:
    from_addr: str
    to_addr: str
    amount: int
    ret_unforgeable: Par
    success: Optional[Tuple[bool, str]]

@dataclass
class DeployWithTransaction:
    deploy_info: DeployInfo
    transactions: List[Transaction]
