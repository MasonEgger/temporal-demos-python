import asyncio


async def main():
    for i in range(0, 10):
        print(i)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
