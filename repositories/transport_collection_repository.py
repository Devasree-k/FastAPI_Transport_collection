from database import get_connection

class CollectionRepository:

    async def create(self, data, totals):
        async with await get_connection() as connect:

            async with connect.cursor() as cursor:

                await cursor.execute('''
                    INSERT INTO transport_collections
                        (driver_id, 
                        vehicle_number, 
                        collection_date, 
                        morning_trips, 
                        evening_trips,
                        morning_collection, 
                        evening_collection, 
                        fuel_expense, 
                        other_expense,
                        total_trips, 
                        total_collection, 
                        total_expense,
                        net_collection)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (
                    data["driver_id"], data["vehicle_number"], data["collection_date"],
                    data["morning_trips"], data["evening_trips"],
                    data["morning_collection"], data["evening_collection"],
                    data["fuel_expense"], data["other_expense"],
                    totals.total_trips, totals.total_collection,
                    totals.total_expense, totals.net_collection
                ))
                row = await cursor.fetchone()

        return await self.get_by_id(row["id"])

    async def get_all(self, limit: int, offset: int):

        async with await get_connection() as connect:

            async with connect.cursor() as cursor:

                await cursor.execute('''
                    SELECT c.id, 
                        c.driver_id, 
                        d.driver_name, 
                        c.vehicle_number,
                        c.collection_date, 
                        c.morning_trips, 
                        c.evening_trips,
                        c.morning_collection, 
                        c.evening_collection,
                        c.fuel_expense, 
                        c.other_expense, 
                        c.total_trips,
                        c.total_collection, 
                        c.total_expense, 
                        c.net_collection,
                        c.report_file
                    FROM transport_collections c
                    JOIN drivers d ON c.driver_id = d.driver_id
                    ORDER BY c.id
                    LIMIT %s OFFSET %s
                ''', (limit, offset))

                return await cursor.fetchall()

    async def get_total_count(self):
        async with await get_connection() as connect:

            async with connect.cursor() as cursor:

                await cursor.execute('''
                    SELECT COUNT(*) AS total FROM transport_collections ''')
                
                row = await cursor.fetchone()
                return row["total"]


    async def get_by_id(self, collection_id):
        async with await get_connection() as connect:

            async with connect.cursor() as cursor:

                await cursor.execute('''
                    SELECT 
                        c.id, c.driver_id, 
                        d.driver_name, 
                        c.vehicle_number,
                        c.collection_date, 
                        c.morning_trips, 
                        c.evening_trips,
                        c.morning_collection, 
                        c.evening_collection,
                        c.fuel_expense, 
                        c.other_expense, 
                        c.total_trips,
                        c.total_collection, 
                        c.total_expense, 
                        c.net_collection,
                        c.report_file
                    FROM transport_collections c
                    JOIN drivers d ON c.driver_id = d.driver_id
                    WHERE c.id = %s
                ''', (collection_id,))

                return await cursor.fetchone()

    async def update_report(self, collection_id, filename):
        async with await get_connection() as connect:

            async with connect.cursor() as cursor:

                await cursor.execute('''
                    UPDATE transport_collections
                    SET report_file = %s
                    WHERE id = %s
                    RETURNING id
                ''', (filename, collection_id))

                return await cursor.fetchone()

    async def delete(self, collection_id):

        async with await get_connection() as connect:

            async with connect.cursor() as cursor:

                await cursor.execute('''
                    DELETE FROM transport_collections
                    WHERE id = %s
                    RETURNING id
                ''', (collection_id,))

                return await cursor.fetchone()

    async def patch(self, collection_id, data, totals):
        allowed_fields = {
            "driver_id", 
            "vehicle_number", 
            "collection_date",
            "morning_trips", 
            "evening_trips",
            "morning_collection", 
            "evening_collection",
            "fuel_expense", 
            "other_expense"
        }

        fields = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        fields["total_trips"] = totals.total_trips
        fields["total_collection"] = totals.total_collection
        fields["total_expense"] = totals.total_expense
        fields["net_collection"] = totals.net_collection

        set_values = ", ".join(
            f"{column} = %s" for column in fields
        )
        values = list(fields.values()) + [collection_id]

        async with await get_connection() as connect:
            async with connect.cursor() as cursor:
                await cursor.execute(
                    f'''
                    UPDATE transport_collections
                    SET {set_values}
                    WHERE id = %s
                    RETURNING id
                    ''',
                    values
                )

                row = await cursor.fetchone()

        if not row:
            return None

        return await self.get_by_id(collection_id)
    