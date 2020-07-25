# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

prefixForIP = "192.168.1."
link = request.LAN("lan")

for i in range(2):
  if i == 0:
    node = request.XenVM("webserver")
    node.routable_control_ip = "true"
    node.addService(rspec.Execute(shell="/bin/sh",
                              command="sudo apt update"))
    node.addService(rspec.Execute(shell="/bin/sh",
                              command="sudo apt install -y apache2"))
    node.addService(rspec.Execute(shell="/bin/sh",
                              command='sudo ufw allow in "Apache Full"'))
    node.addService(rspec.Execute(shell="/bin/sh",
                              command='sudo systemctl status apache2'))
  else:
    node = request.XenVM("observer")
    
    node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD"
    iface = node.addInterface("if" + str(i))
    iface.component_id = "eth1"
    iface.addAddress(rspec.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
    link.addInterface(iface)

# Print the generated rspec
pc.printRequestRSpec(request)
