from staketaxcsv.common.Exporter import Row
from staketaxcsv.common.make_tx import (
    _make_tx_exchange,
    make_reward_tx,
    make_unknown_tx,
    make_unknown_tx_with_transfer,
)
from staketaxcsv.arch import util_arch
import logging


def _edit_row(row, txinfo, msginfo):
    row.txid = txinfo.txid + "-" + str(msginfo.msg_index)
    if msginfo.msg_index > 0:
        row.fee = ""
        row.fee_currency = ""


def make_arch_tx(txinfo, msginfo, sent_amount, sent_currency, received_amount, received_currency,
                 txid=None, empty_fee=False):
    tx_type = util_arch._make_tx_type(msginfo)
    row = _make_tx_exchange(
        txinfo, sent_amount, sent_currency, received_amount, received_currency, tx_type,
        txid=txid, empty_fee=empty_fee)
    _edit_row(row, txinfo, msginfo)
    return row

def make_arch_reward_tx(txinfo, msginfo, reward_amount, reward_currency):
    row = make_reward_tx(txinfo, reward_amount, reward_currency)
    _edit_row(row, txinfo, msginfo)
    return row

def make_arch_unknown_tx(txinfo, msginfo):
    row = make_unknown_tx(txinfo)
    _edit_row(row, txinfo, msginfo)
    return row

def make_arch_unknown_tx_with_transfer(txinfo, msginfo, sent_amount, sent_currency, received_amount,
                                       received_currency, empty_fee=False, z_index=0):
    row = make_unknown_tx_with_transfer(
        txinfo, sent_amount, sent_currency, received_amount, received_currency, empty_fee, z_index)
    _edit_row(row, txinfo, msginfo)
    return row

def make_arch_dao_doa_multisig_tx_with_transfer(txinfo, msginfo, sent_amount, sent_currency, received_amount,
                                       received_currency, empty_fee=False, z_index=0):
    row = make_unknown_tx_with_transfer(
        txinfo, sent_amount, sent_currency, received_amount, received_currency, empty_fee, z_index)
    
    row.tx_type = "_DAO_DAO_Multisig_Proposal"
    
    proposal_id = msginfo.message["msg"]["execute"].get("proposal_id")
    if proposal_id:
        row.comment = f"Proposal ID: {proposal_id}"

    _edit_row(row, txinfo, msginfo)
    return row
