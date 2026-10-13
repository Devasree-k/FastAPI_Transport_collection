from database import get_connection

class DriverRepository:
    async def create(self, data):
        async with await get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO drivers (driver_name, phone_number) VALUES (%s, %s) RETURNING driver_id, driver_name, phone_number",
                    (data["driver_name"], data["phone_number"])
                )
                return await cur.fetchone()

    async def get_all(self):
        async with await get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT driver_id, driver_name, phone_number FROM drivers ORDER BY driver_id")
                return await cur.fetchall()

    async def get_by_id(self, driver_id):
        async with await get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT driver_id, driver_name, phone_number FROM drivers WHERE driver_id=%s", (driver_id,))
                return await cur.fetchone()

    async def delete(self, driver_id):
        async with await get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("DELETE FROM drivers WHERE driver_id=%s RETURNING driver_id", (driver_id,))
                return await cur.fetchone()
