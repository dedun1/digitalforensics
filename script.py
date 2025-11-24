import os
import struct

# This is the location of the disk image
IMAGE_PATH = r"D:\eyadforensics\evidence\cwimage.dd"

# Each sector in the disk is 512 bytes
SECTOR_SIZE = 512

# Read the first 512 bytes of the disk (this is the MBR area)
def read_mbr(path):
    with open(path, "rb") as f:
        return f.read(SECTOR_SIZE)

# This function looks inside the MBR and tries to find partitions
def get_partitions(mbr):
    partitions = []

    # The partition table starts at byte 446 in the MBR
    start_location = 446

    # There are 4 possible partition entries, each 16 bytes
    for i in range(4):
        entry = mbr[start_location + i*16 : start_location + (i+1)*16]

        part_type = entry[4]  # This tells us what type of partition it is
        first_sector = struct.unpack("<I", entry[8:12])[0]
        total_sectors = struct.unpack("<I", entry[12:16])[0]

        # Skip empty partition entries
        if part_type == 0 or total_sectors == 0:
            continue

        size_gb = (total_sectors * SECTOR_SIZE) / (1024**3)

        partitions.append({
            "number": i+1,
            "type": hex(part_type),
            "start_sector": first_sector,
            "total_sectors": total_sectors,
            "size_gb": size_gb
        })

    return partitions

def main():
    # Check the image exists
    if not os.path.exists(IMAGE_PATH):
        print("Disk image not found.")
        return

    print("Reading MBR from disk image...\n")
    
    mbr = read_mbr(IMAGE_PATH)
    parts = get_partitions(mbr)

    if not parts:
        print("No partitions found in the MBR.")
        return

    # Print the info about each partition
    for p in parts:
        print(f"Partition {p['number']}:")
        print(f"  Type:          {p['type']}")
        print(f"  Start sector:  {p['start_sector']}")
        print(f"  Total sectors: {p['total_sectors']}")
        print(f"  Size (GB):     {p['size_gb']:.2f} GB\n")

if __name__ == "__main__":
    main()
