import subprocess
from pathlib import Path

stateFile = Path("experiment.state")

MAX_ITRS = 5
arrivalRates = [0.25, 0.3, 1, 10, 1000, 10000, 50000, 100000, 500000 , 1000000]

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
    subprocess.run(["vagrant", "ssh", "service", "-c", f"cd /opt/smartfactoryservice/docker && sudo env APP_ID=service-app APP_PORT=6000 DAPR_VOL=/opt/smartfactoryservice/dapr RUNTIME_IP=192.168.56.2 DAPR_APP_IMG=smartfactoryservice:dapr PUBLISH_START_DELAY=90000 PART_ARRIVAl_RATE_PER_SEC={arrivalRates[btch]} docker compose down"], check=True)
    if(itr == 0):
        subprocess.run(["vagrant", "ssh", "collector", "-c", f"cd /opt/smartfactorycollector/docker && sudo env APP_ID=smartfactorycollector APP_PORT=8081 RUNTIME_IP=192.168.56.2 DAPR_VOL=/opt/smartfactorycollector/dapr DAPR_APP_IMG=smartfactorycollector:dapr COLLECTOR_RUN_ID={btch} docker compose down"], check=True)

    #Resetting
    subprocess.run(["vagrant", "provision", "dapr"], check=True)
    if(itr == 0):
        subprocess.run(["vagrant", "ssh", "collector", "-c", f"cd /opt/smartfactorycollector/docker && sudo env APP_ID=smartfactorycollector APP_PORT=8081 RUNTIME_IP=192.168.56.2 DAPR_VOL=/opt/smartfactorycollector/dapr DAPR_APP_IMG=smartfactorycollector:dapr COLLECTOR_RUN_ID={btch} docker compose up -d"], check=True)
    subprocess.run(["vagrant", "ssh", "service", "-c", f"sudo cp -r /vagrant/service/. /opt/smartfactoryservice/docker && cd /opt/smartfactoryservice/docker && sudo docker build -t smartfactoryservice:dapr . && sudo env APP_ID=service-app APP_PORT=6000 DAPR_VOL=/opt/smartfactoryservice/dapr RUNTIME_IP=192.168.56.2 DAPR_APP_IMG=smartfactoryservice:dapr PUBLISH_START_DELAY=90000 PART_ARRIVAl_RATE_PER_SEC={arrivalRates[btch]} docker compose up -d"],check=True)
    subprocess.run(["vagrant", "provision", "monitor"], check=True)
    subprocess.run(["vagrant", "provision", "messageprocessor"], check=True)
    subprocess.run(["vagrant", "provision", "jobcontroller"], check=True)
    subprocess.run(["vagrant", "provision", "arm"], check=True)
    subprocess.run(["vagrant", "provision", "belt"], check=True)
    subprocess.run(["vagrant", "provision", "assemblycontroller"], check=True)

#Updating state
itr = (itr+1) if(itr < (MAX_ITRS-1)) else 0
btch = min(btch + 1, len(arrivalRates)-1) if(itr == 0) else btch
stateFile.write_text(f"{btch},{itr}")
