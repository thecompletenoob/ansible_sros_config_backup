from netmiko import ConnectHandler


def main():
    sr1 = {
        "device_type": "alcatel_sros",
        "host": "SR1",
        "username": "admin",
        "password": "admin",
    }

    sr2 = {
        "device_type": "alcatel_sros",
        "host": "SR2",
        "username": "admin",
        "password": "admin",
    }

    show_cmd = "admin display-config"

    for device in (sr1, sr2):
        hostname_file = f"{device['host']}.txt"
        with ConnectHandler(**device) as conn:
            output = conn.send_command(show_cmd)
            with open(hostname_file, "w+") as f:
                f.write(output)
            # print(output)


if __name__ == "__main__":
    main()
