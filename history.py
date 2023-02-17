DEFAULT_FILE_LOCATION = "/var/log/zypp/history"
DISCARDED = ["#", "zypper", "yast"]

try:
    with open(DEFAULT_FILE_LOCATION) as f:
        lines = f.readlines()
        
        # eat lines with discarded chars
        lines = [line for line in lines if not any(c in line for c in DISCARDED)]

        # eat lines with discarded words
        lines = [line for line in lines if not any(word.lower() in DISCARDED for word in line)]

        for line in lines:
            elems = line.split('|')
            
            entry_date = elems[0]
            entry_action = elems[1]
            entry_package = elems[2]
            entry_version = elems[3]
            # entry_arch = elems[4]

            print(f"{entry_date}\t{entry_action}\t\t{entry_package} ({entry_version})")

except PermissionError:
    print(f"Insufficient privileges to access zypper history file ({DEFAULT_FILE_LOCATION}). Are you root?")
