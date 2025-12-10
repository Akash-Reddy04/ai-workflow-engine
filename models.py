from typing import Dict, Any, List, Optional
from pydantic import BaseModel

# 1. The State that flows between nodes

class WorkflowState(BaseModel):
    data: Dict[str, Any] = {}
    history: List[str] = []  

# 2. Definitions for creating a Graph
class NodeDefinition(BaseModel):
    name: str
    function_name: str  

class EdgeDefinition(BaseModel):
    from_node: str
    to_node: str
    condition: Optional[str] = None 

# 3. API Request Models
class GraphCreateRequest(BaseModel):
    nodes: List[NodeDefinition]
    edges: List[EdgeDefinition]
    start_node: str

class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = {}