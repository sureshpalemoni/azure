#!/usr/bin/python
from vm_params import *
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials
import os


def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id


credentials, subscription_id = get_credentials()

resource_client = ResourceManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)

resg = resource_client.resource_groups.create_or_update(
    resource_group_name,
    {
        'location': location
    }
)

rg = resg.name

vm_list = [vm1, vm2]


def lb_config(a,b):
	return ("/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/loadBalancers/{}/{}/{}").format(subscription_id, rg, lb_name, a,b)


lb_params = {"location": location,
            "frontend_ip_configurations": [
                {
                    "name": "LoadBalancerFrontEnd",
                    "private_ip_allocation_method": "Dynamic",
                    "subnet": {
                            "id": subnet_name
                    }
                    
                }
            ],
            "backend_address_pools": [
                {
                    "name": "tethabe"
                }
            ],

            "probes": [
                {
                    "name": "testprobe",
                    "protocol": "Tcp",
                    "port": 22,
                    "interval_in_seconds": 5,
                    "number_of_probes": 2
                }
            ],
            "load_balancing_rules": [
                {
                    "name": "testrule",

                    "frontend_ip_configuration": {
                        "id": lb_config("frontendIPConfigurations","loadBalancerFrontEnd")
                    },
                    "frontend_port": 22,
                    "backend_port": 22,
                    "enable_floating_ip": False,
                    "idle_timeout_in_minutes": 4,
                    "protocol": "Tcp",
                    "load_distribution": "Default",
                    "backend_address_pool": {
                        "id": lb_config("backendAddressPools","tethabe")
                    },
                    "probe": {
                        "id": lb_config("probes","testprobe")
                    }
                }
            ]              
            }

network_client.load_balancers.create_or_update(rg, lb_name, lb_params)

AVSET_PARAMETERS={
        'location': location,
        'platform_update_domain_count': 5,
        'platform_fault_domain_count': 2,
        "managed": "true"
        }

#import pdb;pdb.set_trace()
avset = compute_client.availability_sets.create_or_update(rg, avset_name, AVSET_PARAMETERS)

nsg_params={"location": location,
            "security_rules": [{
                "name": "ssh",
                "protocol": "TCP",
                "source_port_range": "*",
                "destination_port_range": "22",
                "source_address_prefix": "*",
                "destination_address_prefix": "*",
                "access": "Allow",
                "priority": 100,
                "direction": "Inbound"
            }]
            }


network_client.network_security_groups.create_or_update(rg, "default-nsg-ssh", nsg_params)

nif_params={"location": location,
            "network_security_group": {
                "id": ("/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/networkSecurityGroups/default-nsg-ssh").format(subscription_id,rg)
            },
            "ip_configurations": [{"name": "ipconfig-1",
                                  "private_ip_allocation_method": "Dynamic",
                                  "subnet": {"id": subnet_name},
                                  "load_balancer_backend_address_pools": [
                                      {
                                        "id": lb_config("backendAddressPools","tethabe")
                                      }
                                   ]      
                                 }]
            }


def nif(vm, nic):
	netint = vm+nic
	netinf = network_client.network_interfaces.create_or_update(rg, netint, nif_params)
	return ("/subscriptions/{}/resourceGroups/{}/providers/Microsoft.Network/networkInterfaces/{}").format(subscription_id,rg, netint)

for i in vm_list:
	VM_PARAMETERS={
	        'location': location,
	        'availability_set': {
	            "id": avset.id
	        },
	        'os_profile': {
	            'computer_name': i,
	            'admin_username': admin_username,
	            'admin_password': admin_password
	        },
	        'hardware_profile': {
	            'vm_size': 'Standard_DS2_v2'
	        },
	        'storage_profile': {
	            'image_reference': {
	                'publisher': 'Canonical',
	                'offer': 'UbuntuServer',
	                'sku': '16.04.0-LTS',
	                'version': 'latest'
	            },
	        },
	        'network_profile': {
	            'network_interfaces': [{
	                "id": nif(i, "_nic")
	            }]
	        },
	    }

	def create_vm():
	    compute_client.virtual_machines.create_or_update(
	        rg, i , VM_PARAMETERS)

	create_vm()
