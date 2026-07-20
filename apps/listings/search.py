from dataclasses import dataclass
from datetime import date

@dataclass(slots=True)
class ListingSearchParams:
    check_in: date | None = None
    check_out: date | None = None
    adults: int | None = None
    children: int | None = None