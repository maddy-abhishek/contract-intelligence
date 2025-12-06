from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Sub-models for complex fields
class Signatory(BaseModel):
    name: Optional[str] = Field(None, description="Name of the person signing")
    title: Optional[str] = Field(None, description="Job title of the person signing")

class Party(BaseModel):
    name: str = Field(..., description="Legal name of the company or individual")
    role: Optional[str] = Field(None, description="Role in contract (e.g., Client, Provider)")

# 2. The Main Contract Schema
class ContractExtraction(BaseModel):
    parties: List[Party] = Field(..., description="List of parties involved in the contract")
    effective_date: Optional[str] = Field(None, description="The date the contract becomes active")
    term: Optional[str] = Field(None, description="The duration of the contract (e.g., '1 year')")
    governing_law: Optional[str] = Field(None, description="State or Country law that applies")
    payment_terms: Optional[str] = Field(None, description="When payments are due (e.g., 'Net 30')")
    termination: Optional[str] = Field(None, description="Conditions for ending the contract")
    auto_renewal: bool = Field(False, description="True if contract renews automatically")
    confidentiality: Optional[str] = Field(None, description="Summary of confidentiality clauses")
    indemnity: Optional[str] = Field(None, description="Summary of indemnification obligations")
    liability_cap: Optional[str] = Field(None, description="Monetary cap on liability (e.g., '$1,000,000')")
    signatories: List[Signatory] = Field(default_factory=list, description="List of people who signed")