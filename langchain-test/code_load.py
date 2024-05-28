import warnings

warnings.filterwarnings("ignore")

from langchain.globals import set_debug

set_debug(True)

from langchain.globals import set_verbose

set_verbose(True)



from pprint import pprint

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language





loader = GenericLoader.from_filesystem(
    "/Users/mac/Desktop/gpt_test/langchain-test",
    glob="*",
    suffixes=[".py", ".js"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=1000),
)
docs = loader.load()


# for document in docs:
#     pprint(document.metadata)



# # print("\n\n--8<--\n\n".join([document.page_content for document in docs]))
# print("============ doc ==========")
# print(docs[0].page_content)
# print("============ doc ==========")



from langchain_text_splitters import RecursiveCharacterTextSplitter

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=1000, chunk_overlap=0
)
texts = python_splitter.split_documents(docs)


# print("============ text ==========")
# print(texts[0].page_content)
# print("============ text ==========")




from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
retriever = db.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 8},
)





from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langsmith.wrappers import wrap_openai
# from langsmith import traceable


llm = ChatOpenAI(model="gpt-4-turbo-2024-04-09", temperature=0, verbose=True)


# First we need a prompt that we can pass into an LLM to generate this search query

prompt = ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
        (
            "user",
            "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
        ),
    ]
)

retriever_chain = create_history_aware_retriever(llm, retriever, prompt)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user's questions based on the below context:\n\n{context}",
        ),
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
    ]
)
document_chain = create_stuff_documents_chain(llm, prompt)

qa = create_retrieval_chain(retriever_chain, document_chain)



question = "main.py文件中代码提出3点优化建议,每个建议需要提供原代码出处"
result = qa.invoke({"input": question})
result["answer"]
print(result["answer"])