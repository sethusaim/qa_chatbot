from dataclasses import dataclass, field
from typing import Dict


@dataclass
class DataIngestionConfig:
    char_splitter_args: Dict[str, int] = field(
        default_factory=lambda: ({"chunk_size": 1024, "chunk_overlap": 128})
    )

    data_folder: str = "hfcrawl/output/"

    persist_directory: str = "db"

    data_loader_kwargs: Dict[str, str] = field(
        default_factory=lambda: ({"encoding": ":utf-8"})
    )

    return_source_documents: bool = True


@dataclass
class ChainConfig:
    chain_type: str = "stuff"

    verbose: bool = True


@dataclass
class MemoryConfig:
    memory_key: str = "chat_history"

    return_messages: bool = False


@dataclass
class OpenAIConfig:
    temperature: int = 0

    max_tokens: int = 1024


@dataclass
class VectorStoreConfig:
    persist_directory: str = "db"
