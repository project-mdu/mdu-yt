import aiohttp
import asyncio
import os
import argparse
import ssl
import logging
from urllib.parse import urlparse
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn, SpinnerColumn
from rich.console import Console
from rich.panel import Panel
from rich.logging import RichHandler

console = Console()

# Set up logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, console=console)]
)

log = logging.getLogger("rich")

async def download_chunk(session, url, start, end, filename, chunk_number, progress, task):
    headers = {'Range': f'bytes={start}-{end}'}
    chunk_size = end - start + 1
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            async with session.get(url, headers=headers) as response:
                with open(f"{filename}.part{chunk_number}", "wb") as f:
                    downloaded = 0
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress.update(task, advance=len(chunk))
            log.info(f"Chunk {chunk_number} downloaded successfully")
            return
        except Exception as e:
            if attempt < max_retries - 1:
                log.warning(f"Error downloading chunk {chunk_number}: {str(e)}. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                log.error(f"Failed to download chunk {chunk_number} after {max_retries} attempts: {str(e)}")
                raise

def combine_chunks(filename, split_file, chunk_size, file_size, file_allocation):
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Combining chunks", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    ) as progress:
        combine_task = progress.add_task("Combining", total=file_size)
        with open(filename, "r+b" if file_allocation == 'prealloc' else "wb") as outfile:
            for i in range(split_file):
                chunk_file = f"{filename}.part{i}"
                with open(chunk_file, "rb") as infile:
                    outfile.seek(i * chunk_size)
                    while True:
                        data = infile.read(8192)
                        if not data:
                            break
                        outfile.write(data)
                        progress.update(combine_task, advance=len(data))
                os.remove(chunk_file)
                log.info(f"Chunk {i} combined and removed")

async def parallel_download(url, num_connections=16, split_file=16, file_allocation='prealloc', check_certificate='auto', output_directory=None, output_filename=None):
    if output_directory:
        download_dir = os.path.abspath(output_directory)
    else:
        download_dir = os.path.expanduser("~/Downloads")
    os.makedirs(download_dir, exist_ok=True)

    log.info(f"Starting download from {url}")
    log.debug(f"Using {num_connections} connections")
    log.debug(f"Splitting file into {split_file} parts")
    log.debug(f"File allocation method: {file_allocation}")
    log.debug(f"Certificate check: {check_certificate}")
    log.debug(f"Download directory: {download_dir}")

    ssl_context = ssl.create_default_context()
    if check_certificate == 'no':
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    try:
        with console.status("[bold green]Preparing download...", spinner="dots"):
            async with aiohttp.ClientSession() as session:
                async with session.head(url, ssl=ssl_context) as response:
                    file_size = int(response.headers.get('Content-Length', 0))
                    if not output_filename:
                        output_filename = os.path.basename(urlparse(url).path)
                        if not output_filename:
                            output_filename = 'downloaded_file'

                filename = os.path.join(download_dir, output_filename)
                log.info(f"Output filename: {filename}")

                if file_size == 0:
                    log.warning("Unable to determine file size. Downloading as a single file.")
                    async with session.get(url, ssl=ssl_context) as response:
                        with open(filename, "wb") as f:
                            with Progress(
                                SpinnerColumn(),
                                TextColumn("[bold blue]Downloading", justify="right"),
                                BarColumn(bar_width=None),
                                "[progress.percentage]{task.percentage:>3.1f}%",
                                "•",
                                DownloadColumn(),
                                "•",
                                TransferSpeedColumn(),
                                "•",
                                TimeRemainingColumn(),
                            ) as progress:
                                task = progress.add_task("[cyan]Downloading...", total=float('inf'))
                                async for chunk in response.content.iter_chunked(8192):
                                    f.write(chunk)
                                    progress.update(task, advance=len(chunk))
                    log.info(f"Download completed: {filename}")
                    return

                chunk_size = file_size // split_file

                log.debug(f"File size: {file_size} bytes")
                log.debug(f"Chunk size: {chunk_size} bytes")

                if file_allocation == 'prealloc':
                    with open(filename, "wb") as f:
                        f.seek(file_size - 1)
                        f.write(b'\0')

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        ) as progress:
            main_task = progress.add_task("download", filename=filename, total=file_size)
            tasks = []
            for i in range(split_file):
                start = i * chunk_size
                end = start + chunk_size - 1 if i < split_file - 1 else file_size - 1
                task = progress.add_task(f"Chunk {i+1}", total=end-start+1, visible=False)
                download_task = asyncio.create_task(download_chunk(session, url, start, end, filename, i, progress, main_task))
                tasks.append(download_task)

            await asyncio.gather(*tasks)

        log.info("All chunks downloaded. Combining chunks...")

        combine_chunks(filename, split_file, chunk_size, file_size, file_allocation)

        log.info(f"Download completed: {filename}")
        return "complete"
    except Exception as e:
        log.exception(f"Error occurred: {str(e)}")
        return "error"

async def download_multiple(urls, num_connections, split_file, file_allocation, check_certificate, output_directory):
    for url in urls:
        await parallel_download(url, num_connections, split_file, file_allocation, check_certificate, output_directory)

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced Parallel Downloader with Multi-URL Support")
    parser.add_argument("urls", nargs='*', help="URLs to download")
    parser.add_argument("-i", "--input-file", help="Text file containing URLs to download")
    parser.add_argument("-c", "--connections", type=int, default=16, help="Number of connections (default: 16)")
    parser.add_argument("-x", "--max-connections", type=int, default=16, help="Maximum number of connections (default: 16, max: 8192)")
    parser.add_argument("-s", "--split-file", type=int, default=16, help="Number of parts to split the file into (default: 16)")
    parser.add_argument("--file-allocation", choices=['none', 'prealloc', 'falloc'], default='prealloc', help="File allocation method (default: prealloc)")
    parser.add_argument("--check-certificate", choices=['auto', 'yes', 'no'], default='auto', help="Whether to check the server certificate (default: auto)")
    parser.add_argument("-d", "--output-directory", help="Output directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Set logging level based on verbosity and debug flag
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    # Collect URLs from both command line arguments and input file
    urls = args.urls
    if args.input_file:
        urls.extend(read_urls_from_file(args.input_file))

    if not urls:
        log.error("No URLs provided. Please specify URLs or use an input file.")
        exit(1)

    # Ensure max_connections is within the allowed range
    args.max_connections = max(1, min(args.max_connections, 8192))
    
    # Use the lower of connections and max_connections
    num_connections = min(args.connections, args.max_connections)

    console.print(Panel("Enhanced Parallel Downloader with Multi-URL Support", title="Welcome", border_style="bold magenta"))
    log.info(f"Starting downloads with {num_connections} connections per file")
    
    asyncio.run(download_multiple(
        urls,
        num_connections, 
        args.split_file, 
        args.file_allocation, 
        args.check_certificate,
        args.output_directory
    ))