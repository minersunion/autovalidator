#### What is Weight Copying?

Weight Copying (WC) is a practice where a dishonest validator copies the weights (or scores) determined by honest validators and submits them as their own without performing the necessary work. There are several types of WC validators:

- **Dumb copy validator**: Simply copies weights from another sophisticated validator.
- **Last epoch copying validator**: Copies weights from the previous epoch.
- **Boosting validator**: Uses historical information to infer correct weights without doing the full work.

#### Importance of Preventing Weight Copying

Weight Copying is harmful because it allows dishonest validators to receive rewards unfairly, thereby reducing the earnings for honest validators and compromising the integrity of the network. The presence of WC validators can lead to:

- **Financial Loss**: Honest validators lose dividends to WC validators.
- **Reduced Trust**: The trustworthiness of the network decreases if validators can cheat without repercussions.
- **Inefficiency**: The system becomes less efficient as resources are unfairly distributed.

#### Commit Reveal

The commit reveal feature changes the way subnet validator weights are recorded to the chain. Instead of submitting weights openly that can be seen immediately, validators upload an encrypted hash of their weights. This hash is decrypted after a set number of blocks.

[Complete documentation](https://docs.bittensor.com/subnets/commit-reveal)
