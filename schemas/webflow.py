from pydantic import BaseModel, Field


class Payload(BaseModel):
    name: str
    siteId: str
    data: dict
    schema_: list[dict] = Field(alias="schema")
    submittedAt: str
    id: str
    formId: str
    formElementId: str

class WebflowPayload(BaseModel):
    triggerType: str
    payload: Payload