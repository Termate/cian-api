from __future__ import annotations

from pydantic import BaseModel


class Listing(BaseModel):
    listing_id: str
    district: str | None = None
    url: str | None = None
    title: str | None = None
    price_rub: int | None = None
    area_m2: float | None = None
    floor: int | None = None
    total_floors: int | None = None
    metro: str | None = None
    address: str | None = None
    description_snippet: str | None = None
    source_page: str | None = None
    scraped_at: str | None = None


class Stats(BaseModel):
    total_rows: int
    unique_listings: int
    min_price: int | None = None
    max_price: int | None = None
    avg_price: float | None = None
    avg_area: float | None = None
