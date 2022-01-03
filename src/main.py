import os
import dotenv
from uploader import Uploader
from time import sleep
import json

def main():
    # Initialize env variables
    dotenv.load_dotenv()
    seed_phrase = os.getenv("SEED_PHRASE")
    password = os.getenv("PASSWORD")

    description = "TEST DESCRIPTION"
    external_link = "https://www.google.com/"

    # Initialize
    uploader = Uploader()
    uploader.connect_metamask(seed_phrase, password)

    # Connect to the specified network - ENTER THE APPROPRIATE NETWORK
    NETWORK_RPC = "https://ropsten.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161"
    CHAIN_ID = 3
    uploader.set_network(NETWORK_RPC, CHAIN_ID) # Custom network to add to Metamask
    uploader.open_metamask()
    # uploader.set_network("", 0, 1) # Use a default network provided by Metamask

    # Connect to OpenSea
    uploader.connect_opensea(test=False)
    COLLECTION_URL = "https://opensea.io/collection/bananarepublican123"
    uploader.set_collection_url(COLLECTION_URL)

    # Upload NFT data in 'metadata.json' to OpenSea - MODIFY THE UPLOAD FUNCTION AND THE METADATA TO CONTAIN ANY ADDITIONAL METADATA
    metadata = json.load(open(os.path.join(os.getcwd(), "data", "metadata.json")))
    first_upload = True
    for i, data in enumerate(metadata):
        try:
            uploader.upload(os.path.join( os.getcwd(), "data", "assets", data["asset"]), data["name"], description, external_link, data["properties"])
            if first_upload:
                uploader.sign_transaction()
                first_upload = False 
        except Exception as e:
            print(f"Failed to upload NFT {i} '{data['name']}' for reason '{e}'.")

    # Close
    uploader.close()

# Run main if this file is run directly
if __name__ == "__main__":
    main()
