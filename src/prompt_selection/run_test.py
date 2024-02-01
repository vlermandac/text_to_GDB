from .blind_test import run_blind_test
from .test_prompts import get_results


def run_prompt_selection(prompts_dir, results_dir, client):
    get_results(prompts_dir, results_dir, client)
    run_blind_test(results_dir)
