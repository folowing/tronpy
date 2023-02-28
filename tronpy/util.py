import time

from .keys import sha256
from .smart_contract_pb2 import (
    TriggerSmartContract,
    Contract,
    TransactionRawData,
)


def get_ttl_hash(seconds=3600):
    """Return the same value withing `seconds` time period"""
    return round(time.time() / seconds)


def get_transaction_id(txn):
    tx_obj = txn._raw_data
    contract_obj = tx_obj['contract'][0]['parameter']['value']
    smart_contract = TriggerSmartContract()
    smart_contract.owner_address = bytes.fromhex(contract_obj['owner_address'])
    smart_contract.contract_address = bytes.fromhex(contract_obj['contract_address'])
    smart_contract.call_value = contract_obj['call_value']
    smart_contract.data = bytes.fromhex(contract_obj['data'])
    smart_contract.call_token_value = contract_obj['call_token_value']
    smart_contract.token_id = contract_obj['token_id']

    contract = Contract()
    contract.type = Contract.ContractType.TriggerSmartContract
    contract.parameter.Pack(smart_contract)

    raw_data = TransactionRawData()
    raw_data.ref_block_bytes = bytes.fromhex(tx_obj['ref_block_bytes'])
    raw_data.ref_block_hash = bytes.fromhex(tx_obj['ref_block_hash'])
    raw_data.expiration = tx_obj['expiration']
    raw_data.timestamp = tx_obj['timestamp']
    raw_data.fee_limit = tx_obj['fee_limit']
    raw_data.contract.extend([contract])

    raw_data_bytes = raw_data.SerializeToString()
    return sha256(raw_data_bytes).hex()
