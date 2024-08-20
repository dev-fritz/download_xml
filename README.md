# Documentation for Client Class
## Overview

The Client class is designed to handle asynchronous downloading of files from given URLs and to compress the downloaded files into a ZIP archive. It uses the aiohttp library for HTTP requests, aiofiles for asynchronous file operations, and asyncio for managing concurrency.
### Methods
#### __init__(self)

Initializes the Client object by creating an instance of aiohttp.ClientSession.
#### async download_notes(self, url: str, number: str | int)

Asynchronously downloads a file from the specified URL and saves it to a local directory.

- Parameters:
    url (str): The URL to download the file from.
    number (str | int): The identifier to use as the filename.

- Behavior:
    Retries downloading the file if the request fails due to a timeout or client error.
    Saves the downloaded file to /tmp/tmp_files0/ with the given number as the filename.

#### async create_download_pool(self, data: dict, filename: str, concurrent_downloads: int = 30)

Asynchronously manages a pool of downloads, ensuring that a specified number of downloads happen concurrently.

- Parameters:
    data (dict): A dictionary containing a list of links. Each link should be a dictionary with url and identifier keys.
    filename (str): The name of the ZIP file to be created.
    concurrent_downloads (int, optional): The maximum number of concurrent downloads. Default is 30.

- Behavior:
    Creates a directory at /tmp/tmp_files0 if it does not exist.
    Downloads files using a semaphore to limit the number of concurrent downloads.
    After all downloads are complete, it calls create_zip to compress the downloaded files into a ZIP archive.

#### @staticmethod async create_zip(path: str, filename: str)

Asynchronously creates a ZIP archive of the files in the specified directory.

- Parameters:
    path (str): The directory containing the files to be zipped.
    filename (str): The name of the ZIP file to be created.

- Behavior:
    Creates a ZIP file at /tmp/ with the specified filename.
    Adds all .xml files from the path directory to the ZIP archive.
    Deletes each file from the directory after adding it to the ZIP archive.

#### async close_session(self)

Asynchronously closes the aiohttp.ClientSession to release resources.

## Usage Example

    import asyncio
    
    async def main():
        client = Client()
        
        data = {
            'links': [
                {'url': 'http://example.com/file1.xml', 'identifier': '1'},
                {'url': 'http://example.com/file2.xml', 'identifier': '2'}
            ]
        }
        await client.create_download_pool(data, 'archive.zip')
        await client.close_session()
    
        asyncio.run(main())
