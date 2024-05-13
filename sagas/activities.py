import asyncio
from dataclasses import dataclass

from temporalio import activity


@dataclass
class BookVacationInput:
    book_user_id: str
    book_car_id: str
    book_hotel_id: str
    book_flight_id: str
    attempts: int
    simulated_failure: str


SLEEP_TIME = 3


@activity.defn
async def book_car(input: BookVacationInput) -> str:
    await asyncio.sleep(SLEEP_TIME)
    if activity.info().attempt < input.attempts:
        activity.heartbeat(
            f"Invoking activity, attempt number {activity.info().attempt}"
        )
        await asyncio.sleep(SLEEP_TIME)
        raise RuntimeError("Car service is down")

    if input.simulated_failure == "car":
        raise Exception("Invalid car booking, rolling back!")

    print(f"Booking car: {input.book_car_id}")
    return f"Booked car: {input.book_car_id}"


@activity.defn
async def book_hotel(input: BookVacationInput) -> str:
    await asyncio.sleep(SLEEP_TIME)
    if activity.info().attempt < input.attempts:
        activity.heartbeat(
            f"Invoking activity, attempt number {activity.info().attempt}"
        )
        await asyncio.sleep(SLEEP_TIME)
        raise RuntimeError("Hotel service is down")

    if input.simulated_failure == "hotel":
        raise Exception("Invalid hotel booking, rolling back!")

    print(f"Booking hotel: {input.book_hotel_id}")
    return f"Booked hotel: {input.book_hotel_id}"


@activity.defn
async def book_flight(input: BookVacationInput) -> str:
    await asyncio.sleep(SLEEP_TIME)
    if activity.info().attempt < input.attempts:
        activity.heartbeat(
            f"Invoking activity, attempt number {activity.info().attempt}"
        )
        await asyncio.sleep(SLEEP_TIME)
        raise RuntimeError("Flight service is down")

    if input.simulated_failure == "flight":
        raise Exception("Invalid flight booking, rolling back!")

    print(f"Booking flight: {input.book_flight_id}")
    return f"Booked flight: {input.book_flight_id}"


@activity.defn
async def undo_book_car(input: BookVacationInput) -> str:
    print(f"Undoing booking of car: {input.book_car_id}")
    return f"Undoing booking of car: {input.book_car_id}"


@activity.defn
async def undo_book_hotel(input: BookVacationInput) -> str:
    print(f"Undoing booking of hotel: {input.book_hotel_id}")
    return f"Undoing booking of hotel: {input.book_hotel_id}"


@activity.defn
async def undo_book_flight(input: BookVacationInput) -> str:
    print(f"Undoing booking of flight: {input.book_flight_id}")
    return f"Undoing booking of flight: {input.book_flight_id}"
