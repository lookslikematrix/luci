from assertpy import assert_that
from click.testing import CliRunner

from src.luanti_cli.__main__ import cli

RUNNER = CliRunner()


def test_help():
    # arrange

    # act
    response = RUNNER.invoke(cli=cli, args=["--help"])

    # assert
    assert_that(response.output).is_equal_to(
        "Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n"
        "  📦️ LuCI - Luanti Commandline Interface 📦️\n\n"
        "  Read here for further information:\n\n"
        "      https://github.com/lookslikematrix/luci\n\n"
        "  If you've any issues report them here:\n\n"
        "      https://github.com/lookslikematrix/luci/issues/new\n\n"
        "Options:\n"
        "  --loglevel TEXT  Set loglevel (default: WARNING)\n"
        "  --help           Show this message and exit.\n\n"
        "Commands:\n"
        "  blocks  Get all block types from current Luanti game.\n"
        "  build   Build a STL file into Luanti.\n"
        "  erase   Erase a STL file from Luanti.\n"
        "  info    Get info.\n"
    )
