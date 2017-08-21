Prerequisites to run this script:

1. install azure sdk with command - Linux: "pip install --pre azure"
2. Source the azure credentials

 export AZURE_TENANT_ID={your tenant ID}
 export AZURE_CLIENT_ID={your client ID}
 export AZURE_CLIENT_SECRET={your client secret}
 export AZURE_SUBSCRIPTION_ID={your subscription ID}

3. Edit the parameters in the vm_params.py file.
4. execute : python create_vm.py

Resources creation steps in sequence:

1. Azure Load Balancer Creation using python
2. Azure Availability set creation creation using python
3. Azure Network security group creation using Python
4. Azure Network Interfaces creation using python
5. Azure Virtual Machine creation using Python

Note: These VMs uses managed disk.
