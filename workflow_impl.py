import asyncio
from app.engine import WorkflowEngine



async def extract_functions(state: dict):
    """Simulates extracting functions from code."""
    code = state.get("code", "")
    return {
        "functions": ["func_a", "func_b"], 
        "log": "Extracted 2 functions from code."
    }

async def check_complexity(state: dict):
    """Simulates checking cyclomatic complexity."""
    current_score = state.get("quality_score", 5)
    return {
        "complexity_report": "High complexity detected",
        "quality_score": current_score,
        "log": "Complexity check complete."
    }

async def suggest_improvements(state: dict):
    """Simulates an AI suggesting fixes."""
    current_score = state.get("quality_score", 0)
    new_score = current_score + 3  
    return {
        "quality_score": new_score,
        "log": f"Applied improvements. New Score: {new_score}"
    }


def is_quality_low(state: dict):
    return state.get("quality_score", 0) < 10

def is_quality_high(state: dict):
    return state.get("quality_score", 0) >= 10


def create_code_review_graph():
    engine = WorkflowEngine()
    
    # Register the nodes
    engine.add_node("extract", extract_functions)
    engine.add_node("complexity", check_complexity)
    engine.add_node("improve", suggest_improvements)
    
    # Set the starting point
    engine.set_start_node("extract")
    
    # Define the flow (Edges)
    # 1. Extract -> Complexity
    engine.add_edge("extract", "complexity")
    
    # 2. Complexity -> Improve
    engine.add_edge("complexity", "improve")
    
    
    engine.add_edge("improve", "improve", condition=is_quality_low)
    
    
    
    return engine