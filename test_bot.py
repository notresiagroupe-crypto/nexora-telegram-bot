import asyncio, os, sys, traceback

async def main():
    token = os.getenv("TELEGRAM_TOKEN", "")
    print(f"Token: {token[:20]}..." if token else "❌ NO TOKEN")
    
    try:
        from telegram import Bot
        from telegram.ext import Application
        
        print("Creating bot...")
        bot = Bot(token=token)
        
        print("Getting bot info...")
        me = await bot.get_me()
        print(f"✅ Bot OK: @{me.username}")
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
        sys.exit(1)

asyncio.run(main())
