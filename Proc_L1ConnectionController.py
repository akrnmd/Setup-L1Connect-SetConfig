import cloudshell.helpers.scripts.cloudshell_scripts_helpers as helpers
# How to use this file
#
# from Proc_L1ConnectionController import L1ConnectionController
# L1CC = L1ConnectionController()
# L1CC.ChangeStateOfAllL1Routes("Connect")
class L1ConnectionController:
    def __init__(self):
        self.reservation_id = helpers.get_reservation_context_details().id
        self.session = helpers.get_api_session()
        self.routes = self.session.GetReservationDetails(self.reservation_id).ReservationDescription.RequestedRoutesInfo

    def ChangeStateOfAllL1Routes(self, TargetState):
        for route in self.routes:
            endpoints = []

            routeType = route.RouteType
            endpoints.append(route.Source)
            endpoints.append(route.Target)
            if TargetState == "Connect":
                self.session.WriteMessageToReservationOutput(self.reservation_id, "Connect route: " + route.Source + " to:" + route.Target)
                self.session.ConnectRoutesInReservation(self.reservation_id, endpoints, routeType)
            if TargetState == "Disconnect":
                self.session.WriteMessageToReservationOutput(self.reservation_id,
                                                        "DisConnect route: " + route.Source + " to:" + route.Target)
                self.session.DisconnectRoutesInReservation(self.reservation_id, endpoints)