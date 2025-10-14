#!/usr/bin/env python3
"""
OSC Receiver Program
Receives and displays OSC messages from other applications.
"""

from pythonosc import dispatcher
from pythonosc import osc_server
import argparse


def print_handler(address, *args):
    """
    Default handler that prints received OSC messages.

    Args:
        address: The OSC address pattern (e.g., '/filter', '/volume')
        *args: The arguments sent with the OSC message
    """
    print(f"OSC Message received:   Address: {address} , Arguments: {args} \n")

def eeg_handler(address, *args):
    """
    Example handler for EEG messages.
    """
    if args:
        TP9 = args[0]
        AF7 = args[1]
        AF8 = args[2]
        TP10 = args[3]
        print(f"EEG Received, TP9 = {TP9} , AF7 = {AF7} , AF8 = {AF8} , TP10 = {TP10}")

def eeg_Aux_handler(address, *args):
    """
    Example handler for EEG messages.
    """
    if args:
        AUX_LEFT = args[0]
        AUX_RIGHT = args[1]
        AUX3 = args[2]
        AUX4 = args[3]
        print(f"EEG Received, AUX_LEFT = {TP9} , AUX_RIGHT = {AF7} , AF8 = {AF8} , TP10 = {TP10}")


def main():
    """
    Main function to set up and start the OSC server.
    """
    parser = argparse.ArgumentParser(
        description="OSC Receiver - Listen for OSC messages",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--ip",
        default="0.0.0.0",
        help="The IP address to listen on (use 0.0.0.0 for all interfaces)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7000,
        help="The port to listen on"
    )

    args = parser.parse_args()

    # Create a dispatcher to route OSC messages to handlers
    disp = dispatcher.Dispatcher()

    # Map specific OSC addresses to handler functions
    disp.map("/eeg", eeg_handler)

    # Catch-all handler for any other OSC addresses
    disp.map("/*", print_handler)

    # Create and start the OSC server
    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), disp)

    print("=" * 50)
    print(f"OSC Receiver started")
    print(f"Listening on {args.ip}:{args.port}")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down OSC receiver...")
        server.shutdown()
        print("Done!")


if __name__ == "__main__":
    main()
