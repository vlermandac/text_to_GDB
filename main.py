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

prompt = "PROMPT_FILE"

if args.test_prompts:
    if prompt in os.environ:
        raise EnvironmentError(f'''The environment variable '{prompt}'
                               is already set. Remove it to run a new
                               prompt selection.''')

    prompts_dir = os.getenv('TEST_PROMPTS_DIR', './data/tests/prompts/')
    results_dir = os.getenv('TEST_RESULTS_DIR', './data/tests/results/')
    run_prompt_selection(prompts_dir, results_dir, client)
    exit(0)

prompt = os.getenv('PROMPT_FILE', './selected_prompt.txt')
