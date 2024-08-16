## Here's a brief description of what relay-mining is:

- Honest validator A sends a query to relay miner B.
- Relay validator B receives the request from miner B and forwards it to honest miner C.
- Honest miner C responds to relay validator B, believing the request is legitimate.
- Relay validator B then sends the response back to relay miner B, who in turn responds to honest validator A.


## One possible solution for subnets to introduce (by const):

- Validators should advertise an Axon with a list of synapses requests they've made over a period of time: [Synapse1 ... SynapseN].
- Miners should periodically query that list of synapses by pulling them from the validator's Axon.
<dl>
    <dd>* If the requests are not available, blacklist the validator.</dd>
    <dd>* If requests sent to a miner are not on that list, blacklist the validator.</dd>
    <dd>* If the timestamps from the requests are incorrect, blacklist the validator.</dd>
</dl>
- Miners should be able to see all the requests they ever receive on these lists. They can also detect if requests from an honest validator are duplicated by the relay validator and sent to them. Even with request obfuscation (where the middle validator alters the internal request), relay miners will have significantly different fingerprints than honest validators in terms of the number of requests to one miner or another. If this is observed, blacklist the validator.

<note>Note:<note> Relay-mining is possible only for validators, as it requires a validator key in the relaying layer (B).

Here's an example PR to prevent relay-mining: [PR by namoray](https://github.com/namoray/vision/pull/77/files)
