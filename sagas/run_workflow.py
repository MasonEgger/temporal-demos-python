import os
import uuid
from typing import Optional

from activities import BookVacationInput

# Import the workflow from the previous code
from book_workflow import BookWorkflow
from flask import Flask, render_template, request
from temporalio.client import Client, TLSConfig

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
async def display_form():
    if request.method == "GET":
        return render_template("book_vacation.html")

    user_id = f'{request.form.get("name").replace(" ", "-").lower()}-{str(uuid.uuid4().int)[:6]}'
    attempts = request.form.get("attempts")
    car = request.form.get("car")
    hotel = request.form.get("hotel")
    flight = request.form.get("flight")
    failure = request.form.get("failure")
    name = request.form.get("name")

    input = BookVacationInput(
        attempts=int(attempts),
        book_user_id=user_id,
        book_car_id=car,
        book_hotel_id=hotel,
        book_flight_id=flight,
        simulated_failure=failure,
    )

    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        BookWorkflow.run,
        input,
        id=user_id,
        task_queue="saga-task-queue",
    )
    if result == "PyCon Trip Cancelled :(":
        return render_template("book_vacation.html", cancelled=True)

    else:
        result_list = result.split("Booked ")
        car = result_list[1].split(":")[1].title()
        hotel = result_list[2].split(":")[1].title()
        flight = result_list[3].split(":")[1].title()
        return render_template(
            "book_vacation.html",
            result=result,
            cancelled=False,
            car=car,
            hotel=hotel,
            flight=flight,
            user_id=user_id,
            name=name,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
