# coding:utf-8
from cloudshell.api.cloudshell_api import InputNameValue
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.common_cloudshell_api import CloudShellAPIError


class WorkConfig:
    def __init__(self):
        self.sandbox = Sandbox()
        self.automation_api = self.sandbox.automation_api
        self.reservation_id = self.sandbox.reservationContextDetails.id
        self.reservation_details = self.automation_api.GetReservationDetails(self.reservation_id)
        self.reservation_description = self.reservation_details.ReservationDescription

    def input_config_all(self, config_attribute):
        for resource in self.reservation_description.Resources:
            # コンフィグのパスを取得
            try:
                config_path = self.automation_api.GetAttributeValue(resource.Name, config_attribute).Value
                self.input_config(resource.Name, config_path)

            # Attributeが取得できないリソースはスキップ
            except:
                continue

    def input_config(self, resource_name, config_path, config_type='running', config_method='override'):
        """
        :param resource_name: リソース名
        :param config_path: コンフィグのパス
        :param config_type: write config to running or startup
        :param config_method: override or append
        :return:
        """
        input_config_details = []

        input_config_details.append(InputNameValue('path', config_path))
        input_config_details.append(InputNameValue('configuration_type', config_type))
        input_config_details.append(InputNameValue('restore_method', config_method))
        input_config_details.append(InputNameValue('vrf_management_name', ''))

        try:
            self.automation_api.ExecuteCommand(reservationId=self.reservation_id,
                                               targetName=resource_name,
                                               targetType='Resource',
                                               commandName='restore',
                                               commandInputs=input_config_details)
            self._sandbox_output('Success input config to: ' + resource_name)

        except CloudShellAPIError:
            self._sandbox_output('Failed input config to: ' + resource_name)

    # "Sandbox"の"Output"上にテキストを表示
    def _sandbox_output(self, text):
        """
        :param text: Output上に表示させるテキスト
        :return:
        """
        self.automation_api.WriteMessageToReservationOutput(self.reservation_id, text)
