from exceptions.transport_collection_exception import NotFoundException
from repositories.driver_repository import DriverRepository

class DriverService:
    def __init__(self):
        self.repository = DriverRepository()

    async def create(self, data):
        return await self.repository.create(data)

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, driver_id):
        driver = await self.repository.get_by_id(driver_id)
        if not driver:
            raise NotFoundException("Driver id not found")
        return driver

    async def delete(self, driver_id):
        if not await self.repository.delete(driver_id):
            raise NotFoundException("Driver id not found")
        return {"message": "Driver deleted"}
