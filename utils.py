"""General utility functions that are re-used in different scripts."""

import click
from mne.utils import logger

from tqdm import tqdm
from joblib import Parallel

class ProgressParallel(Parallel):
    def __init__(self, use_tqdm=True, total=None, *args, **kwargs):
        self._use_tqdm = use_tqdm
        self._total = total
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        with tqdm(disable=not self._use_tqdm, total=self._total) as self._pbar:
            return Parallel.__call__(self, *args, **kwargs)

    def print_progress(self):
        if self._total is None:
            self._pbar.total = self.n_dispatched_tasks
        self._pbar.n = self.n_completed_tasks
        self._pbar.refresh()


@click.command()
@click.option("--subj",
              type=int,
              help="Subject number")
@click.option("--session",
              type=int,
              help="Session number")
@click.option("--task",
              type=str,
              default='oddeven',
              help="Session number")
@click.option("--overwrite",
              default=False,
              type=bool,
              help="Overwrite?")
@click.option("--interactive",
              default=False,
              type=bool,
              help="Interactive?")
@click.option("--report",
              default=False,
              type=bool,
              help="Generate HTML-report?")
@click.option("--jobs",
              default=1,
              type=int,
              help="The number of hobs to run in parallel")
def get_inputs(
        subj,
        session,
        task,
        overwrite,
        interactive,
        report,
        jobs
):
    """Parse inputs in case script is run from command line.
    See Also
    --------
    parse_overwrite
    """
    # collect all in dict
    inputs = dict(
        sub=subj,
        session=session,
        task=task,
        overwrite=overwrite,
        interactive=interactive,
        report=report,
        jobs=jobs
    )

    return inputs


def parse_overwrite(defaults):
    """Parse which variables to overwrite."""
    logger.info("\nParsing command line options...\n")

    # invoke `get_inputs()` as command line application
    inputs = get_inputs.main(standalone_mode=False, default_map=defaults)

    # check if any defaults should be overwritten
    overwrote = 0
    for key, val in defaults.items():
        if val != inputs[key]:
            logger.info(f"    > Overwriting default '{key}': {val} -> {inputs[key]}")  # noqa
            defaults[key] = inputs[key]
            overwrote += 1
