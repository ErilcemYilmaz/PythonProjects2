import csv
import ipaddress
import json

"""
    This Script can be used to:
        - calculate CIDR IP addresses
        - generate white/- blacklists files for IP's as JSON.
        
        
    USAGE NOTE: 
    
        - The file containing the IP addresses must be a CSV file with delimiter ";" (otherwise Script has to be adjusted).
        - The data must be in the following Cloumns (otherwise Script has to be adjusted): 
        - Column 1 = start_ip - Column 2 = end_ip - Column 6 = CIDR IP address - Column 7 = expirationDate - Column 8 = description
        
"""


def calculate_CIDR(start_ip, end_ip):
    """
    Calculates the CIDR from the given start IP to end IP address

    Args:
        start_ip (int): start IP address
        end_ip (int): end IP address

    Returns:
        str: returns a string representation of the IP address with the calcualted Subnet
    """
    start_ip_int = int(ipaddress.ip_address(start_ip))
    end_ip_int = int(ipaddress.ip_address(end_ip))

    # Calculate the XOR of the two IP addresses to find the difference
    xor_result = start_ip_int ^ end_ip_int

    # Count the number of leading zeros in the XOR result
    cidr = 32 - xor_result.bit_length()

    subnet = ipaddress.ip_network(start_ip + "/" + str(cidr), strict=False)
    return str(subnet)


def CIDR_from_csv(csv_file):
    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader)  # Skip header
        for row in csv_reader:
            start_ip, end_ip = row[0], row[1]
            subnet = calculate_CIDR(start_ip, end_ip)
            print(subnet)


def csv_to_json(csv_file, json_file):
    """
    creats a JSON file whit given entries from a CSV file

    Args:
        csv_file (path): path to csv file containing the IP's
        json_file (path): output path of the json file
    """
    whitelist = []
    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file, delimiter=";")
        next(csv_reader)  # Skip header
        for row in csv_reader:
            ip, expirationDate, description = row[6], row[7], row[8]
            whitelist_entry = {
                "ip": ip,
                "expirationDate": expirationDate,
                "description": description,
            }
            whitelist.append(whitelist_entry)

    with open(json_file, "w") as file:
        json.dump(whitelist, file, indent=4)


# Example usage:
csv_file = r"C:\Users\ery\Desktop\Whitelist_IP.csv"
json_file = r"C:\Users\ery\Desktop\IP_Whitelist.json"

csv_to_json(csv_file, json_file)
CIDR_from_csv(csv_file)
