import logging

import staketaxcsv.arch
import staketaxcsv.arch.constants as co
import staketaxcsv.common.ibc.handle
import staketaxcsv.common.ibc.processor
from staketaxcsv.arch.config_arch import localconfig
from staketaxcsv.settings_csv import ARCH_NODE
from staketaxcsv.arch import util_arch
import staketaxcsv.arch.contracts.dao_dao_multisig
import staketaxcsv.arch.handle_unknown

CONTRACT_DAO_DAO_MULTI_SIG = "archway19erqhx6pu6tea3k7szaqg08nv2xhrmp7aqu7j9jm54v54qcunt0q5jqtu2"


def process_txs(wallet_address, elems, exporter):
    for elem in elems:
        process_tx(wallet_address, elem, exporter)


def process_tx(wallet_address, elem, exporter):
    txinfo = staketaxcsv.common.ibc.processor.txinfo(
        wallet_address, elem, co.MINTSCAN_LABEL_ARCH, ARCH_NODE)
    txinfo.url = "https://www.mintscan.io/archway/tx/{}".format(txinfo.txid)

    if txinfo.is_failed:
        staketaxcsv.common.ibc.processor.handle_failed_transaction(exporter, txinfo)
        return txinfo

    for msginfo in txinfo.msgs:
        result = staketaxcsv.common.ibc.processor.handle_message(exporter, txinfo, msginfo, localconfig.debug)
        if result:
            continue

        _handle_message(exporter, txinfo, msginfo)

    return txinfo

def _handle_message(exporter, txinfo, msginfo):
    try:
        msg_type = util_arch._msg_type(msginfo)

        # execute contract
        if msg_type == co.MSG_TYPE_EXECUTE_CONTRACT:
            _handle_execute_contract(exporter, txinfo, msginfo)
        else:
            staketaxcsv.arch.handle_unknown.handle_unknown_detect_transfers(exporter, txinfo, msginfo)
    except Exception as e:
        logging.error(
            "Exception when handling txid=%s, exception=%s", txinfo.txid, str(e))
        staketaxcsv.arch.handle_unknown.handle_unknown_detect_transfers(exporter, txinfo, msginfo)

        if localconfig.debug:
            raise e

    return txinfo


def _handle_execute_contract(exporter, txinfo, msginfo):
    contract = msginfo.contract

    dao_dao_address = msginfo.wasm[0]["dao"]
    #logging.info("dao_dao_address: %s", dao_dao_address)
    if dao_dao_address == CONTRACT_DAO_DAO_MULTI_SIG:
        #txinfo.print()
        staketaxcsv.arch.contracts.dao_dao_multisig.handle(exporter, txinfo, msginfo)
    else:
        staketaxcsv.arch.handle_unknown.handle_unknown_detect_transfers(exporter, txinfo, msginfo)
