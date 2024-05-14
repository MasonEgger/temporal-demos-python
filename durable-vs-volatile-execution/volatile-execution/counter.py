import asyncio


async def main():
    number = 1
    limit = 10
    while number <= limit:
        print(number)
        number = number + 1
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
