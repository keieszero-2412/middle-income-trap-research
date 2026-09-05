"""Run the reduced five-variable Cox PH branch."""
from cox_model import run_branch


REDUCED_COVARIATES = ['TFP', 'GE', 'AGEDEP', 'TO', 'CREDIT']


if __name__ == '__main__':
    run_branch(REDUCED_COVARIATES, output_suffix='_5vars', branch_name='5-vars')