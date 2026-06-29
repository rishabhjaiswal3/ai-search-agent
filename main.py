import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from openai import APIConnectionError
# from tavily import TavilyClient
from langchain_tavily import TavilySearch


# @tool
# def search_tavily(query: str) -> str:
#     """
#     Search the web for the query
#     Args:
#         query: The query to search for
#     Returns:
#         The search results
#     """
#     # return "This is a test search result"
#     tavily_api_key = os.getenv("TAVILY_API_KEY")

#     if not tavily_api_key:
#         raise ValueError("TAVILY_API_KEY is not set")

#     client = TavilyClient(api_key=tavily_api_key)
#     results = client.search(query)
#     return results



def main():
    load_dotenv(override=True)

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in `.env`")

    # Prove the tool itself returns the hardcoded value (no LLM involved).
    # print("[direct tool call]", search_tavily.invoke({"query": "What is the weather in Tokyo?"}))

    llm = ChatOpenAI(
        #  model="gpt-4o-mini", temperature=0, api_key=openai_api_key
          ) 

    tools = [TavilySearch()]
    graph = create_agent(
        model=llm,
        tools=tools,
        # system_prompt=(
        #     "You are a helpful assistant.\n"
        #     "For this question, you MUST call the `search_tavily` tool exactly once before answering.\n"
        #     "Then answer with the tool result."
        # ),
        # debug=True,
    )
    try:
        result = graph.invoke({"messages": [{"role": "user", "content": "Search for Job Search for AI Engineer In India And return the results in a list of jobs with the company name, job title, job description, and job url?"}]})
    except APIConnectionError as e:
        print(
            "\n[agent failed] The LLM request to OpenAI is being blocked (proxy/403), so the agent never gets a chance "
            "to call your tool.\n"
            "Fix the proxy/network, or switch the agent LLM to a local model (Ollama) to test tool-calling offline."
        )
        raise

    print("\n--- Messages (you should see a ToolMessage) ---")
    for m in result["messages"]:
        role = getattr(m, "type", m.__class__.__name__)
        content = getattr(m, "content", m)
        print(f"{role}: {content}")

    last_message = result["messages"][-1]
    print("\n--- Final AI output ---")
    print(getattr(last_message, "content", last_message))

if __name__ == "__main__":
    main()