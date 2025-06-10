import os
from dotenv import load_dotenv

load_dotenv()

# === Secrets ===
ANTHROPIC_API_KEY   = os.getenv("ANTHROPIC_API_KEY")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
SENDGRID_API_KEY    = os.getenv("SENDGRID_API_KEY")

# === Source settings ===
# arXiv categories (e.g. cs.LG, stat.ML)
ARXIV_CATEGORIES    = os.getenv("ARXIV_CATEGORIES", "cs.LG,stat.ML").split(",")

# Queries for Claude’s web_search tool
SEARCH_QUERIES      = os.getenv("SEARCH_QUERIES", "latest AI news").split(";")

# How many tweets to fetch (if using Twitter)
NUM_TWEETS          = int(os.getenv("NUM_TWEETS", "100"))

# === Email settings ===
EMAIL_FROM         = os.getenv("EMAIL_FROM")
EMAIL_TO           = os.getenv("EMAIL_TO")
EMAIL_SUBJECT      = os.getenv("EMAIL_SUBJECT", "Daily AI Newsletter")

# === Delivery controls ===
# e.g. maximum items per newsletter
MAX_ITEMS          = int(os.getenv("MAX_ITEMS", "10"))
