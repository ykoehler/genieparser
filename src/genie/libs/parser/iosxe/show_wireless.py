import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional


# ========================================
# Schema for:
#  * 'show wireless fabric client summary'
# ========================================
class ShowWirelessFabricClientSummarySchema(MetaParser):
    """Schema for show wireless fabric client summary."""

    schema = {
        "number_of_fabric_clients" : int,
        Optional("mac_address") : {
            Optional(str) : {
                Optional("ap_name") : str,
                Optional("wlan") : int,
                Optional("state") : str,
                Optional("protocol") : str,
                Optional("method") : str,
            }
        }
    }
              
# ========================================
# Parser for:
#  * 'show wireless fabric client summary'
# ========================================
class ShowWirelessFabricClientSummary(ShowWirelessFabricClientSummarySchema):
    """Parser for show wireless fabric client summary"""

    cli_command = 'show wireless fabric client summary'
    
    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
        else:
            output=output
              
        show_wireless_fabric_client_summary_dict = {}


        # Number of Fabric Clients : 8

        # MAC Address    AP Name                          WLAN State              Protocol Method     
        # --------------------------------------------------------------------------------------------
        # 58bf.ea72.1730 a2-11-cap43                   17   Run                11ac     Dot1x     
        # 58bf.ea73.39b4 a2-11-cap50                   19   IP Learn           11n(2.4) MAB       
        # 58bf.ea47.1c4c a2-11-cap52                   19   Webauth Pending    11n(2.4) MAB       
        # --------------------------------------------------------------------------------------------
        # 58bf.ea47.1c59 a2-11-cap46                   17   Run                11ac     Dot1x     
        # 58bf.ea41.eac4 a2-12-cap15                   19   Webauth Pending    11n(2.4) MAB       
        # 58bf.eaef.9769 a2-11-cap44                   19   Webauth Pending    11n(2.4) MAB       
        # --------------------------------------------------------------------------------------------
        # 58bf.ea02.5c2a a2-12-cap17                   19   Webauth Pending    11ac     MAB       
        # 58bf.ea09.f357 a2-12-cap17                   19   Webauth Pending    11ac     MAB   

        # Number of Fabric Clients : 8
        p_clients = re.compile(r"^Number\s+of\s+Fabric\s+Clients\s+:\s+(?P<clients>\S+)$")

        # MAC Address    AP Name                          WLAN State              Protocol Method
        p_header = re.compile(r"^MAC\s+Address\s+AP\s+Name\s+WLAN\s+State\s+Protocol\s+Method$")

        # -------------------------------------------------------------------------------------------------------------------------
        p_delimiter = re.compile(
            r"^-------------------------------------------------------------------------------------------------------------------------$")

        # 58bf.ea72.1730 a2-11-cap43                   17   Run                11ac     Dot1x
        p_client_info = re.compile(r"^(?P<mac>\S{4}\.\S{4}\.\S{4})\s+(?P<name>\S+)\s+(?P<wlan>\S+)\s+(?P<state>.*)\s+(?P<protocol>\S+)\s+(?P<method>(Dot1x|MAB))$")


        show_wireless_fabric_client_summary_dict = {}

        for line in output.splitlines():
            line = line.strip()
            # Number of Fabric Clients : 8
            if p_clients.match(line):
                match = p_clients.match(line)
                client_count = int(match.group('clients'))
                if not show_wireless_fabric_client_summary_dict.get('number_of_fabric_clients'):
                    show_wireless_fabric_client_summary_dict.update({'number_of_fabric_clients' : client_count})
                continue
            # MAC Address    AP Name                          WLAN State              Protocol Method
            elif p_header.match(line):
                match = p_header.match(line)
                continue
            # -------------------------------------------------------------------------------------------------------------------------
            elif p_delimiter.match(line):
                match = p_delimiter.match(line)
                continue
            # 58bf.ea72.1730 a2-11-cap43                   17   Run                11ac     Dot1x
            elif p_client_info.match(line):
                match = p_client_info.match(line)
                groups = match.groupdict()
                mac_address = groups['mac']
                ap_name = groups['name']
                wlan = int(groups['wlan'])
                state = groups['state'].strip()
                protocol = groups['protocol']
                method = groups['method']
                if not show_wireless_fabric_client_summary_dict.get('mac_address'):
                    show_wireless_fabric_client_summary_dict['mac_address'] = {}
                show_wireless_fabric_client_summary_dict['mac_address'].update({mac_address : {'ap_name' : ap_name, 'wlan' : wlan, 'state' : state, 'protocol' : protocol, 'method' : method}})

        return show_wireless_fabric_client_summary_dict

      
