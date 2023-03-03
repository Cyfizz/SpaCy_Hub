import abc
from typing import List, Union, Callable


class Candidate(abc.ABC):
    """A `Candidate` object refers to a textual mention that may or may not be resolved
    to a specific `entity_id` from a Knowledge Base. This will be used as input for the entity_id linking
    algorithm which will disambiguate the various candidates to the correct one.
    Each candidate (mention, entity_id) pair is assigned a certain prior probability.

    DOCS: https://spacy.io/api/kb/#candidate-init
    """

    def __init__(
        self,
        mention: str,
        entity_id: int,
        entity_name: str,
        entity_vector: List[float],
        prior_prob: float,
    ):
        """Initializes properties of `Candidate` instance.
        mention (str): Mention text for this candidate.
        entity_id (int): Unique entity ID.
        entity_name (str): Entity name.
        entity_vector (List[float]): Entity embedding.
        prior_prob (float): Prior probability of entity for this mention - i.e. the probability that, independent of
            the context, this mention resolves to this entity_id in the corpus used to build the knowledge base. In
            cases in which this isn't always possible (e.g.: the corpus to analyse contains mentions that the KB corpus
            doesn't) it might be better to eschew this information and always supply the same value.
        """
        self._mention_ = mention
        self._entity = entity_id
        self._entity_ = entity_name
        self._entity_vector = entity_vector
        self._prior_prob = prior_prob

    @property
    def entity(self) -> int:
        """RETURNS (int): Unique entity ID."""
        return self._entity

    @property
    def entity_(self) -> str:
        """RETURNS (int): Entity name."""
        return self._entity_

    @property
    def mention_(self) -> str:
        """RETURNS (str): Mention."""
        return self._mention_

    @property
    def entity_vector(self) -> List[float]:
        """RETURNS (List[float]): Entity vector."""
        return self._entity_vector

    @property
    def prior_prob(self) -> float:
        """RETURNS (List[float]): Entity vector."""
        return self._prior_prob


class InMemoryCandidate(Candidate):
    """Candidate for InMemoryLookupKB."""

    def __init__(
        self,
        retrieve_string_from_hash: Callable[[int], str],
        entity_hash: int,
        entity_freq: int,
        entity_vector: List[float],
        mention_hash: int,
        prior_prob: float,
    ):
        """
        retrieve_string_from_hash (Callable[[int], str]): Callable retrieving entity name from provided entity/vocab
            hash.
        entity_hash (str): Hashed entity name /ID.
        entity_freq (int): Entity frequency in KB corpus.
        entity_vector (List[float]): Entity embedding.
        mention_hash (int): Hashed mention.
        prior_prob (float): Prior probability of entity for this mention - i.e. the probability that, independent of
            the context, this mention resolves to this entity_id in the corpus used to build the knowledge base. In
            cases in which this isn't always possible (e.g.: the corpus to analyse contains mentions that the KB corpus
            doesn't) it might be better to eschew this information and always supply the same value.
        """
        super().__init__(
            mention=retrieve_string_from_hash(mention_hash),
            entity_id=entity_hash,
            entity_name=retrieve_string_from_hash(entity_hash),
            entity_vector=entity_vector,
            prior_prob=prior_prob,
        )
        self._retrieve_string_from_hash = retrieve_string_from_hash
        self._entity = entity_hash
        self._entity_freq = entity_freq
        self._mention = mention_hash
        self._prior_prob = prior_prob

    @property
    def entity(self) -> int:
        """RETURNS (int): hash of the entity_id's KB ID/name"""
        return self._entity

    @property
    def mention(self) -> int:
        """RETURNS (int): Mention hash."""
        return self._mention

    @property
    def entity_freq(self) -> float:
        """RETURNS (float): Relative entity frequency."""
        return self._entity_freq
