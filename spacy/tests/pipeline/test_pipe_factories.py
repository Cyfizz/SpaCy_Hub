import pytest
from spacy.language import Language
from spacy.tokens import Doc
from spacy.util import registry
from thinc.api import Model, Linear
from thinc.config import ConfigValidationError
from pydantic import StrictInt, StrictStr


def test_pipe_function_component():
    name = "test_component"

    @Language.component(name)
    def component(doc: Doc) -> Doc:
        return doc

    factory_name = Language.get_factory_name(name)
    assert factory_name in registry.factories
    nlp = Language()
    with pytest.raises(ValueError):
        nlp.add_pipe(component)
    nlp.add_pipe(name)
    assert name in nlp.pipe_names
    assert nlp.pipe_factories[name] == name
    assert Language.factory_meta[factory_name]
    pipe = nlp.get_pipe(name)
    assert pipe == component
    pipe = nlp.create_pipe(name)
    assert pipe == component


def test_pipe_class_component_init():
    name1 = "test_class_component1"
    name2 = "test_class_component2"

    @Language.factory(name1)
    class Component1:
        def __init__(self, nlp: Language, name: str):
            self.nlp = nlp

        def __call__(self, doc: Doc) -> Doc:
            return doc

    class Component2:
        def __init__(self, nlp: Language, name: str):
            self.nlp = nlp

        def __call__(self, doc: Doc) -> Doc:
            return doc

    @Language.factory(name2)
    def factory(nlp: Language, name=name2):
        return Component2(nlp, name)

    nlp = Language()
    for name, Component in [(name1, Component1), (name2, Component2)]:
        factory_name = Language.get_factory_name(name)
        assert factory_name in registry.factories
        with pytest.raises(ValueError):
            nlp.add_pipe(Component(nlp, name))
        nlp.add_pipe(name)
        assert name in nlp.pipe_names
        assert nlp.pipe_factories[name] == name
        assert Language.factory_meta[factory_name]
        pipe = nlp.get_pipe(name)
        assert isinstance(pipe, Component)
        assert isinstance(pipe.nlp, Language)
        pipe = nlp.create_pipe(name)
        assert isinstance(pipe, Component)
        assert isinstance(pipe.nlp, Language)


def test_pipe_class_component_config():
    name = "test_class_component_config"

    @Language.factory(name)
    class Component:
        def __init__(
            self, nlp: Language, name: str, value1: StrictInt, value2: StrictStr
        ):
            self.nlp = nlp
            self.value1 = value1
            self.value2 = value2

        def __call__(self, doc: Doc) -> Doc:
            return doc

    nlp = Language()
    with pytest.raises(ConfigValidationError):  # no config provided
        nlp.add_pipe(name)
    with pytest.raises(ConfigValidationError):  # invalid config
        nlp.add_pipe(name, config={"value1": "10", "value2": "hello"})
    nlp.add_pipe(name, config={"value1": 10, "value2": "hello"})
    pipe = nlp.get_pipe(name)
    assert isinstance(pipe.nlp, Language)
    assert pipe.value1 == 10
    assert pipe.value2 == "hello"


def test_pipe_class_component_defaults():
    name = "test_class_component_defaults"

    @Language.factory(name)
    class Component:
        def __init__(
            self,
            nlp: Language,
            name: str,
            value1: StrictInt = 10,
            value2: StrictStr = "hello",
        ):
            self.nlp = nlp
            self.value1 = value1
            self.value2 = value2

        def __call__(self, doc: Doc) -> Doc:
            return doc

    nlp = Language()
    nlp.add_pipe(name)
    pipe = nlp.get_pipe(name)
    assert isinstance(pipe.nlp, Language)
    assert pipe.value1 == 10
    assert pipe.value2 == "hello"


def test_pipe_class_component_model():
    name = "test_class_component_model"
    default_config = {
        "model": {
            "@architectures": "spacy.TextCat.v1",
            "exclusive_classes": False,
            "pretrained_vectors": None,
            "width": 64,
            "embed_size": 2000,
            "window_size": 1,
            "conv_depth": 2,
            "ngram_size": 1,
            "dropout": None,
        },
        "value1": 10,
    }

    @Language.factory(name, default_config=default_config)
    class Component:
        def __init__(self, nlp: Language, model: Model, name: str, value1: StrictInt):
            self.nlp = nlp
            self.model = model
            self.value1 = value1
            self.name = name

        def __call__(self, doc: Doc) -> Doc:
            return doc

    nlp = Language()
    nlp.add_pipe(name)
    pipe = nlp.get_pipe(name)
    assert isinstance(pipe.nlp, Language)
    assert pipe.value1 == 10
    assert isinstance(pipe.model, Model)


def test_pipe_class_component_model_custom():
    name = "test_class_component_model_custom"
    arch = f"{name}.arch"
    default_config = {"value1": 1, "model": {"@architectures": arch, "nO": 0, "nI": 0}}

    @Language.factory(name, default_config=default_config)
    class Component:
        def __init__(
            self, nlp: Language, model: Model, name: str, value1: StrictInt = 10
        ):
            self.nlp = nlp
            self.model = model
            self.value1 = value1
            self.name = name

        def __call__(self, doc: Doc) -> Doc:
            return doc

    @registry.architectures(arch)
    def make_custom_arch(nO: StrictInt, nI: StrictInt):
        return Linear(nO, nI)

    nlp = Language()
    config = {"value1": 20, "model": {"@architectures": arch, "nO": 1, "nI": 2}}
    nlp.add_pipe(name, config=config)
    pipe = nlp.get_pipe(name)
    assert isinstance(pipe.nlp, Language)
    assert pipe.value1 == 20
    assert isinstance(pipe.model, Model)
    assert pipe.model.name == "linear"

    nlp = Language()
    with pytest.raises(ConfigValidationError):
        config = {"value1": "20", "model": {"@architectures": arch, "nO": 1, "nI": 2}}
        nlp.add_pipe(name, config=config)
    with pytest.raises(ConfigValidationError):
        config = {"value1": 20, "model": {"@architectures": arch}}
        nlp.add_pipe(name, config=config)
    with pytest.raises(ConfigValidationError):
        config = {"value1": 20, "model": {"@architectures": arch, "nO": 1.0, "nI": 2.0}}
        nlp.add_pipe(name, config=config)