# =================================
# Schema for:
#  * 'show wireless fabric summary'
# =================================
class ShowWirelessFabricSummarySchema(MetaParser):
    """Schema for show wireless fabric summary."""

    schema = {
        "fabric_status": str,
        Optional("control_plane"): {
            Optional("ip_address"): {
                Optional(str): {
                    Optional("name"): str,
                    Optional("key"): str,
                    Optional("status"): str
                }
            }
        },
        Optional("fabric_vnid_mapping"): {
            Optional("l2_vnid"): {
                Optional(int): {
                    Optional("name"): str,
                    Optional("l3_vnid"): int,
                    Optional("control_plane_name"): str,
                    Optional("ip_address"): str,
                    Optional("subnet"): str
                }
            }
        }
    }
    
    
# =================================
# Parser for:
#  * 'show wireless fabric summary'
# =================================
class ShowWirelessFabricSummary(ShowWirelessFabricSummarySchema):
    """Parser for show wireless fabric summary"""

    cli_command = 'show wireless fabric summary'
    
    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
        else:
            output=output
            
        # Fabric Status      : Enabled
        #
        #
        # Control-plane:
        # Name                             IP-address        Key                              Status
        # --------------------------------------------------------------------------------------------
        # default-control-plane            10.10.90.16       099fff                           Up
        # default-control-plane            10.10.90.22       099fff                           Up
        #
        #
        # Fabric VNID Mapping:
        # Name               L2-VNID        L3-VNID        IP Address             Subnet        Control plane name
        # ----------------------------------------------------------------------------------------------------------------------
        # Data                8192           0                                  0.0.0.0            default-control-plane 
        # Guest               8189           0                                  0.0.0.0            default-control-plane 
        # Voice               8191           0                                  0.0.0.0            default-control-plane
        # Fabric_B_INFRA_VN     8188           4097           10.10.40.0          255.255.254.0      default-control-plane
        # Physical_Security     8190           0                                  0.0.0.0            default-control-plane



        # Fabric Status      : Enabled
        p_status = re.compile(r"^Fabric\s+Status\s+:\s+(?P<status>(Enabled|Disabled))$")

        # Control-plane:
        p_control = re.compile(r"^Control-plane:$")

        # Name                             IP-address        Key                              Status
        p_header_1 = re.compile(r"^Name\s+IP-address\s+Key\s+Status$")

        # --------------------------------------------------------------------------------------------
        p_delimiter_1 = re.compile(r"^--------------------------------------------------------------------------------------------$")

        # default-control-plane            10.10.90.11       fa85ff                           Up
        p_cp_client = re.compile(r"^(?P<cp_name>\S+)\s+(?P<cp_ip_address>\S+)\s+(?P<cp_key>\S+)\s+(?P<cp_status>\S+)$")

        # Fabric VNID Mapping:
        p_vnid = re.compile(r"^Fabric\s+VNID\s+Mapping:$")

        # Name               L2-VNID        L3-VNID        IP Address             Subnet        Control plane name
        p_header_2 = re.compile(r"^Name\s+L2-VNID\s+L3-VNID\s+IP\s+Address\s+Subnet\s+Control\s+plane\s+name$")

        # ----------------------------------------------------------------------------------------------------------------------
        p_delimiter_2 = re.compile(r"^----------------------------------------------------------------------------------------------------------------------$")

        # Data                8192           0                                  0.0.0.0            default-control-plane
        p_vnid_mappings = re.compile(r"^(?P<vnid_name>\S+)\s+(?P<vnid_l2>\d+)\s+(?P<vnid_l3>\d+)\s+(?P<vnid_ip_address>\S+)\s+(?P<vnid_subnet>\S+)\s+(?P<vnid_cp_name>\S+)$")

        # Voice               8191           0                                  0.0.0.0            default-control-plane
        p_vnid_mappings_no_ip = re.compile(r"^(?P<vnid_name>\S+)\s+(?P<vnid_l2>\d+)\s+(?P<vnid_l3>\d+)\s+(?P<vnid_subnet>\S+)\s+(?P<vnid_cp_name>\S+)$")


        show_wireless_fabric_summary_dict = {}

        for line in output.splitlines():
            line = line.strip()
            # Fabric Status      : Enabled
            if p_status.match(line):
                match = p_status.match(line)
                status = match.group("status")
                if status == "Enabled":
                    if not show_wireless_fabric_summary_dict.get("fabric_status"):
                        show_wireless_fabric_summary_dict.update({ "fabric_status" : status })
                else:
                    if not show_wireless_fabric_summary_dict.get("fabric_status"):
                        show_wireless_fabric_summary_dict.update({ "fabric_status" : status })
                continue
            # Control-plane:
            elif p_control.match(line):
                continue
            # Name                             IP-address        Key                              Status
            elif p_header_1.match(line):
                continue
            # --------------------------------------------------------------------------------------------
            elif p_delimiter_1.match(line):
                continue
            # default-control-plane            10.10.90.11       fa85ff                           Up
            elif p_cp_client.match(line):
                if not show_wireless_fabric_summary_dict.get("control_plane"):
                    show_wireless_fabric_summary_dict.update({ "control_plane" : { "ip_address" : {} }})
                match = p_cp_client.match(line)
                groups = match.groupdict()
                show_wireless_fabric_summary_dict["control_plane"]["ip_address"].update({ groups["cp_ip_address"] : { "name" : groups["cp_name"], "key": groups["cp_key"], "status" : groups["cp_status"]} })
                continue
            # Fabric VNID Mapping:
            elif p_vnid.match(line):
                if not show_wireless_fabric_summary_dict.get("fabric_vnid_mapping"):
                    show_wireless_fabric_summary_dict.update({ "fabric_vnid_mapping": { "l2_vnid" : {} }})
                continue
            # Name               L2-VNID        L3-VNID        IP Address             Subnet        Control plane name
            elif p_header_2.match(line):
                continue
            # ----------------------------------------------------------------------------------------------------------------------
            elif p_delimiter_2.match(line):
                continue
            # Fabric_B_INFRA_VN     8188           4097           10.10.40.0          255.255.254.0      default-control-plane
            elif p_vnid_mappings.match(line):
                match = p_vnid_mappings.match(line)
                groups = match.groupdict()
                show_wireless_fabric_summary_dict["fabric_vnid_mapping"]["l2_vnid"].update({ int(groups["vnid_l2"]) : { "name": groups["vnid_name"], "l3_vnid": int(groups["vnid_l3"]), "ip_address": groups["vnid_ip_address"], 
                                                                                "subnet": groups["vnid_subnet"], "control_plane_name": groups["vnid_cp_name"]}})
                continue
            # Voice               8191           0                                  0.0.0.0            default-control-plane
            elif p_vnid_mappings_no_ip.match(line):
                match = p_vnid_mappings_no_ip.match(line)
                groups = match.groupdict()
                show_wireless_fabric_summary_dict["fabric_vnid_mapping"]["l2_vnid"].update({ int(groups["vnid_l2"]) : { "name": groups["vnid_name"], "l3_vnid": int(groups["vnid_l3"]), "control_plane_name": groups["vnid_name"] }})
                continue
        
        return show_wireless_fabric_summary_dict


