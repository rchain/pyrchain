import logging
import time

import pytest
import typing_extensions
from rchain.client import RClient, RClientException


class PredicateProtocol(typing_extensions.Protocol):
    def __str__(self) -> str:
        # pylint: disable=pointless-statement
        ...

    def is_satisfied(self) -> bool:
        # pylint: disable=pointless-statement, no-self-use
        ...


class WaitTimeoutError(Exception):
    def __init__(self, predicate: 'PredicateProtocol', timeout: int) -> None:
        super().__init__()
        self.predicate = predicate
        self.timeout = timeout


def wait_using_wall_clock_time(predicate: PredicateProtocol, timeout: int) -> None:
    logging.info("AWAITING {}".format(predicate))

    elapsed = 0
    while elapsed < timeout:
        start_time = time.time()

        is_satisfied = predicate.is_satisfied()
        if is_satisfied:
            logging.info("SATISFIED {}".format(predicate))
            return

        condition_evaluation_duration = time.time() - start_time
        elapsed = int(elapsed + condition_evaluation_duration)
        time_left = timeout - elapsed

        # iteration duration is 15% of remaining timeout
        # but no more than 10s and no less than 1s
        iteration_duration = int(min(10, max(1, int(0.15 * time_left))))

        time.sleep(iteration_duration)
        elapsed = elapsed + iteration_duration
    logging.info("TIMEOUT %s", predicate)
    raise WaitTimeoutError(predicate, timeout)


def wait_using_wall_clock_time_or_fail(predicate: PredicateProtocol, timeout: int) ->None:
    try:
        wait_using_wall_clock_time(predicate, timeout)
    except WaitTimeoutError:
        pytest.fail('Failed to satisfy {} after {}s'.format(predicate, timeout))

class BlockSee(PredicateProtocol):
    def __init__(self, client: RClient, block_hash:str):
        self.client = client
        self.block_hash = block_hash

    def __str__(self) -> str:
        args = ', '.join(repr(a) for a in (self.node.name, self.block_hash))
        return '<{}({})>'.format(self.__class__.__name__, args)

    def is_satisfied(self) -> bool:
        try:
            self.client.show_block(self.block_hash)
            return True
        except RClientException:
            return False