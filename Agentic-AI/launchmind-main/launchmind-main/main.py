from dotenv import load_dotenv
load_dotenv()

from agents.ceo_agent import run as run_ceo
from message_bus import print_full_log

# ── Your startup idea goes here ────────────────────────────────
STARTUP_IDEA = "A mobile app that connects students with local tutors"

if __name__ == "__main__":
    print("\n🚀 LAUNCHMIND STARTING...\n")
    result = run_ceo(STARTUP_IDEA)
    print("\n📋 PRINTING FULL MESSAGE LOG...")
    print_full_log()