import numpy as np
import pandas as pd

labelData = '../../Datasets/Real/300sLablingSet.csv'
rawData = '../../Datasets/Real/300sTrainingData.csv'

labelSet = pd.read_csv(labelData, usecols = ['Traffic Application'])
pktLength = pd.read_csv(rawData, usecols = ['Length'])
arrTime = pd.read_csv(rawData, usecols = ['Time'])
scrIpRaw = pd.read_csv(rawData, usecols = ['Source'])
destIpRaw = pd.read_csv(rawData, usecols = ['Destination'])
protName = pd.read_csv(rawData, usecols = ['Protocol'])
scrIp = pd.read_csv(labelData, usecols = ['Source IP'])
destIp = pd.read_csv(labelData, usecols = ['Destination IP'])

labelSet = np.array(labelSet)
pktLength = np.array(pktLength, dtype = float)
arrTime = np.array(arrTime, dtype = float)
scrIpRaw = np.array(scrIpRaw)
scrIp = np.array(scrIp)
destIpRaw = np.array(destIpRaw)
destIp = np.array(destIp)
protName = np.array(protName)

totalNumFlows = len(labelSet)

gIndx = np.where((labelSet == 'google') | (labelSet == 'gmail') | (labelSet == 'googlemap') | (labelSet == 'googledrive'))[0]
ytIndx = np.where((labelSet == 'youtube') | (labelSet == 'youtube_web'))[0]
nfIndx = np.where(labelSet == 'netflix')[0]
tIndx = np.where(labelSet == 'bittorrent')[0]
fbIndx = np.where(labelSet == 'facebook')[0]
htIndx = np.where(labelSet == 'http')[0]
sslIndx = np.where(labelSet == 'ssl')[0]

# Make labling simple
labelSet[gIndx] = 'google'
labelSet[ytIndx] = 'youtube'

gPerc = (len(gIndx) / totalNumFlows) * 100
ytPerc = (len(ytIndx) / totalNumFlows) * 100
nfPerc = (len(nfIndx) / totalNumFlows) * 100
tPerc = (len(tIndx) / totalNumFlows) * 100
fbPerc = (len(fbIndx) / totalNumFlows) * 100
htPerc = (len(htIndx) / totalNumFlows) * 100
sslPerc = (len(sslIndx) / totalNumFlows) * 100
pthPerc = ((totalNumFlows - (len(gIndx) + len(ytIndx) + len(nfIndx) + len(tIndx) + len(fbIndx) + len(htIndx) + len(sslIndx))) / totalNumFlows) * 100

print("\n========================================")
print("\n%.2f%% of flows are Google Related" %gPerc)
print("\n%.2f%% of flows are Youtube" %ytPerc)
print("\n%.2f%% of flows are NetFlix" %nfPerc)
print("\n%.2f%% of flows are Torrent" %tPerc)
print("\n%.2f%% of flows are Facebook" %fbPerc)
print("\n%.2f%% of flows are HTTP" %htPerc)
print("\n%.2f%% of flows are SSL" %sslPerc)
print("\n%.2f%% of flows are Other" %sslPerc)
print("\n========================================")

# Create training data
trainingData = np.zeros((len(scrIpRaw), 6), dtype = object)
trainingData[:, 0] = scrIpRaw[:, 0]       # First column is Source IP
trainingData[:, 1] = destIpRaw[:, 0]      # Second column is Destination IP
trainingData[:, 2] = arrTime[:, 0]        # Third column is Packet Arrival Time
trainingData[:, 3] = pktLength[:, 0]      # Fourth column is Packet Length
trainingData[:, 4] = protName[:, 0]       # Fifth column is Protocol Name    
trainingData[:, 5] = 'other'              # Sixth column is Traffic Label which is other by default

# Extract all the flows
for i in range(0, len(scrIp)):
    flowScrIp = scrIp[i]
    flowDestIp = destIp[i]

    scrTempIndx = np.where(scrIpRaw == flowScrIp)[0]   # Find all A's
    destTempIndx = np.where(destIpRaw == flowDestIp)[0]   # Find all B's
    
    # Find all indexes for this half flow from A to B
    flowInd = np.intersect1d(scrTempIndx, destTempIndx)
    
    trainingData[flowInd, 5] = labelSet[i]  # Fifth column is Traffic Label


gFlowVol = sum(pktLength[np.where(trainingData[:, 5] == 'google')[0]])
ytFlowVol = sum(pktLength[np.where(trainingData[:, 5] == 'youtube')[0]])
nfFlowVol = sum(pktLength[np.where(trainingData[:, 5] == 'netflix')[0]])
tFlowVol = sum(pktLength[np.where(trainingData[:, 5] == 'bittorrent')[0]])
fbFlowVol = sum(pktLength[np.where(trainingData[:, 5] == 'facebook')[0]])
htFlowVol = sum(pktLength[np.where(trainingData[:, 5] == 'http')[0]])
sslFlowVol = sum(pktLength[np.where(trainingData[:, 5] == 'ssl')[0]])

#trainingData = pd.DataFrame(trainingData)
#columns = ['Source', 'Destination', 'Time', 'Length', 'Protocol', 'Application']
#trainingData.to_csv("../../Datasets/Real/trainingData.csv", index_label = False, header = columns, index = False)       

totalTrVol = sum(pktLength)

othFlowVol = totalTrVol - (gFlowVol + ytFlowVol + nfFlowVol + tFlowVol + fbFlowVol + htFlowVol + sslFlowVol)

print("\n%.2f%% of traffic is Google Related" %(gFlowVol * 100 /totalTrVol))
print("\n%.2f%% of traffic is Youtube" %(ytFlowVol * 100 /totalTrVol))
print("\n%.2f%% of traffic is NetFlix" %(nfFlowVol * 100 /totalTrVol))
print("\n%.2f%% of traffic is Torrent" %(tFlowVol * 100 /totalTrVol))
print("\n%.2f%% of traffic is Facebook" %(fbFlowVol * 100 /totalTrVol))
print("\n%.2f%% of traffic is HTTP" %(htFlowVol * 100 /totalTrVol))
print("\n%.2f%% of traffic is SSL" %(sslFlowVol * 100 /totalTrVol))
print("\n%.2f%% of traffic is Other" %(othFlowVol * 100 /totalTrVol))
print("\n========================================")