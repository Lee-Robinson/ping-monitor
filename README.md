# Ping Monitor - Network Connectivity Testing Tool

A cross-platform Python application that continuously monitors network connectivity by pinging a target server (default: Google DNS 8.8.8.8) and logs packet drops with detailed timestamps. Perfect for documenting intermittent network issues to share with your ISP.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Lee-Robinson/ping-monitor)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![Ping Monitor Screenshot](https://github.com/user-attachments/assets/c0873a1a-5752-49f1-931f-f48efc292233)

## 🚀 Features

- **Cross-platform**: Works on Windows, macOS, and Linux
- **Continuous monitoring**: Runs indefinitely until stopped
- **Detailed logging**: Records every packet drop with precise timestamps
- **Professional reports**: Generates HTML reports perfect for ISP communication
- **Real-time statistics**: Shows live success rates and consecutive drop counts
- **Graceful shutdown**: Ctrl+C stops monitoring and generates final report
- **Customizable**: Easy to modify target IP, ping intervals, and file locations

## 📋 Requirements

- Python 3.6 or higher
- Internet connection
- Administrative/root privileges may be required on some systems for ping functionality

## 🔧 Installation

### Option 1: Download and Run
1. Download `ping_monitor.py` from this repository
2. Open terminal/command prompt in the download location
3. Run: `python3 ping_monitor.py` (macOS/Linux) or `python ping_monitor.py` (Windows)

### Option 2: Clone Repository
```bash
git clone https://github.com/Lee-Robinson/ping-monitor.git
cd ping-monitor
python3 ping_monitor.py
```

## 🖥️ Platform-Specific Setup

### macOS
```bash
# Install Python 3 if needed (using Homebrew)
brew install python

# Run the monitor
python3 ping_monitor.py
```

### Windows
```bash
# Download Python from python.org if needed
# Then run in Command Prompt or PowerShell
python ping_monitor.py
```

### Linux
```bash
# Install Python 3 if needed (Ubuntu/Debian)
sudo apt update && sudo apt install python3

# Run the monitor
python3 ping_monitor.py
```

## 🎯 Usage

### Basic Usage
```bash
python3 ping_monitor.py
```

### What You'll See
```
============================================================
  PING MONITOR - Network Connectivity Testing Tool
============================================================
Ping Monitor v1.0 - Cross-Platform Network Monitoring Tool
System: Darwin 21.6.0
Target: 8.8.8.8
Logging drops to: ping_drops.log
Report will be saved to: ping_report.html
Press Ctrl+C to stop monitoring and generate report

Status: 60 pings sent, 0 drops (100.0% success)
✗ 14:23:45 - Packet drop detected (consecutive: 1)
✗ 14:23:46 - Packet drop detected (consecutive: 2)
✓ Connection restored after 2 drops
```

### Stopping the Monitor
- Press `Ctrl+C` to stop monitoring
- The application will generate a final report automatically
- Files are saved in the same directory where you run the script

## 📊 Output Files

The application creates two files:

### 1. `ping_drops.log` (Text Log)
```
Ping Monitor Started - 2025-05-31 14:20:15
Target: 8.8.8.8
System: Darwin 21.6.0
--------------------------------------------------
2025-05-31 14:23:45 - Packet drop detected (consecutive: 1)
2025-05-31 14:23:46 - Packet drop detected (consecutive: 2)
```

### 2. `ping_report.html` (Professional Report)
- Complete statistics and analysis
- Hourly drop patterns
- System information
- ISP-ready summary section
- Professional formatting for technical support

## ⚙️ Customization

You can modify the script parameters by editing the `main()` function:

```python
monitor = PingMonitor(
    target="8.8.8.8",                    # Change ping target
    interval=1,                          # Seconds between pings
    log_file="my_ping_drops.log",        # Custom log filename
    report_file="my_ping_report.html"    # Custom report filename
)
```

### Common Customizations
- **Different target**: Change to your ISP's DNS or another reliable server
- **Faster monitoring**: Set `interval=0.5` for ping every 500ms
- **Slower monitoring**: Set `interval=5` for ping every 5 seconds
- **Custom file location**: Use full paths like `"/Users/username/Desktop/ping_log.txt"`

## 🔍 Troubleshooting

### "Permission Denied" Error
Some systems require elevated privileges for ping:
```bash
# macOS/Linux
sudo python3 ping_monitor.py

# Windows (Run Command Prompt as Administrator)
python ping_monitor.py
```

### "Python Not Found" Error
- **Windows**: Download from [python.org](https://python.org/downloads/)
- **macOS**: Install via Homebrew: `brew install python`
- **Linux**: Install via package manager: `sudo apt install python3`

### Script Doesn't Stop with Ctrl+C
- Try `Ctrl+Z` then `kill %1` (Linux/macOS)
- Close terminal window as last resort
- Files should still be generated upon exit

## 📈 Understanding the Results

### Success Rate Guidelines
- **99.9%+**: Excellent connection
- **99.0-99.9%**: Good connection with minor issues
- **95.0-99.0%**: Noticeable issues, report to ISP
- **<95.0%**: Significant problems requiring immediate ISP attention

### Using Results with Your ISP
1. Run monitor during problem periods (overnight, peak hours)
2. Collect at least 1-2 hours of data showing issues
3. Share the HTML report with your ISP support
4. Reference specific timestamps and drop patterns
5. Include system information from the report

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- Feature enhancements
- Platform-specific improvements
- Documentation updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for network troubleshooting and ISP communication
- Inspired by the need for concrete evidence of intermittent connectivity issues
- Cross-platform compatibility for maximum usability

---

**Happy monitoring!** 🖥️📡
