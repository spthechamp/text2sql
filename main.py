import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

client = st.secrets['GROQ_API_KEY']

with open('schema.txt', 'r') as f:
    text = f.read()

st.title('NL to SQL Query Generator')
st.caption("NOTE: This is an AI model that takes schema of a database and generates a SQL query based on the questions asked to it.")

schema = st.text_area("Provide schema of your database here:", value=text)
question = st.text_input("Ask your question here:", value="How many engineers bought beauty product?")
generate_button = st.button("Generate")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant that strictly converts natural language instructions into SQL queries based only on the given database schema. "
            "You must follow these rules: "
            "1. If the user's instruction is directly related to the provided database schema, generate only the SQL query as the output, with no explanation. "
            "2. If the instruction is unrelated to the database schema, ambiguous, or lacks enough information to generate an SQL query, respond only with 'None'. "
            "3. Do not make assumptions about missing information or attempt to infer a schema that is not explicitly given. "
            "4. If any entity or field mentioned in the instruction is not present in the schema, reply strictly with 'None'. "
            "Database schema: {schema}.",
        ),
        ("human", "{instruction}"),
    ]
)

chain = prompt | llm

if generate_button:
    result = chain.invoke(
        {
            "instruction": f"{question}",
            "schema": f"{schema}"
        }
    ).content

    if result!='None':
        st.write(f"{result}")
    else:
        st.error('Irrelavant Question! Please ask questions related to your DB only.')
        