from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
import Proc_L1ConnectionController as L1ConnectionController


def main():
# Default Setup Process
    sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox)
    sandbox.execute_setup()

# Additional Setup Process
# Connect All L1 Routes
    L1ConnectionController.ChangeStateOfAllL1Routes("Connect")

# Set Config
# insert code here

# Entry Point
if __name__ == "__main__":
    main()