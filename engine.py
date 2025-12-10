import asyncio
from typing import Dict, Callable, Any, Optional
from app.models import WorkflowState

class WorkflowEngine:
    def __init__(self):
        
        self.nodes: Dict[str, Callable] = {}
        
        self.edges: Dict[str, list] = {} 
        self.start_node: str = ""

    def add_node(self, name: str, func: Callable):
        """Registers a function as a node in the graph."""
        self.nodes[name] = func

    def add_edge(self, from_node: str, to_node: str, condition: Optional[Callable] = None):
        """Defines a connection between two nodes."""
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append({"to": to_node, "condition": condition})

    def set_start_node(self, node_name: str):
        self.start_node = node_name

    async def run(self, initial_state: Dict[str, Any]):
        """Runs the workflow starting from the start_node."""
        state = WorkflowState(data=initial_state)
        current_node_name = self.start_node
        
        
        steps = 0
        max_steps = 20 

        while current_node_name and steps < max_steps:
            print(f"--- Executing Node: {current_node_name} ---")
            
            node_func = self.nodes.get(current_node_name)
            if not node_func:
                print(f"Error: Node '{current_node_name}' not found.")
                break
                
           
            try:
                
                updated_data = await node_func(state.data)
                if updated_data:
                    state.data.update(updated_data)
            except Exception as e:
                print(f"Error executing {current_node_name}: {e}")
                break

            
            state.history.append(current_node_name)

            
            next_node_name = None
            possible_edges = self.edges.get(current_node_name, [])
            
            for edge in possible_edges:
                condition = edge.get("condition")
                target = edge.get("to")
                
                if condition:
                    
                    if condition(state.data):
                        next_node_name = target
                        break
                else:
                    
                    next_node_name = target
                    break
            
            
            current_node_name = next_node_name
            steps += 1

        return state