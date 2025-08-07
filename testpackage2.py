import asyncio
import bdomarket

async def main():
    async with bdomarket.Market():
        pass
    
if __name__ == "__main__":
    asyncio.run(main())