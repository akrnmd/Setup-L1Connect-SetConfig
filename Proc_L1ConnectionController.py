import cloudshell.helpers.scripts.cloudshell_scripts_helpers as helpers

# How to use this file

# import Proc_L1ConnectionController as L1ConnectionController
# L1ConnectionController.ChangeStateOfAllL1Routes("Connect")
# or
# L1ConnectionController.ChangeStateOfAllL1Routes("Disconnect")

def ChangeStateOfAllL1Routes(TargetState):
    reservation_id = helpers.get_reservation_context_details().id

    session = helpers.get_api_session()
    resources = session.GetReservationDetails(reservation_id).ReservationDescription

    routes = session.GetReservationDetails(reservation_id).ReservationDescription.RequestedRoutesInfo

    for route in routes:
        endpoints = []

        routeType = route.RouteType
        endpoints.append(route.Source)
        endpoints.append(route.Target)
        if TargetState == "Connect":
            session.WriteMessageToReservationOutput(reservation_id, "Connect route: " + route.Source + " to:" + route.Target)
            session.ConnectRoutesInReservation(reservation_id, endpoints, routeType)
        if TargetState == "Disonnect":
            session.WriteMessageToReservationOutput(reservation_id,
                                                    "DisConnect route: " + route.Source + " to:" + route.Target)
            session.DisconnectRoutesInReservation(reservation_id, endpoints)