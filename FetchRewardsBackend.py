from flask import Flask, request, jsonify
import heapq
import datetime
import json

app = Flask(__name__)


# Defining class with attributes of each point dictionary entry
class PointClass:
    def __init__(self, payerDictionary):
        self.payer = payerDictionary['payer']
        self.points = int(payerDictionary['points'])
        self.timestamp = datetime.datetime.strptime(payerDictionary['timestamp'], "%Y-%m-%dT%H:%M:%SZ")

    # Custom sort for heap based on timestamp
    def __lt__(self, other):
        return self.timestamp < other.timestamp


# Defining cache class where we locally sore data and perform operation
class PointCache:
    def __init__(self):
        self.minHeap = []
        heapq.heapify(self.minHeap)

    def addPointEntry(self, pointNode):
        heapq.heappush(self.minHeap, pointNode)

    def getPointEntry(self):
        payerMap = {}
        for entry in self.minHeap:
            if payerMap.get(entry.payer) is None:
                payerMap[entry.payer] = 0
            payerMap[entry.payer] = payerMap[entry.payer] + entry.points
        return payerMap

    def updateCache(self, newCache):
        self.minHeap = newCache
        heapq.heapify(self.minHeap)

    def spendPoints(self, pointsDict):
        result = {}
        points = int(pointsDict['points'])
        tempCache = []
        while len(self.minHeap) and points > 0:
            payerPointNode = heapq.heappop(self.minHeap)
            if payerPointNode.points == 0:
                tempCache.append(payerPointNode)
            elif payerPointNode.points < 0:
                points += 0 - payerPointNode.points
                tempCache.append(payerPointNode)
                if result.get(payerPointNode.payer) is None:
                    result[payerPointNode.payer] = 0
                result[payerPointNode.payer] = result[payerPointNode.payer] + payerPointNode.points * -1
                payerPointNode.points = 0
            else:
                pointRemained = max(0, payerPointNode.points - points)
                if result.get(payerPointNode.payer) is None:
                    result[payerPointNode.payer] = 0
                if pointRemained == 0:
                    result[payerPointNode.payer] = result[payerPointNode.payer] + payerPointNode.points * -1
                    points = points - payerPointNode.points
                    payerPointNode.points = 0
                else:
                    result[payerPointNode.payer] = result[payerPointNode.payer] + points * -1
                    payerPointNode.points = pointRemained
                    points = 0

                tempCache.append(payerPointNode)

        return result, tempCache + self.minHeap


cache = PointCache()

# Route to add point table
@app.route('/addPayerEntry', methods=['Post'])
def addPayerEntry():
    p1 = request.args.get('pointEntry')
    p1 = json.loads(p1)
    cache.addPointEntry(PointClass(p1))
    return jsonify(cache.getPointEntry())


# Route to spend points
@app.route('/spendPoints', methods=['Get'])
def spendPoints():
    p1 = json.loads(request.args.get('spendPoints'))
    pointsDeductionSummary = cache.spendPoints(p1)
    cache.updateCache(pointsDeductionSummary[1])
    result = jsonify(pointsDeductionSummary[0])
    return result

# Route to get updated point table
@app.route('/getPointTable', methods=['Get'])
def getPointTable():
    result = jsonify(cache.getPointEntry())
    print(cache.getPointEntry())
    return result


if __name__ == '__main__':
    app.run(port=8080)
