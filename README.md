# Interface control
A graphical application for managing network interfaces and routing traffic from specific applications through selected interfaces.

# Features
- Add or remove network interfaces (e.g., TAP interfaces).
- List all network interfaces and mark newly added interfaces.
- Route traffic from selected applications through chosen network interfaces.
- Process selection interface with sortable columns by PID and process name.
- Launch applications bound to specific interfaces using IP addresses.

# Prerequisites
- Python 3.x
- Dependencies: Install the following libraries using pip:
```bash
pip install psutil
```
- Windows OS with administrative privileges.
- tapctl.exe for managing TAP interfaces (usually part of [OpenVPN](https://openvpn.net/downloads/openvpn-connect-v3-windows.msi) installation).
- [ForceBindIP](https://r1ch.net/projects/forcebindip) (Leave link, cause you can download just source and do not install it)

# Installation
1. Clone the repository:
```bash
git clone https://github.com/Azaki21421/Interface-control.git
cd Interface-control
```
2. Install dependencies:
```bash
pip install psutil
```
 - openvpn (tap driver)
 - ForceBindIP
3. Run the application:

```bash
python network_manager.py
```
```Note: The script requires administrator privileges to manage network interfaces. It will prompt you to run as an administrator if not already elevated.```

# Usage
- Add Interface: Click "Add Interface" to create a new TAP interface.
- Remove Interface: Click "Remove Interface" to delete an existing interface.
- Assign Routes:
 - Click "Assign Routes" to open the process selection window.
 - Select a process by PID or name.
 - Choose a network interface to bind the application’s traffic.

# To-Do List

1. Replace OpenVPN Dependency:
 - The current implementation uses tapctl.exe from OpenVPN to manage TAP interfaces. Find a suitable alternative that does not rely on OpenVPN.
2. Find Alternative to ForceBindIP:
 - The application currently uses ForceBindIP to bind applications to specific network interfaces. Consider alternatives or custom implementations for binding traffic to interfaces.
3. Enhance Error Handling:
 - Improve error handling when managing interfaces and routing traffic.
4. Cross-Platform Support:
 - Extend functionality to support other operating systems like Linux and macOS.

# Dependencies
- ```psutil```: For retrieving system and network interface information.
- ```tapctl.exe```: Command-line utility for managing TAP interfaces.
- ```ForceBindIP```: Tool to bind applications to specific network interfaces (needs replacement).
