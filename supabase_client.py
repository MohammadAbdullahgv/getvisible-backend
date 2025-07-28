from supabase import create_client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = create_client(url, key)
