import pytest

from tracemate.providers.base import LLMProvider


class ConcreteProvider(LLMProvider):
    def generate(self, prompt: str, system_instruction: str | None = None) -> str:
        return "Test response"


class IncompleteProvider(LLMProvider):
    pass


def test_concrete_provider():
    provider = ConcreteProvider()
    assert provider.generate("Test") == "Test response"


def test_abstract_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        IncompleteProvider()