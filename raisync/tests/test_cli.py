import json
import pathlib
import signal

import eth_account
import pytest
from click.testing import CliRunner
from raisync.cli import main

from raisync.util import TokenMatchChecker


def test_cli(config, tmp_path):
    key = "0x3ff6c8dfd3ab60a14f2a2d4650387f71fe736b519d990073e650092faaa621fa"
    acc = eth_account.Account.from_key(key)
    obj = eth_account.account.create_keyfile_json(acc.key, b"")
    keyfile = tmp_path / f"{acc.address}.json"
    keyfile.write_text(json.dumps(obj))
    root = pathlib.Path(__file__).parents[2]
    contracts_deployment_dir = str(root / "contracts/build/deployments/dev")

    signal.signal(signal.SIGALRM, lambda *_unused: signal.raise_signal(signal.SIGINT))
    signal.setitimer(signal.ITIMER_REAL, 2)

    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "--keystore-file",
            str(keyfile),
            "--password",
            "",
            "--l2a-rpc-url",
            config.l2a_rpc_url,
            "--l2b-rpc-url",
            config.l2b_rpc_url,
            "--l2a-contracts-deployment-dir",
            contracts_deployment_dir,
            "--l2b-contracts-deployment-dir",
            contracts_deployment_dir,
            "--token-match-file",
            str(root / "raisync/data/tokens.example.json"),
        ],
    )
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "token_chain_ids_validity",
    [(["28", "588"], True), (["10", "42161", "288"], True), (["10", "28", "588"], False)],
)
def test_token_lists_validity(token_chain_ids_validity):
    token_address = "0x0000000000000000000000000000000000000001"
    token_chain_ids, valid = token_chain_ids_validity
    tokens = [
        # Parametrized token map
        [[chain_id, token_address] for chain_id in token_chain_ids],
        # Valid token map
        [
            ["28", "0x2De6a0f9dDFCb338AF1a126Dc77af9a245bBc83d"],
            ["588", "0xD184D3515e1817DDE870a2F30DEC29a8f1192414"],
        ],
    ]

    if not valid:
        with pytest.raises(AssertionError):
            TokenMatchChecker(tokens)
    else:
        TokenMatchChecker(tokens)
