import subprocess
from pathlib import Path
from time import sleep

stateFile = Path("experiment.state")

MAX_ITRS = 3
arrivalRates = [0.25, 0.3, 1, 10, 100, 1000]

btch = 0
itr = 0
if(stateFile.exists()):
    state = stateFile.read_text().split(",")
    btch = int(state[0])
    itr = int(state[1])

print(f"Arrival rate = {arrivalRates[btch]}, Iteration = {itr}\n")

if(btch == 0 and itr == 0):
    subprocess.run(["vagrant", "up"], check=True)
else:
    #Cleanup
    subprocess.run(["vagrant", "ssh", "starteventpublisher", "-c", "sudo docker rm -f smartfactoryepcsm"], check=True)
    subprocess.run(["vagrant", "ssh", "infra", "-c", "cd /opt/smartfactory/infra && sudo env ETCD_IP=192.168.59.2 docker compose down"])
    subprocess.run(["vagrant", "ssh", "service", "-c", "sudo docker rm -f smartfactoryservicecsm"], check=True)
    if(itr == 0):
        subprocess.run(["vagrant", "ssh", "collector", "-c", "sudo docker rm -f smartfactorycollector"], check=True)

    #Resetting
    subprocess.run(["vagrant", "ssh", "infra", "-c", "cd /opt/smartfactory/infra && sudo env ETCD_IP=192.168.59.2 docker compose up -d"])
    sleep(1.0)
    if(itr == 0):
        subprocess.run(["vagrant", "ssh", "collector", "-c", f"sudo docker run -d --name smartfactorycollector --network host -v /vagrant/metrics:/collector/metrics:rw -e ZENOH_CONFIG_URI=/collector/zenoh/zenoh.json5 -e RUN_ID={btch} smartfactorycollector:csml"], check=True)
    subprocess.run(["vagrant", "ssh", "service", "-c", f"sudo docker run -d --name smartfactoryservicecsm --restart unless-stopped --network host -e ZENOH_CONFIG_URI=/service/zenoh/zenohSrv.json5 smartfactoryservice:csm"], check=True)
    subprocess.run(["vagrant", "provision", "monitor"], check=True)
    subprocess.run(["vagrant", "provision", "messageprocessor"], check=True)
    subprocess.run(["vagrant", "provision", "jobcontroller"], check=True)
    subprocess.run(["vagrant", "provision", "arm"], check=True)
    subprocess.run(["vagrant", "provision", "belt"], check=True)
    subprocess.run(["vagrant", "provision", "assemblycontroller"], check=True)
    subprocess.run(["vagrant", "ssh", "starteventpublisher", "-c", f"sudo docker run -d --name smartfactoryepcsm --network host -e ZENOH_CONFIG_URI=/publisher/zenoh/zenohSrv.json5 -e PART_ARRIVAl_RATE_PER_SEC={arrivalRates[btch]} -e PUBLISH_START_DELAY=60000 smartfactoryep:csm"], check=True)

#Updating state
itr = (itr+1) if(itr < (MAX_ITRS-1)) else 0
btch = min(btch + 1, len(arrivalRates)-1) if(itr == 0) else btch
stateFile.write_text(f"{btch},{itr}")