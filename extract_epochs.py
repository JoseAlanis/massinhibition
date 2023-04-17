"""
==============
Extract epochs
==============

Extracts relevant epochs for the conditions in question.

Authors: José C. García Alanis <alanis.jcg@gmail.com>

License: BSD (3-clause)
"""

# %%
# imports
import sys
import os

from utils import parse_overwrite

# %%
# default settings (use subject 1, don't overwrite output files)
subj = 1
session = 1
task = 'oddeven'
overwrite = False
report = False
jobs = 1

# %%
# When not in an IPython session, get command line inputs
# https://docs.python.org/3/library/sys.html#sys.ps1
if not hasattr(sys, "ps1"):
    defaults = dict(
        sub=subj,
        session=session,
        task=task,
        overwrite=overwrite,
        report=report,
        jobs=jobs
    )

    defaults = parse_overwrite(defaults)

    subj = defaults["sub"]
    session = defaults["session"]
    task = defaults["task"]
    overwrite = defaults["overwrite"]
    report = defaults["report"]
    jobs = defaults["jobs"]


# %%
# paths and overwrite settings
if subj not in SUBJECT_IDS:
    raise ValueError(f"'{subj}' is not a valid subject ID.\nUse: {SUBJECT_IDS}")

# skip bad subjects
if session == 1 and subj in BAD_SUBJECTS_SES_01:
    sys.exit()
if session == 2 and subj in BAD_SUBJECTS_SES_02:
    sys.exit()

if not os.path.exists(FPATH_DATA_BIDS):
    raise RuntimeError(
        FPATH_BIDS_NOT_FOUND_MSG.format(FPATH_DATA_BIDS)
    )

# create path for preprocessed data
subj_str = str(subj).rjust(3, '0')
FPATH_PREPROCESSED = os.path.join(FPATH_DATA_DERIVATIVES,
                                  'preprocessing',
                                  'sub-%s' % subj_str)

if not Path(FPATH_PREPROCESSED).exists():
    Path(FPATH_PREPROCESSED).mkdir(parents=True, exist_ok=True)

if overwrite:
    logger.info("`overwrite` is set to ``True`` ")

# %%
#  create path for import

# subject file id
str_subj = str(subj).rjust(3, '0')

FPATH_PREPROCESSED = os.path.join(FPATH_PREPROCESSED,
                                  'eeg',
                                  'sub-%s_task-%s_preprocessed-raw.fif' % (
                                      str_subj, task))

if not os.path.exists(FPATH_PREPROCESSED):
    warnings.warn(FPATH_BIDSDATA_NOT_FOUND_MSG.format(FPATH_PREPROCESSED))
    sys.exit()

# %%
# get the data
raw = read_raw_fif(FPATH_PREPROCESSED)
raw.load_data()