from pydantic import BaseModel


class Amenity(BaseModel):
    c_amenity_id: int
    c_amenity_name: str
    c_amenity_group_id: int
    c_amenity_group_name: str
    c_amenity_group_priority: int
    c_amenity_priority_inside_group: int
