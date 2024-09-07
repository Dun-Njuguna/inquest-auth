from pydantic import BaseModel
from typing import Any, Dict, List, Optional, Union

class ResponseModel(BaseModel):
    error: bool
    message: str
    data: Optional[Union[Dict[str, Any], List[Any]]]  # Accept dict or list

    class Config:
        from_attributes = True
