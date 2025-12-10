from fastapi import FastAPI, HTTPException
from app.models import GraphRunRequest
from app.workflow_impl import create_code_review_graph

app = FastAPI()

# Initialize our sample graph
# In a real app, you might load this from a DB based on ID
graph_engine = create_code_review_graph()

@app.get("/")
def home():
    return {"message": "AI Workflow Engine is Ready"}

@app.post("/graph/run")
async def run_workflow(request: GraphRunRequest):
    """
    Executes the workflow.
    Input: JSON with graph_id and initial_state
    Output: Final state and execution history
    """
    
    print(f"Starting workflow with state: {request.initial_state}")
    
    try:
        final_state = await graph_engine.run(request.initial_state)
        
        return {
            "status": "success",
            "final_state": final_state.data,
            "execution_history": final_state.history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))