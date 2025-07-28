from supabase_client import client
from playwright.async_api import async_playwright
from datetime import datetime
import asyncio

async def run_campaigns(campaign_ids):
    processed = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for campaign_id in campaign_ids:
            # Fetch campaign
            campaign = client.table("campaigns").select("*").eq("id", campaign_id).single().execute().data
            account = client.table("accounts").select("*").eq("user_id", campaign["user_id"]).single().execute().data
            targets = client.table("targets").select("*").eq("campaign_id", campaign_id).eq("status", "pending").limit(10).execute().data

            context = await browser.new_context()
            await context.add_cookies(account["cookies_json"])
            page = await context.new_page()

            for target in targets:
                try:
                    await page.goto(target["twitter_url"], timeout=60000)
                    await asyncio.sleep(3)

                    full_name = "there"  # You can extract from target if needed
                    msg = campaign["message_template"].replace("{Full Name}", full_name)

                    # simulate typing
                    # await page.fill("selector-for-input-box", msg)
                    # await page.keyboard.press("Enter")
                    await asyncio.sleep(2)

                    # Update status
                    client.table("targets").update({
                        "status": "sent",
                        "sent_at": datetime.utcnow().isoformat()
                    }).eq("id", target["id"]).execute()

                except Exception as e:
                    client.table("targets").update({
                        "status": "failed"
                    }).eq("id", target["id"]).execute()
                    print(f"❌ Error: {e}")

            await context.close()
            processed.append({ "campaign": campaign_id, "targets": len(targets) })

        await browser.close()
    return processed
