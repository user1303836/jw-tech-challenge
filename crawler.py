"""block crawler technical challenge for relayer

Usage:
    crawler.py [options] --start_block=<start_block> --end_block=<end_block>
    crawler.py [options] --start_block=<start_block> --end_block=<end_block> --get_largest_volume_block

Options:
    -h --help       Show this screen.
    --url=<url>     Node to connect to [default: https://rpc.ankr.com/eth/e9ee8f6ef6d38ecd2956ed5e4cd3ac0c34c002d99af19150699c64b64e0d21fb].
"""

from docopt import docopt
from web3 import Web3

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, select
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Blocks(Base):
    __tablename__ = "blocks"
    id = Column(Integer, primary_key=True)
    block = Column(Integer, unique=True, nullable=False)
    transactions_count = Column(Integer, nullable=False)


engine = create_engine("sqlite:///blocks.db")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


def write_all_transactions_to_db(w3: Web3, start_block: int, end_block: int) -> None:
    if (
        not (start_block > 0)
        and (end_block < w3.eth.get_block("latest")["number"])
        and (start_block < end_block)
    ):
        raise ValueError(
            "Invalid block range. Start block must be greater than 0 and end block must be less than latest block."
        )
    s = session()
    for b in range(start_block, end_block + 1):
        block_transactions_count = w3.eth.get_block_transaction_count(b)
        print(f"Found block {b} with {block_transactions_count} transactions")
        s.add(
            Blocks(
                block=b,
                transactions_count=block_transactions_count,
            )
        )
    s.commit()


def get_largest_volume_block() -> Blocks:
    s = session()
    stmt = select(Blocks).order_by(Blocks.transactions_count.desc())
    res = s.execute(stmt)
    if not res:
        raise ValueError("No blocks found in db")
    most_transactions_block = res.scalars().first()
    return most_transactions_block


if __name__ == "__main__":
    args = docopt(__doc__)

    default_url = "https://rpc.ankr.com/eth/e9ee8f6ef6d38ecd2956ed5e4cd3ac0c34c002d99af19150699c64b64e0d21fb"
    url = args["--url"] if args["--url"] else default_url
    web3 = Web3(Web3.HTTPProvider(url))

    start_block = int(args["--start_block"])
    end_block = int(args["--end_block"])
    write_all_transactions_to_db(web3, start_block, end_block)

    if args["--get_largest_volume_block"]:
        print("Getting block with largest tx count...")
        block = get_largest_volume_block()
        print(
            f"Block {block.block} has the most txs with {block.transactions_count} txs."
        )
