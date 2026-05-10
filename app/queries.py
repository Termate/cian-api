from __future__ import annotations

from typing import Any

from app.database import get_connection

ALLOWED_SORT_FIELDS = {
    "price_rub",
    "area_m2",
    "scraped_at",
    "listing_id",
}

ALLOWED_SORT_ORDERS = {
    "asc",
    "desc",
}


def get_listings(
    limit: int,
    offset: int,
    min_price: int | None,
    max_price: int | None,
    min_area: float | None,
    max_area: float | None,
    sort_by: str,
    sort_order: str,
) -> list[dict[str, Any]]:
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise ValueError(f"sort_by must be one of: {sorted(ALLOWED_SORT_FIELDS)}")

    if sort_order not in ALLOWED_SORT_ORDERS:
        raise ValueError("sort_order must be 'asc' or 'desc'")

    query = "SELECT * FROM listings WHERE 1=1"
    params: list[Any] = []

    if min_price is not None:
        query += " AND price_rub >= ?"
        params.append(min_price)

    if max_price is not None:
        query += " AND price_rub <= ?"
        params.append(max_price)

    if min_area is not None:
        query += " AND area_m2 >= ?"
        params.append(min_area)

    if max_area is not None:
        query += " AND area_m2 <= ?"
        params.append(max_area)

    query += f" ORDER BY {sort_by} {sort_order.upper()} LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]


def get_listing_by_id(listing_id: str) -> dict[str, Any] | None:
    query = "SELECT * FROM listings WHERE listing_id = ? ORDER BY scraped_at DESC LIMIT 1"

    with get_connection() as conn:
        row = conn.execute(query, [listing_id]).fetchone()

    if row is None:
        return None

    return dict(row)


def get_stats() -> dict[str, Any]:
    query = '''
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT listing_id) AS unique_listings,
            MIN(price_rub) AS min_price,
            MAX(price_rub) AS max_price,
            AVG(price_rub) AS avg_price,
            AVG(area_m2) AS avg_area
        FROM listings
        WHERE price_rub IS NOT NULL
    '''

    with get_connection() as conn:
        row = conn.execute(query).fetchone()

    return dict(row)
