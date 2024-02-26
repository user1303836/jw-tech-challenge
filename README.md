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
python crawler.py --url=https://your.ethereum.node --start_block=18908800 --end_block=18909050
```

Use the following command to return the block with the largest volume of ether:

```
python crawler.py --get_largest_volume_block
```

You can also do both steps with one command (`--url` is an optional arg):

```
python crawler.py --url=https://your.ethereum.node --get_largest_volume_block
```

Note: For the purposes of this exercise, every time a `--start_block` and `--end_block` is specified, the script will drop all rows from the SQLite db, and repopulate the db with the blocks in the specified range.
