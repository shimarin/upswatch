# upswatch

Script to watch UPS status periodically

This script runs as a daemon and periodically checks the status of a UPS.  If the UPS status changes, an email is sent to a specified address.

## Pre-requisites

- NUT (Network UPS Tools) installed and configured

## Usage
```
usage: upswatch.py [-c|--config <config_file>] [-u|--ups <ups_name>] [-v|--verbose] [-h|--help]
```

- ups_name: Name of the UPS to watch.  NUT must be configured with this name.

## Configuration

The configuration file is an INI file with the following sections:

### [UPS]

- **name**: Name of the UPS

### [Email]

- **to**: Email address to send to
- **from**: Email address to send from
- **server**: SMTP server address (default: "localhost")
- **port**: SMTP server port (default: 25)
- **user**: SMTP server username
- **pass**: SMTP server password
- **tls**: Whether to use TLS (default: False)
