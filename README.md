# jw-tech-challenge

This is the repo for Jeremy Wang's submission for the Relayer Software Engineer Technical Challenge.

## Installation and Requirements

---

To run this you'll need python 3.11+, as well as the API endpoint for an Ethereum Node. You can find a list of publically available Ethereum nodes here: https://ethereumnodes.com/ This project was tested with the Ankr RPC endpoint, but should work with any popular Ethereum node provider such as Infura or Flashbots. For the purposes of this exercise, I've exposed my own Ankr RPC endpoint, and the script will use this as a default if a `--url` is not specified by the user.

Clone the repo:

```
git clone git@github.com:user1303836/jw-tech-challenge.git
```

Install the dependencies with pip (Python 3.11+):

```
pip install -r requirements.txt
```

## Usage

---

Use the following command to select a block range and populate the SQLite db (`--url` is an optional arg):

```
python crawler.py --url=https://your.ethereum.node --start_block=18908800 --end_block=18909050 --get_largest_volume_block
```

## Notes

- For the purposes of this exercise, every time a `--start_block` and `--end_block` is specified, the script will drop all rows from the SQLite db, and repopulate the db with the blocks in the specified range.
- The inputs are by block number, but an alternative approach would be to have inputs as timestamps. The web3 library doesn't have a function to explicitly get blocks by their timestamps (presumably because you would have to have the exact UTC timestamp), but you could implement a binary search to find the block that most closely matches the input start & end timestamps. The binary search would also have to have a function to check for the minimum diff between the current block's timestamp and the input start & end timestamps to determine which block to use for the start & end timestamps. I think something like this would almost certainly make me hit rate limits, so I decided against doing this.
- There is a chance that you get rate limited depending on which node API you're using. This could potentially be resolved by using a library such as polling2, and repeatedly short-polling the API endpoint while ignoring 429s returned by the API. I wanted to keep dependencies to a minimum for the scope of this exercise.
- It's generally the convention that in a larger project, would put ORM db models in its own models module, but this is sort of "small potatoes", and I think it's okay to have the models in the same script.
- I purchased 200 million ANKR RPC credits for $20, so feel free to go crazy and use them if you want. The endpoint is the default one in the script.
