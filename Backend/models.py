from pydantic import BaseModel

class Element(BaseModel):
    titre : str
    groupe : str
    source : str
    ordre : int = None