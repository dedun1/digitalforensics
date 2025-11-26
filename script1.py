import csv
import os

EXPORT_DIR = r"D:\eyadforensics\exports"

REG_DIR = r"D:\eyadforensics\exports"

REG_HIVES = ["sam.csv", "system.csv", "software.csv"]

FILES = {
    "apps": "installedapps.csv",
    "accounts": "useraccounts.csv",
    "usb": "usbdeviceattached.csv",
    "run": "runhistory.csv"
}

def read_csv(name):
    path = os.path.join(EXPORT_DIR, FILES[name])
    if not os.path.exists(path):
        print(f"[!] Missing file: {path}")
        return []
    with open(path, encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f))

#Check for registry hive files WITH DEBUG PATH PRINTING
def check_registry_files():
    print("\nRegistry Hive Check")
    for hive in REG_HIVES:
        path = os.path.join(REG_DIR, hive)

        # DEBUG: print exact path being checked
        print(f"Checking: {path}")

        if os.path.exists(path):
            print(f"[✓] {hive} found")
        else:
            print(f"[!] {hive} NOT found")

def showinstalledapps():
    print("\nInstalled Applications")
    apps = read_csv("apps")
    print(f"Total: {len(apps)}")
    for a in apps[:200]:
        print(f"- {a.get('Program Name')} | Date/Time: {a.get('Date/Time')}")

def showaccounts():
    print("\nUser Accounts")
    accounts = read_csv("accounts")
    print(f"Total: {len(accounts)}")
    for acc in accounts:
        print(f"- {acc.get('Login Name')} | Created: {acc.get('Creation Time')}")

def showusb():
    print("\nUSB History")
    rows = read_csv("usb")
    print(f"Total: {len(rows)}\n")
    for row in rows:
        make  = row.get("Device Make", "Unknown")
        model = row.get("Device Model", "Unknown")
        dev_id = row.get("Device ID", "Unknown")
        date = row.get("Date/Time", "Unknown")
        print(f"- {make} {model} | ID: {dev_id} | Date: {date}")

def programhistory():
    print("\nProgram History")
    run = read_csv("run")
    print(f"Total: {len(run)}")
    for r in run[:10]:
        print(f"- {r.get('Program Name')} | Last Run: {r.get('Date/Time')}")

def main():
    print("Scan Script\n")
    check_registry_files()    
    showinstalledapps()
    showaccounts()
    showusb()
    programhistory()

if __name__ == "__main__":
    main()
