
from tracemate.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    def generate(self, prompt: str, system_instruction: str | None = None) -> str:
        return "Gemini response"


class IncompleteProvider(LLMProvider):
    pass


provider = GeminiProvider()
assert provider.generate("Explain linked lists") == "Gemini response"

try:
    IncompleteProvider()
except TypeError:
    print("Abstract class enforcement: PASSED")
else:
    raise AssertionError("Incomplete provider should not be instantiable.")

print("Concrete provider implementation: PASSED")
