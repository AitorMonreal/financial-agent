import sys
from unittest.mock import MagicMock

# Mock pydantic_ai to avoid dependency hell during unit testing 
# since we are only testing the deterministic Python logic.
class MockAgent:
    def __init__(self, model, result_type=None, system_prompt=None, **kwargs):
        self.model = model
        self.result_type = result_type
        self.system_prompt = system_prompt

    def run_sync(self, prompt, *args, **kwargs):
        mock_result = MagicMock()
        mock_result.data = None
        return mock_result

mock_pydantic_ai = MagicMock()
mock_pydantic_ai.Agent = MockAgent

sys.modules['pydantic_ai'] = mock_pydantic_ai
