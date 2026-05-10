from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from app.queries import get_listing_by_id, get_listings, get_stats
from app.schemas import Listing, Stats

app = FastAPI(
    title="Cian Studios API",
    description="API для просмотра данных по аренде студий в ЮВАО Москвы, собранных с ЦИАН.",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/listings", response_model=list[Listing])
def listings(
    limit: int = Query(default=10, ge=1, le=100, description="Размер ответа, максимум 100"),
    offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
    min_price: int | None = Query(default=None, ge=0, description="Минимальная цена"),
    max_price: int | None = Query(default=None, ge=0, description="Максимальная цена"),
    min_area: float | None = Query(default=None, ge=0, description="Минимальная площадь"),
    max_area: float | None = Query(default=None, ge=0, description="Максимальная площадь"),
    sort_by: str = Query(default="price_rub", description="Поле сортировки"),
    sort_order: str = Query(default="asc", description="Порядок сортировки: asc или desc"),
) -> list[Listing]:
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price cannot be greater than max_price")

    if min_area is not None and max_area is not None and min_area > max_area:
        raise HTTPException(status_code=400, detail="min_area cannot be greater than max_area")

    try:
        return get_listings(
            limit=limit,
            offset=offset,
            min_price=min_price,
            max_price=max_price,
            min_area=min_area,
            max_area=max_area,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/listings/{listing_id}", response_model=Listing)
def listing_by_id(listing_id: str) -> Listing:
    row = get_listing_by_id(listing_id)

    if row is None:
        raise HTTPException(status_code=404, detail="Listing not found")

    return row


@app.get("/stats", response_model=Stats)
def stats() -> Stats:
    return get_stats()
