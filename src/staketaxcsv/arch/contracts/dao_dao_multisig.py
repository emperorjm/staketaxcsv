from staketaxcsv.arch.make_tx import make_arch_unknown_tx, make_arch_dao_doa_multisig_tx_with_transfer
from staketaxcsv.arch import util_arch
import logging


def handle(exporter, txinfo, msginfo):
    transfers_in, transfers_out = msginfo.transfers
    transfers_net_in, transfers_net_out = msginfo.transfers_net

    if len(transfers_in) == 0 and len(transfers_out) == 0:
        handle_unknown(exporter, txinfo, msginfo)
        return
    elif len(transfers_in) == 1 and len(transfers_out) == 1:
        # Present unknown transaction as one line (for this special case).
        sent_amount, sent_currency = transfers_out[0]
        received_amount, received_currency = transfers_in[0]

        row = make_arch_dao_doa_multisig_tx_with_transfer(
            txinfo, msginfo, sent_amount, sent_currency, received_amount, received_currency)
        
        exporter.ingest_row(row)
    else:
        # Handle unknown transaction as separate transfers for each row.
        rows = []
        for sent_amount, sent_currency in transfers_net_out:
            rows.append(
                make_arch_dao_doa_multisig_tx_with_transfer(txinfo, msginfo, sent_amount, sent_currency, "", ""))
        for received_amount, received_currency in transfers_net_in:
            rows.append(
                make_arch_dao_doa_multisig_tx_with_transfer(txinfo, msginfo, "", "", received_amount, received_currency))
        util_arch._ingest_dao_dao_rows(exporter, rows)

def handle_unknown(exporter, txinfo, msginfo):
    row = make_arch_unknown_tx(txinfo, msginfo)
    
    exporter.ingest_row(row)
