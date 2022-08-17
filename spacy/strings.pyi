from typing import Optional, Iterable, Iterator, Union, Any, Tuple
from pathlib import Path

class StringStore:
    def __init__(self, strings: Optional[Iterable[str]]) -> None: ...
    def __getitem__(self, string_or_hash: Union[str, int]) -> Union[str, int]: ...
    def as_int(self, key: Union[str, int]) -> int: ...
    def as_string(self, string_or_hash: Union[str, int]) -> str: ...
    def add(self, string: str) -> int: ...
    def items(self) -> Tuple[int, str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, string_or_hash: Union[str, int]) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __reduce__(self) -> Any: ...
    def to_disk(self, path: Union[str, Path]) -> None: ...
    def from_disk(self, path: Union[str, Path]) -> StringStore: ...
    def to_bytes(self, **kwargs: Any) -> bytes: ...
    def from_bytes(self, bytes_data: bytes, **kwargs: Any) -> StringStore: ...
    def _reset_and_load(self, strings: Iterable[str]) -> None: ...
