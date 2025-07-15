from dotenv import load_dotenv
load_dotenv()
import argparse
import socket
from src.webui.interface import theme_map, create_ui


def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from start_port"""
    for i in range(max_attempts):
        port = start_port + i
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None


def main():
    parser = argparse.ArgumentParser(description="Gradio WebUI for Browser Agent")
    parser.add_argument("--ip", type=str, default="127.0.0.1", help="IP address to bind to")
    parser.add_argument("--port", type=int, default=7788, help="Port to listen on")
    parser.add_argument("--auto-port", action="store_true", help="Automatically find an available port if the specified port is busy")
    parser.add_argument("--theme", type=str, default="Ocean", choices=theme_map.keys(), help="Theme to use for the UI")
    args = parser.parse_args()

    port = args.port
    if args.auto_port:
        available_port = find_available_port(port)
        if available_port:
            port = available_port
            print(f"Using available port: {port}")
        else:
            print(f"Could not find an available port starting from {args.port}")
            return

    demo = create_ui(theme_name=args.theme)
    try:
        demo.queue().launch(server_name=args.ip, server_port=port)
    except OSError as e:
        if "Cannot find empty port" in str(e):
            print(f"Port {port} is busy. Try using --auto-port flag to automatically find an available port.")
            available_port = find_available_port(port)
            if available_port:
                print(f"Suggestion: Use port {available_port} instead, or run with --auto-port flag")
        raise


if __name__ == '__main__':
    main()