# ===================================
# Schema for:
#  * 'show wireless mobility ap-list'
# ===================================
class ShowWirelessMobilityApListSchema(MetaParser):
    """Schema for show wireless mobility ap-list."""

    schema = {
        "ap_name": {
            Any(): {
                "ap_radio_mac": str,
                "controller_ip": str,
                "learnt_from": str,
            }
        }
    }


# ===================================
# Parser for:
#  * 'show wireless mobility ap-list'
# ===================================
class ShowWirelessMobilityApList(ShowWirelessMobilityApListSchema):
    """Parser for show wireless mobility ap-list"""

    cli_command = "show wireless mobility ap-list"

    def cli(self, output=None):
        if output is None:
            output = self.device.execute(self.cli_command)
        else:
            output = output

        # AP name                           AP radio MAC      Controller IP     Learnt from
        # --------------------------------------------------------------------------------------
        # b80-72-cap30                    58bf.eab3.1420    10.10.7.177      Self
        # b80-81-cap4                     58bf.ea13.62a0    10.10.7.177      Self
        # b80-52-cap6                     58bf.ea13.75e0    10.10.7.177      Self

        # AP name                           AP radio MAC      Controller IP     Learnt from
        ap_header_capture = re.compile(
            r"^AP\s+name\s+AP\s+radio\s+MAC\s+Controller\s+IP\s+Learnt\s+from$"
        )

        # b80-72-cap30                    58bf.eab3.1420    10.10.7.177      Self
        ap_info_capture = re.compile(
            r"^(?P<ap_name>\S+)\s+(?P<ap_radio_mac>\S{4}\.\S{4}\.\S{4})\s+(?P<controller_ip>\d+\.\d+\.\d+\.\d+)\s+(?P<learnt_from>\S+)$"
        )

        ap_info_obj = {}

        for line in output.splitlines():

            line = line.strip()

            if ap_header_capture.match(line):
                continue

            elif ap_info_capture.match(line):
                ap_info_capture_match = ap_info_capture.match(line)
                groups = ap_info_capture_match.groupdict()

                if not ap_info_obj.get("ap_name", {}):
                    ap_info_obj["ap_name"] = {}

                ap_name_dict = {
                    # ap_name: b80-72-cap30
                    groups["ap_name"]: {
                        # radio_mac: 58bf.eab3.1420
                        "ap_radio_mac": groups["ap_radio_mac"],
                        # controller_ip: 10.10.7.177
                        "controller_ip": groups["controller_ip"],
                        # learnt_from: Self
                        "learnt_from": groups["learnt_from"],
                    }
                }

                ap_info_obj["ap_name"].update(ap_name_dict)

        return ap_info_obj