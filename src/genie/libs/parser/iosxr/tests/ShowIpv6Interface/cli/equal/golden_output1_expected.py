expected_output = {
    "GigabitEthernet0/0/0/0": {
        "enabled": True,
        "oper_status": "up",
        "vrf": "default",
        "int_status": "up",
        "ipv6": {
            "incomplete_protocol_adj": "0",
            "complete_glean_adj": "0",
            "dropped_protocol_req": "0",
            "dropped_glean_req": "0",
            "nd_router_adv": "1800",
            "complete_protocol_adj": "0",
            "icmp_unreachables": "enabled",
            "ipv6_link_local": "fe80::250:56ff:fe8d:8d58",
            "incomplete_glean_adj": "0",
            "nd_adv_duration": "160-240",
            "ipv6_groups": [
                "ff02::1:ff00:1",
                "ff02::1:ff8d:8d58",
                "ff02::2",
                "ff02::1",
            ],
            "nd_adv_retrans_int": "0",
            "nd_cache_limit": "1000000000",
            "stateless_autoconfig": True,
            "icmp_redirects": "disabled",
            "dad_attempts": "1",
            "ipv6_mtu": "1514",
            "ipv6_mtu_available": "1500",
            "2001:112::1/64": {
                "ipv6_subnet": "2001:112::",
                "ipv6_prefix_length": "64",
                "ipv6": "2001:112::1",
            },
            "nd_dad": "enabled",
            "nd_reachable_time": "0",
            "table_id": "0xe0800000",
        },
        "vrf_id": "0x60000000",
        "ipv6_enabled": True,
    },
}