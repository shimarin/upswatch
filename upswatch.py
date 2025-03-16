#!/usr/bin/env python3
import configparser,logging

def get_ups_status(ups_name: str) -> str:
    import subprocess
    # Run `upsc <ups_name> ups.status` to get ups status
    try:
        process = subprocess.run(["upsc", ups_name, "ups.status"], check=True, stdout=subprocess.PIPE)
        return process.stdout.decode().strip()
    except subprocess.CalledProcessError:
        return "UNKNOWN"

def send_email(email_to: str, email_from: str, email_server: str, email_port: int, email_user: str, email_pass: str, email_tls: bool, subject: str, body: str):
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(email_server, email_port)
    if email_tls:
        server.starttls()
    if email_user is not None and email_pass is not None:
        server.login(email_user, email_pass)
    server.send_message(msg)
    server.quit()
    logging.debug(f"Email sent to {email_to}")

def main(config: configparser.ConfigParser):
    import time
    # Get the UPS name from config. Error if not found
    ups_name = config.get('UPS', 'name', fallback=None)
    if ups_name is None:
        raise ValueError("UPS name not found in config file")

    email_to = config.get('Email', 'to', fallback=None)
    if email_to is not None:
        email_from = config.get('Email', 'from', fallback=None)
        if email_from is None:
            raise ValueError("Email from address not found in config file")
        #else
        email_server = config.get('Email', 'server', fallback="localhost")
        email_port = config.get('Email', 'port', fallback=25)
        email_user = config.get('Email', 'user', fallback=None)
        email_pass = config.get('Email', 'pass', fallback=None)
        email_tls = config.get('Email', 'tls', fallback=False)

    last_status = "NONE"
    while True:
        status = get_ups_status(ups_name)
        logging.debug(f"UPS status: {status}")
        if status != last_status:
            logging.info(f"UPS status changed from {last_status} to {status}")
            if email_to is not None:
                send_email(email_to, email_from, email_server, email_port, email_user, email_pass, email_tls, f"UPS status changed to {status}", f"UPS status changed from {last_status} to {status}")
            last_status = status
        # sleep for 1 minute
        time.sleep(60)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='UPS Watcher')
    parser.add_argument("-c", "--config", help="Config file", default="/etc/upswatch.conf")
    parser.add_argument("-u", "--ups", help="UPS name")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    config = configparser.ConfigParser()
    config.read(args.config)
    if args.ups is not None:
        if not config.has_section('UPS'): config.add_section('UPS')
        config['UPS']['name'] = args.ups
    main(config)