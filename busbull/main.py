import argparse
from . import bus_loader

def main():
    parser = argparse.ArgumentParser(description='Warsaw public transport data gatherer.')
    parser.add_argument(
            '--url',
            dest='url',
            help='API url', 
            default='https://api.um.warszawa.pl/api/action/busestrams_get/?')
    parser.add_argument(
            '--sleep-time',
            dest='sleep_time',
            help='Time between fetches (in seconds)',
            default='10')
    parser.add_argument(
            '--transport-type',
            dest='transport_type',
            help='Type of public transport to fetch. 1=buses, 2=trams',
            choices=['1', '2'],
            default='1')
    parser.add_argument(
            '--apikey',
            dest='apikey',
            help='API key for authentication',
            default="b632c1db-f62b-47ae-8bce-e78576e9aab8")
    parser.add_argument(
            '--resource-id',
            dest='resource_id',
            help='id of resource to fetch',
            default="f2e5503e-927d-4ad3-9500-4ab9e55deb59")
    parser.add_argument(
            '--line',
            dest='line',
            help='Limit data to chosen line')
    parser.add_argument(
            '--brigade',
            dest='brigade',
            help='Limit dato to chosen brigade')
    args = parser.parse_args()

    file_base_name = input("How should I name file with gathered data?\n")
    time_in_minutes = input("For how long do you want to gather data? (in minutes)\n")
    time_in_minutes = int(time_in_minutes)
    sleep_time = int(args.sleep_time)

    if time_in_minutes <= 0:
        print("Gathering data time must be a positive number.")
        return
    if sleep_time < 0:
        print("Sleep time can not be negative.")
        return

    fetch_config = {
            "resource_id": args.resource_id,
            "apikey": args.apikey,
            "type": args.transport_type,
    }

    if args.line:
        fetch_config["line"] = args.line
    if args.brigade:
        fetch_config["brigade"] = args.brigade

    bus_loader._start_gathering_data(
            fetch_config=fetch_config,
            data_file=file_base_name+".txt",
            error_file=file_base_name+"_logs.txt",
            tics=time_in_minutes*60//sleep_time,
            url=args.url,
            sleep_time=sleep_time)


if __name__ == '__main__':
    main()
