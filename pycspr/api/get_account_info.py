import typing

from pycspr.api import constants
from pycspr.api.utils import get_block_id_param
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    account_key: typing.Union[bytes, str],
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns on-chain account information at a certain state root hash.

    :param node: Information required to connect to a node.
    :param account_key: An account holder's public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: Account information in JSON format.

    """    
    params = get_params(account_key, block_id)
    response = node.get_response(constants.RPC_STATE_GET_ACCOUNT_INFO, params)

    return response["account"]


def get_params(
    account_key: typing.Union[bytes, str],
    block_id: typing.Union[None, str, int] = None
    ) -> dict:
    """Returns JSON-RPC API request parameters.

    :param account_key: An account holder's public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    account_key = account_key.hex() if isinstance(account_key, bytes) else account_key
    param = {"public_key": account_key}
    param.update(get_block_id_param(block_id))
    return param
