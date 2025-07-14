import typer
from backend_sdk.run_agent import run_carbon_agent

app = typer.Typer(invoke_without_command=True)

@app.callback()
def main(agent_type: str = typer.Argument(..., help="Agent to run: yield_agent or identity_agent")):
    """Run an Ethereum Agent by name"""
    run_carbon_agent(agent_type)

if __name__ == "__main__":
    app()
