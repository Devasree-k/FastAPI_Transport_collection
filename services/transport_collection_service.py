from pathlib import Path
from uuid import uuid4

import aiofiles
from fastapi import UploadFile

import config
from exceptions.transport_collection_exception import (
    BadRequestException,
    NotFoundException,
)
from models.totals import CollectionTotals
from repositories.driver_repository import DriverRepository
from repositories.transport_collection_repository import CollectionRepository


ALLOWED_REPORT_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "application/pdf": ".pdf",
}
MAX_REPORT_SIZE = 10 * 1024 * 1024


class CollectionService:
    def __init__(self):
        self.repository = CollectionRepository()
        self.driver_repository = DriverRepository()

    def calculate_totals(self, data):
        total_trips = data["morning_trips"] + data["evening_trips"]
        total_collection = data["morning_collection"] + data["evening_collection"]
        total_expense = data["fuel_expense"] + data["other_expense"]
        return CollectionTotals(
            total_trips, 
            total_collection, 
            total_expense,
            total_collection - total_expense
        )

    async def create(self, data):
        if not await self.driver_repository.get_by_id(data["driver_id"]):
            raise NotFoundException("Driver id not found")
        return await self.repository.create(data, self.calculate_totals(data))

    # async def get_all(self):
    #     return await self.repository.get_all()

    
    async def get_all(self, page: int = 1, limit: int = 3):
        offset = (page - 1) * limit

        collections = await self.repository.get_all( limit, offset)

        total_records = await self.repository.get_total_count()

        total_pages = ((total_records + limit - 1) // limit)

        return {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "total_pages": total_pages,
            "has_previous": page > 1,
            "has_next": page < total_pages,
            "data": collections
        }


    async def get_by_id(self, collection_id):
        collection = await self.repository.get_by_id(collection_id)
        if not collection:
            raise NotFoundException("Collection not found")
        return collection

    async def patch(self, collection_id, changes):
        current = await self.get_by_id(collection_id)
        data = {
            "driver_id": current["driver_id"],
            "vehicle_number": current["vehicle_number"],
            "collection_date": current["collection_date"],
            "morning_trips": current["morning_trips"],
            "evening_trips": current["evening_trips"],
            "morning_collection": current["morning_collection"],
            "evening_collection": current["evening_collection"],
            "fuel_expense": current["fuel_expense"],
            "other_expense": current["other_expense"],
        }
        data.update(changes)
        if not await self.driver_repository.get_by_id(data["driver_id"]):
            raise NotFoundException("Driver not found")
        return await self.repository.patch(
            collection_id, changes, self.calculate_totals(data)
        )

    async def delete(self, collection_id):
        if not await self.repository.delete(collection_id):
            raise NotFoundException("Collection not found")
        return {"message": "Collection deleted"}

    async def save_upload_file(self, file: UploadFile, collection_id: int):
        extension = Path(file.filename or "").suffix.lower()
        if file.content_type not in ALLOWED_REPORT_TYPES:
            raise BadRequestException("Upload a JPG, PNG or PDF report")

        upload_folder = Path(config.UPLOAD_FOLDER) / str(collection_id)
        upload_folder.mkdir(parents=True, exist_ok=True)
        extension = ALLOWED_REPORT_TYPES[file.content_type]
        file_path = upload_folder / f"{uuid4().hex}{extension}"
        total_size = 0

        try:
            async with aiofiles.open(file_path, "wb") as output_file:
                while True:
                    chunk = await file.read(1024 * 1024)
                    if not chunk:
                        break
                    total_size += len(chunk)
                    if total_size > MAX_REPORT_SIZE:
                        if file_path.exists():
                            file_path.unlink()
                        raise BadRequestException("Report file cannot exceed 10 MB")
                    await output_file.write(chunk)
        finally:
            await file.close()

        return file_path.as_posix()

    async def upload_report(self, collection_id: int, file: UploadFile):
        await self.get_by_id(collection_id)
        file_path = await self.save_upload_file(file, collection_id)
        await self.repository.update_report(collection_id, file_path)
        return {"message": "File uploaded", "file_path": file_path}
