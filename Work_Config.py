# coding:utf-8
from cloudshell.api.cloudshell_api import InputNameValue
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.common_cloudshell_api import CloudShellAPIError


class WorkConfig:
    def __init__(self):
        self.sandbox = Sandbox()
        self.automation_api = self.sandbox.automation_api
        self.blueprint = self.automation_api.ActivateTopology
        self.reservation_id = self.sandbox.reservationContextDetails.id
        self.reservation_details = self.automation_api.GetReservationDetails(self.reservation_id)
        self.reservation_description = self.reservation_details.ReservationDescription
        self._FIRST_ONE = 0

    def input_config_all(self, config_attribute):
        # Reserve直後のSetupは、BlueprintのAttributeを使用
        if self.reservation_description.Status == 'Started':
            blueprint_name = self.reservation_description.TopologiesInfo[self._FIRST_ONE].Name
            for blueprint_resource in self.blueprint(self.reservation_id, blueprint_name).Resources:
                resource_attributes = blueprint_resource.ResourceAttributes
                try:
                    attribute_index = list(map(lambda x: x.Name, resource_attributes)).index(config_attribute)
                    config_path = resource_attributes[attribute_index].Value
                    self.input_config(blueprint_resource.Name, config_path)

                except ValueError:
                    continue

        # Active以降の手動Setupは、SandboxのAttributeを使用
        else:
            for resource in self.reservation_description.Resources:
                # コンフィグのパスを取得
                try:
                    config_path = self.automation_api.GetAttributeValue(resource.Name, config_attribute).Value
                    self.input_config(resource.Name, config_path)

                # Attributeが取得できないリソースはスキップ
                except CloudShellAPIError:
                    continue

    def input_config(self, resource_name, config_path, config_type='running', config_method='override'):
        """
        :param resource_name: リソース名
        :param config_path: コンフィグのパス
        :param config_type: write config to running or startup
        :param config_method: override or append
        :return: none
        """
        input_config_details = [InputNameValue('path', config_path),
                                InputNameValue('configuration_type', config_type),
                                InputNameValue('restore_method', config_method),
                                InputNameValue('vrf_management_name', '')]

        try:
            self.automation_api.ExecuteCommand(reservationId=self.reservation_id,
                                               targetName=resource_name,
                                               targetType='Resource',
                                               commandName='restore',
                                               commandInputs=input_config_details)
            self._sandbox_output('Success input config to: ' + resource_name)

        except CloudShellAPIError:
            self._sandbox_output('Failed input config to: ' + resource_name)

    # SandboxのOutput上にテキストを表示
    def _sandbox_output(self, text):
        """
        :param text: Output上に表示させるテキスト
        :return:
        """
        self.automation_api.WriteMessageToReservationOutput(self.reservation_id, text)
