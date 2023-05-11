from typing import Union

from fastapi import FastAPI

from N001.TEMPERATURE.main import get_temp_data
from N001.HEIGHT.main import get_height_data

app = FastAPI()


@app.get("/")
def read_root():
    data = get_temp_data()
    return data #{"Hellos": "World"}


@app.get("/sensor/{sensor_id}/start")
async def read_item(sensor_id: str, q: Union[str, None] = None):
    if sensor_id == '2':
        data = await get_height_data()
    # if sensor_id == '4':
    #     data = 1
    if sensor_id == '5':
        data = get_temp_data()

    return {"sensor_id": sensor_id, 'data': data}