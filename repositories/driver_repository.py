from database import get_connection

class DriverRepository:
    async def create(self, data):
        async with await get_connection() as connect:
            async with connect.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO drivers (driver_name, phone_number) VALUES (%s, %s) RETURNING driver_id, driver_name, phone_number",
                    (data["driver_name"], data["phone_number"])
                )
                return await cursor.fetchone()

    async def get_all(self):
        async with await get_connection() as connect:
            async with connect.cursor() as cursor:
                await cursor.execute("SELECT driver_id, driver_name, phone_number FROM drivers ORDER BY driver_id")
                return await cursor.fetchall()

    async def get_by_id(self, driver_id):
        async with await get_connection() as connect:
            async with connect.cursor() as cursor:
                await cursor.execute("SELECT driver_id, driver_name, phone_number FROM drivers WHERE driver_id=%s", (driver_id,))
                return await cursor.fetchone()

    async def delete(self, driver_id):
        async with await get_connection() as connect:
            async with connect.cursor() as cursor:
                await cursor.execute("DELETE FROM drivers WHERE driver_id=%s RETURNING driver_id", (driver_id,))
                return await cursor.fetchone()
