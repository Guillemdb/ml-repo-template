"""Command line interface for mloq."""
import os

import click


override_opt = click.option(
    "--override/--no-override",
    "-o/ ",
    default=False,
    show_default=True,
    help="If True overwrite existing files. If False ignore files that already exist.",
)
config_file_opt = click.option(
    "--filename",
    "-f",
    "config_file",
    default=None,
    show_default=True,
    help="Name of the repository config file",
    type=click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True),
)


output_path_arg = click.argument(
    "output", type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True)
)

interactive_opt = click.option(
    "--interactive/--no-interactive",
    "-i/ ",
    default=False,
    show_default=True,
    help="If True the configuration values will be defined interactively on the command line.",
)


def _parse_env(config_file, override, interactive):
    """Parse environment variables defining command options."""
    config_file = os.getenv("MLOQ_CONFIG_FILE", config_file)
    override = os.getenv("MLOQ_OVERRIDE", override)
    interactive = os.getenv("MLOQ_INTERACTIVE", interactive)
    return config_file, override, interactive


@click.group()
def cli():
    """Command line interface for ML Ops Quickstart."""
    pass


@cli.command()
@override_opt
@interactive_opt
@config_file_opt
@output_path_arg
def setup(config_file, output, override: bool, interactive: bool):
    from mloq.cli.setup_cmd import setup_cmd

    config_file, override, interactive = _parse_env(config_file, override, interactive)
    setup_cmd(config_file, output, override, interactive)
