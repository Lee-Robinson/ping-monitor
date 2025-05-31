# Ping Monitor - Network Connectivity Testing Tool

A cross-platform Python application that continuously monitors network connectivity by pinging a target server (default: Google DNS 8.8.8.8) and logs packet drops with detailed timestamps. Perfect for documenting intermittent network issues to share with your ISP.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Lee-Robinson/ping-monitor)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![Ping Monitor Screenshot](https://github.com/user-attachments/assets/c0873a1a-5752-49f1-931f-f48efc292233)


# Ping Monitor - Professional Network Connectivity Testing Tool

A cross-platform Python application with an interactive interface for monitoring network connectivity. Features server selection, duration controls, and professional reporting - perfect for documenting network issues to share with your ISP or IT team.

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Lee-Robinson/ping-monitor)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Key Features

### 📋 Interactive Configuration
- **Server Selection Menu**: Choose from 7 popular DNS servers or enter custom IP
- **Duration Controls**: Set specific test duration (1-48 hours) or run continuously
- **Configuration Summary**: Professional overview with confirmation before starting
- **User-Friendly Interface**: Inspired by professional network testing tools like IPERF

### 🔍 Comprehensive Monitoring
- **Real-Time Tracking**: Live updates every minute with progress indicators
- **Detailed Statistics**: Success rates, consecutive drops, and timing analysis
- **Cross-Platform Support**: Automatic OS detection for Windows, macOS, and Linux
- **Graceful Handling**: Proper completion whether duration reached or manually stopped

### 📊 Professional Reporting
- **Dual Output**: Text logs for technical review and HTML reports for presentations
- **ISP-Ready Documentation**: Professional summaries formatted for technical support
- **Visual Analytics**: Hourly drop analysis and statistical breakdowns
- **Complete Audit Trail**: Configuration details and system information embedded

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/Lee-Robinson/ping-monitor.git
cd ping-monitor
python3 ping_monitor.py
```

### Interactive Setup
1. **Choose Your Server**
   ```
   🌍 SERVER SELECTION
   1. Google DNS Primary (8.8.8.8) - Reliable, global coverage
   2. Google DNS Secondary (8.8.4.4) - Backup Google DNS
   3. Cloudflare DNS Primary (1.1.1.1) - Fast, privacy-focused
   4. Cloudflare DNS Secondary (1.0.0.1) - Backup Cloudflare DNS
   5. Quad9 DNS (9.9.9.9) - Security and privacy focused
   6. OpenDNS (208.67.222.222) - Family-safe DNS filtering
   7. OpenDNS Secondary (208.67.220.220) - Backup OpenDNS
   8. Enter custom server
   ```

2. **Set Test Duration**
   ```
   ⏱️  TEST DURATION SELECTION
   1. 1 hour
   2. 2 hours
   3. 4 hours
   4. 8 hours
   5. 24 hours (1 day)
   6. 48 hours (2 days)
   7. Continuous (until stopped manually)
   ```

3. **Review Configuration**
   ```
   ✅ CONFIGURATION SUMMARY
   📡 Server: Google DNS Primary (8.8.8.8)
   ⏱️  Duration: 4 hours
   🔄 Interval: 1 second (continuous monitoring)
   📄 Log file: ping_drops.log
   📊 Report file: ping_report.html
   ```

## 📋 Platform-Specific Setup

### macOS
```bash
# Install Python 3 via Homebrew (if needed)
brew install python

# Clone and run
git clone https://github.com/Lee-Robinson/ping-monitor.git
cd ping-monitor
python3 ping_monitor.py
```

### Windows
```bash
# Download Python from python.org (if needed)
# Clone via Git or download ZIP

# Run in Command Prompt or PowerShell
git clone https://github.com/Lee-Robinson/ping-monitor.git
cd ping-monitor
python ping_monitor.py
```

### Linux (Ubuntu/Debian)
```bash
# Install Python 3 (if needed)
sudo apt update && sudo apt install python3 git

# Clone and run
git clone https://github.com/Lee-Robinson/ping-monitor.git
cd ping-monitor
python3 ping_monitor.py
```

## 🎯 Real-World Usage Examples

### ISP Troubleshooting
```bash
# Document intermittent connection issues
# Select: Cloudflare DNS Primary (1.1.1.1)
# Duration: 8 hours (overnight monitoring)
# Result: Professional report with timestamped drops for ISP support
```

### Business Network Monitoring
```bash
# Monitor office connectivity during business hours
# Select: Google DNS Primary (8.8.8.8) 
# Duration: 24 hours (full day analysis)
# Result: Hourly breakdown showing peak problem times
```

### Home Network Analysis
```bash
# Check connection stability for remote work
# Select: Quad9 DNS (9.9.9.9)
# Duration: 4 hours (during video conferencing)
# Result: Evidence of drops affecting work productivity
```

## 📊 Understanding Your Results

### Live Monitoring Display
```
📊 Status: 3600 pings, 12 drops (99.7% success) | Elapsed: 1:00:00 | 3 hours remaining
❌ 14:23:45 - Packet drop detected (consecutive: 1)
✅ Connection restored after 2 drops
```

### Success Rate Guidelines
- **99.9%+**: Excellent connection quality
- **99.0-99.9%**: Good connection with minor issues  
- **95.0-99.0%**: Noticeable problems - contact ISP
- **<95.0%**: Significant issues requiring immediate attention

### Report Files Generated
- **`ping_drops.log`**: Technical log with raw timestamps
- **`ping_report.html`**: Professional report for sharing with support teams

## 🔧 Advanced Configuration

### Custom Target Servers
```python
# Edit the script to add your preferred servers
# Or select option 8 for custom IP entry during runtime
```

### Output File Locations
Files are saved in the directory where you run the script:
```bash
ls -la
# Shows: ping_drops.log, ping_report.html, plus original files
```

### Running in Background (Linux/macOS)
```bash
# Run in background with output logging
nohup python3 ping_monitor.py > monitor_output.log 2>&1 &

# Check process
ps aux | grep ping_monitor
```

## 🛠️ Troubleshooting

### Permission Issues
Some systems require elevated privileges:
```bash
# macOS/Linux
sudo python3 ping_monitor.py

# Windows (Run Command Prompt as Administrator)
python ping_monitor.py
```

### Python Not Found
- **Windows**: Download from [python.org](https://python.org/downloads/)
- **macOS**: Install via Homebrew: `brew install python`
- **Linux**: Install via package manager: `sudo apt install python3`

### Script Won't Stop
- Try `Ctrl+C` (recommended - generates final report)
- Try `Ctrl+Z` then `kill %1` (Linux/macOS)
- Close terminal window (last resort)
