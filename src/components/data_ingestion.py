import sys
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

from src.entity.config_entity import DataIngestionConfig
from src.exception import CustomException
from src.logger import logging


class DataIngestion:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()

        self.data_ingestion_config = DataIngestionConfig()

    def get_data_loader_docs(self, folder: str) -> List[Document]:
        """
        This function loads text documents from a specified folder using a DirectoryLoader and returns them
        as a list of Document objects.

        Args:
          folder (str): The folder path where the text files to be loaded are located.

        Returns:
          The method `get_data_loader_docs` returns a list of `Document` objects.
        """
        logging.info("Entered get_data_loader_docs method of DataIngestion class")

        try:
            loader = DirectoryLoader(
                folder,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs=self.data_ingestion_config.data_loader_kwargs,
            )

            logging.info("Used DirectoryLoader to load documents")

            documents: List[Document] = loader.load()

            logging.info("Loaded documents to memory")

            logging.info("Exited get_data_loader_docs method of DataIngestion class")

            return documents

        except Exception as e:
            raise CustomException(e, sys)

    def split_docs(self, docs: List[Document]) -> List[Document]:
        """
        This function splits a list of documents into smaller text chunks using a character text splitter.

        Args:
          docs (List[Document]): A list of Document objects that need to be split into smaller chunks.

        Returns:
          a list of documents after splitting them using a character text splitter.
        """
        logging.info("Entered split_docs method of DataIngestion class")

        try:
            text_splitter = CharacterTextSplitter(
                **self.data_ingestion_config.char_splitter_args
            )

            logging.info(
                f"Initialised CharacterTextSplitter with {self.data_ingestion_config.char_splitter_args} args"
            )

            texts: List[Document] = text_splitter.split_documents(documents=docs)

            logging.info("Split the docs with CharacterTextSplitter")

            logging.info("Exited split_docs method of DataIngestion class")

            return texts

        except Exception as e:
            raise CustomException(e, sys)

    def persist_data(self, texts: List[Document], persist_directory: str) -> None:
        """
        This function persists data by creating a Chroma vector database from a list of documents and
        embeddings and saving it to a specified directory.

        Args:
          texts (List[Document]): A list of Document objects that contain the text data to be persisted.
          persist_directory (str): The directory where the vector database will be persisted or saved.
        """
        logging.info("Entered persist_data method of DataIngestion class")

        try:
            vectordb = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=persist_directory,
            )

            logging.info(
                f"Created Chroma vectordb from docs with {self.embeddings} as embeddings and {persist_directory} as persist directory"
            )

            vectordb.persist()

            logging.info(f"Persisted the data to {persist_directory} folder")

            logging.info("Exited persist_data method of DataIngestion class")

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_ingestion(self) -> None:
        """
        This function starts the data ingestion process by getting documents from a specified folder,
        splitting them into texts, and persisting them in a specified directory.
        """
        logging.info("Entered start_data_ingestion method of DataIngestion class")

        try:
            docs = self.get_data_loader_docs(
                folder=self.data_ingestion_config.data_folder
            )

            texts = self.split_docs(docs=docs)

            self.persist_data(
                texts=texts,
                persist_directory=self.data_ingestion_config.persist_directory,
            )

            logging.info("Exited start_data_ingestion method of DataIngestion class")

        except Exception as e:
            raise CustomException(e, sys)
