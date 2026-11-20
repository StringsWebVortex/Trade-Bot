import os

from dotenv import load_dotenv

load_dotenv()

COORDINATOR_MODEL = os.getenv("COORDINATOR_MODEL", "sonnet")
WORKER_MODEL = os.getenv("WORKER_MODEL", "haiku")
MAX_SUBTASKS = int(os.getenv("MAX_SUBTASKS", "5"))
MAX_WORKER_TURNS = int(os.getenv("MAX_WORKER_TURNS", "6"))
# Workers act on LLM-authored instructions, so default to read-only tools. Shell access
# is an explicit opt-in (ideally scoped, e.g. "Read,Grep,Glob,Bash(git log:*)").
WORKER_ALLOWED_TOOLS = os.getenv("WORKER_ALLOWED_TOOLS", "Read,Grep,Glob")
# Hard ceiling on concurrent worker threads, whatever MAX_SUBTASKS is set to.
MAX_CONCURRENT_WORKERS = 8
