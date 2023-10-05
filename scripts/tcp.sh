#!/bin/bash

# Check if the environment variables are set
if [ -z "$PFSENSE_IPADDR" ] || [ -z "$PFSENSE_TCP_PORT" ]; then
  echo "Error: PFSENSE_IPADDR or PFSENSE_TCP_PORT environment variables are not set."
  exit 1
fi

# Execute TCP output
nc "$PFSENSE_IPADDR" "$PFSENSE_TCP_PORT" -C | jq >> /tmp/out.json
