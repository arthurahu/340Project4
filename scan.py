import sys
import json
import subprocess
import time


def scan(self, url):
    self.out[url] = {}

    self.out[url]["scan_time"] = time.time()

    return


def main(self):
    if len(sys.argv) != 3:
        sys.stderr.write("number of args")
        return -1

    file_in = sys.argv[1]
    file_out = sys.argv[2]

    self.out = {}

    with open(file_in, "r") as f:
        for url in f:
            scan(url)

    with open(file_out, "w") as f:
        json.dump(self.out, f, sort_keys=True, indent=4)

    return


if __name__ == '__main__':
    main()
