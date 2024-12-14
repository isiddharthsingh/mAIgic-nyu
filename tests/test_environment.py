import os
from dotenv import load_dotenv
import pytest

# Load environment variables from .env file
load_dotenv()

# List of required environment variables
REQUIRED_ENV_VARS = ["SLACK_APP_TOKEN", "SLACK_BOT_TOKEN"]

def test_env_file_exists():
    """Test that the .env file exists."""
    assert os.path.exists(".env"), "The .env file is missing."
    
@pytest.mark.parametrize("env_var", REQUIRED_ENV_VARS)
def test_env_var_exist(env_var):
    value = os.getenv(env_var)
    assert value, f'Missing definition of environment variable \'{env_var}\''
    