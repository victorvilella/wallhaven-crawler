from threadDownloader import Downloader
import sys


if __name__ == "__main__":
    print("Starting")
    threads = []

    # Argv 1 = Query string
    # Argv 2 = Download location directory
    t = Downloader(sys.argv[1], sys.argv[2])
    t.start()
    threads.append(t)