import os
import json
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from tools.sql_tool import run_sql, get_schema

load_dotenv()

if not os.environ.get("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY not set. Add it to your .env file.")


@tool
def sql_tool(query: str) -> str:
    """Query the 'orders' table using SQLite SQL syntax.
    Use GROUP BY, ORDER BY, LIMIT for rankings/top-N questions.
    Column names with spaces or symbols (like %) MUST be wrapped in double quotes,
    e.g. SELECT "Product line", SUM("Total") FROM orders GROUP BY "Product line"."""
    return run_sql(query)


TOOLS = [sql_tool]
TOOL_MAP = {t.name: t for t in TOOLS}

llm = ChatGroq(temperature=0, model_name="openai/gpt-oss-120b")
llm_with_tools = llm.bind_tools(TOOLS)

ACTUAL_COLUMNS = get_schema()


def invoke_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return llm_with_tools.invoke(messages)
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep(4 * (attempt + 1))
                continue
            raise


# ---------------------------------------------------------------------------
# 1. General Q&A agent
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a business analyst with access to a SQLite table named 'orders'.\n"
    f"The EXACT column names in this table are: {ACTUAL_COLUMNS}\n"
    "You must use these exact column names, including spaces and symbols, "
    "wrapped in double quotes in every query.\n"
    "Always answer data questions by calling sql_tool with an appropriate SQL query.\n"
    "If a query returns a SQL Error, fix the column name or syntax and retry.\n"
    "Give the final answer in plain, clear language including the actual numbers."
)


def ask_agent(question: str) -> str:
    try:
        messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=question)]
        for _ in range(8):
            ai_msg = invoke_with_retry(messages)
            messages.append(ai_msg)
            if not ai_msg.tool_calls:
                return ai_msg.content
            for call in ai_msg.tool_calls:
                tool_fn = TOOL_MAP.get(call["name"])
                output = tool_fn.invoke(call["args"]) if tool_fn else f"Unknown tool: {call['name']}"
                messages.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
        return "Reached max tool-call iterations without a final answer."
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# 2. General store-wide insights
# ---------------------------------------------------------------------------

INSIGHTS_PROMPT = (
    "You are a senior business analyst with access to sql_tool for the 'orders' table.\n"
    f"Exact columns: {ACTUAL_COLUMNS}\n"
    "Run SQL queries to find the 3 most important insights about this business. "
    "For each, run ONE query, then write ONE short sentence with the actual number. "
    "Return only a numbered list of 3 insights, nothing else."
)


def generate_insights() -> str:
    try:
        messages = [SystemMessage(content=INSIGHTS_PROMPT),
                    HumanMessage(content="Generate the key business insights now.")]
        for _ in range(6):
            ai_msg = invoke_with_retry(messages)
            messages.append(ai_msg)
            if not ai_msg.tool_calls:
                return ai_msg.content
            for call in ai_msg.tool_calls:
                tool_fn = TOOL_MAP.get(call["name"])
                output = tool_fn.invoke(call["args"]) if tool_fn else f"Unknown tool: {call['name']}"
                messages.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
        return "Could not complete insights within iteration limit."
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# 3. Question-specific insights (used by the "🧠 Insights on this" button)
# ---------------------------------------------------------------------------

QUESTION_INSIGHTS_PROMPT = (
    "You are a senior business analyst with access to sql_tool for the 'orders' table.\n"
    f"Exact columns: {ACTUAL_COLUMNS}\n"
    "The user asked a specific question. Run 1-3 SQL queries to dig deeper into THIS "
    "exact topic (not general store trends) and surface 2-4 non-obvious findings "
    "specifically related to what they asked.\n"
    "For each finding, write ONE short sentence with the actual number, directly tied "
    "to their question. Return only a numbered list, no preamble, no generic overview."
)


def generate_question_insights(question: str) -> str:
    try:
        messages = [
            SystemMessage(content=QUESTION_INSIGHTS_PROMPT),
            HumanMessage(content=f"The user's question was: '{question}'. Generate insights specifically about this."),
        ]
        for _ in range(6):
            ai_msg = invoke_with_retry(messages)
            messages.append(ai_msg)
            if not ai_msg.tool_calls:
                return ai_msg.content
            for call in ai_msg.tool_calls:
                tool_fn = TOOL_MAP.get(call["name"])
                output = tool_fn.invoke(call["args"]) if tool_fn else f"Unknown tool: {call['name']}"
                messages.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
        return "Could not complete insights within iteration limit."
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# 4. Multi-chart data generator (used by "📊 Visualize this")
# ---------------------------------------------------------------------------

CHART_PROMPT = (
    "You are a data visualization assistant with access to sql_tool for the 'orders' table.\n"
    f"Exact columns: {ACTUAL_COLUMNS}\n"
    "The user's question may need ONE or SEVERAL charts to fully answer it. "
    "For each distinct breakdown needed, run a SQL query with GROUP BY (label + numeric value, max 15 rows).\n"
    "When you have run all needed queries, respond with ONLY raw JSON, no markdown, in exactly this format:\n"
    '{"charts": [{"chart_type": "bar", "title": "short title", "labels": ["a","b"], "values": [1.0, 2.0]}, '
    '{"chart_type": "pie", "title": "short title 2", "labels": ["c","d"], "values": [3.0, 4.0]}]}\n'
    "Use chart_type \"line\" for trends/time/dates, \"pie\" for share/percentage breakdowns, "
    "\"bar\" for category comparisons. Include one chart object per distinct breakdown the "
    "question asks for — if it asks for 3 different breakdowns, return 3 chart objects."
)


def generate_chart_data(question: str) -> dict:
    try:
        messages = [SystemMessage(content=CHART_PROMPT), HumanMessage(content=question)]
        for _ in range(8):
            ai_msg = invoke_with_retry(messages)
            messages.append(ai_msg)
            if not ai_msg.tool_calls:
                text = ai_msg.content.strip().replace("```json", "").replace("```", "").strip()
                return json.loads(text)
            for call in ai_msg.tool_calls:
                tool_fn = TOOL_MAP.get(call["name"])
                output = tool_fn.invoke(call["args"]) if tool_fn else f"Unknown tool: {call['name']}"
                messages.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
        return {"charts": []}
    except Exception as e:
        return {"charts": [], "error": str(e)}