from fastapi import APIRouter, File, UploadFile, status, Query
from schema.transport_collection_schema import CollectionCreate, CollectionPatch, CollectionResponse
from services.transport_collection_service import CollectionService

router = APIRouter(prefix="/collections", tags=["Transport Collections"])
service = CollectionService()

@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(data: CollectionCreate):
    return await service.create(data.model_dump())

# @router.get("/", response_model=list[CollectionResponse])
# async def get_collections():
#     return await service.get_all()


@router.get("/")
async def get_collections(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=3, ge=1, le=20)
):
    return await service.get_all(page, limit)


@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(collection_id: int):
    return await service.get_by_id(collection_id)

@router.patch("/{collection_id}", response_model=CollectionResponse)
async def patch_collection(collection_id: int, data: CollectionPatch):
    changes = data.model_dump(exclude_unset=True)
    if not changes:
        from exceptions.transport_collection_exception import BadRequestException
        raise BadRequestException("Send at least one field to update")
    return await service.patch(collection_id, changes)

@router.delete("/{collection_id}")
async def delete_collection(collection_id: int):
    return await service.delete(collection_id)

@router.post("/{collection_id}/report")
async def upload_report(collection_id: int, file: UploadFile = File(...)):
    return await service.upload_report(collection_id, file)
