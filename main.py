from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from stock_agent.agent import root_agent

runner = Runner(
    agent=root_agent,
    app_name="stock_analyser",
    artifact_service=InMemoryArtifactService(),
    session_service=InMemorySessionService(),
)