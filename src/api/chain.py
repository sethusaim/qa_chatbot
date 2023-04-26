import sys

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models.openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores.chroma import Chroma

from src.entity.config_entity import (
    ChainConfig,
    MemoryConfig,
    OpenAIConfig,
    VectorStoreConfig,
)
from src.exception import CustomException
from src.logger import logging


class BotChain:
    def __init__(self):
        self.vector_store_config = VectorStoreConfig()

        self.openai_config = OpenAIConfig()

        self.memory_config = MemoryConfig()

        self.chain_config = ChainConfig()

    def get_llm_chain(self):
        """
        This function initializes and returns a ConversationalRetrievalChain object for OpenAI language
        model using Chroma database as retriever and ConversationBufferMemory as memory.

        Returns:
          The method `get_llm_chain` returns an instance of the `ConversationalRetrievalChain` class.
        """
        logging.info("Entered get_llm_chain method of LLMChain class")

        try:
            db = Chroma(
                embedding_function=OpenAIEmbeddings(),
                **self.vector_store_config.__dict__,
            )

            logging.info(
                f"Initialised Chroma db with OpenAIEmbeddings as the embedding function and {self.vector_store_config.__dict__} as the parameters"
            )

            memory = ConversationBufferMemory(**self.memory_config.__dict__)

            logging.info(
                f"Initialised ConversationBufferMemory with {self.memory_config.__dict__} as the parameters"
            )

            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=ChatOpenAI(**self.openai_config.__dict__),
                retriever=db.as_retriever(),
                memory=memory,
                get_chat_history=lambda h: h,
                **self.chain_config.__dict__,
            )

            logging.info(
                f"Initialised ConversationalRetrievalChain for OpenAI LLM with {self.openai_config.__dict__} as parameters"
            )

            logging.info("Exited get_llm_chain method of LLMChain class")

            return qa_chain

        except Exception as e:
            raise CustomException(e, sys)
