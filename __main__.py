from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from Proc_L1ConnectionController import L1ConnectionController
from Work_Config import WorkConfig
from cloudshell.api.common_cloudshell_api import CommonAPISession

def main():
# Default Setup Process
    sandbox = Sandbox()
    DefaultSetupWorkflow().register(sandbox)
    sandbox.execute_setup()

# Additional Setup Process
# Connect All L1 Routes
    L1CC = L1ConnectionController()
    L1CC.ChangeStateOfAllL1Routes("Connect")

# Set Config
# insert code here
    work_config = WorkConfig()
    work_config.input_config_all("Config Path")


# Entry Point
if __name__ == "__main__":
    main()
