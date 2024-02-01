import argparse
from dotenv import load_dotenv
import os
import sys
from prompt_selection import run_prompt_selection
from openai import OpenAI

sys.path.append('./src')
load_dotenv()
client = OpenAI()

parser = argparse.ArgumentParser()
parser.add_argument(
        "--test_prompts", action="store_true",
        help="Run the test prompt selection.")
args = parser.parse_args()

if args.test_prompts:
    prompts_dir = os.getenv('TEST_PROMPTS_DIR', './data/tests/prompts/')
    results_dir = os.getenv('TEST_RESULTS_DIR', './data/tests/results/')
    run_prompt_selection(prompts_dir, results_dir, client)
