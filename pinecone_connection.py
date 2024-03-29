#####-----importing neccessary libraries-----#####

import pinecone
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection

#####-----main connection clas-----#####

class PineconeConnection(ExperimentalBaseConnection[pinecone.Index]):

    def _connect(self, **kwargs) -> pinecone.Index:
        pinecone.init(
            api_key = st.secrets["pinecone_api_key"],
            environment = st.secrets["pinecone_environment"]
            )
        index = pinecone.Index(st.secrets["index_name"])
        return index
    
    def cursor(self) -> pinecone.Index:
        if hasattr(self, "_instance") and self._instance:
            return self._instance
        self._instance = self._connect()
        return self._instance
    
    def query(self, query: list, n: int, ttl: int = 3600, **kwargs) -> dict:
        @st.cache_data(ttl=ttl)
        def _query(query: list, n: int, **kwargs) -> dict:
            cursor = self.cursor()
            result = cursor.query([query], top_k=n, include_metadata=True)
            return result.to_dict()

        return _query(query, n, **kwargs)
        
