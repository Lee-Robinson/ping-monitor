#!/usr/bin/env python3
"""
Cross-Platform Continuous Ping Monitor for Packet Loss Detection
Monitors connectivity to a target IP and logs packet drops with timestamps
Compatible with Windows, macOS, and Linux

GitHub: https://github.com/Lee-Robinson/ping-monitor
"""

import subprocess
import datetime
import time
import signal
import sys
import os
import json
import platform

class PingMonitor:
    def __init__(self, target="8.8.8.8", interval=1, log_file="ping_drops.log", report_file="ping_report.html"):
        self.target = target
        self.interval = interval
        self.log_file = log_file
        self.report_file = report_file
        self.total_pings = 0
        self.dropped_pings = 0
        self.consecutive_drops = 0
        self.max_consecutive_drops = 0
        self.start_time = datetime.datetime.now()
        self.drops_log = []
        self.running = True
        self.os_type = platform.system().lower()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        if self.os_type != "windows":
            signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def ping_once(self):
        """Execute a single ping and return True if successful, False if dropped"""
        try:
            if self.os_type == "windows":
                # Windows ping command
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', '3000', self.target],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            else:
                # macOS/Linux ping command
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', '3000', self.target],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            print(f"Error executing ping: {e}")
            return False
    
    def log_drop(self, timestamp):
        """Log a packet drop with timestamp"""
        drop_entry = {
            'timestamp': timestamp.isoformat(),
            'formatted_time': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'consecutive_count': self.consecutive_drops
        }
        self.drops_log.append(drop_entry)
        
        # Write to log file immediately
        with open(self.log_file, 'a') as f:
            f.write(f"{drop_entry['formatted_time']} - Packet drop detected (consecutive: {self.consecutive_drops})\n")
    
    def generate_report(self):
        """Generate an HTML report with statistics and drop details"""
        uptime = datetime.datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        # Calculate statistics
        success_rate = ((self.total_pings - self.dropped_pings) / self.total_pings * 100) if self.total_pings > 0 else 0
        
        # Group drops by hour for analysis
        hourly_drops = {}
        for drop in self.drops_log:
            hour = drop['formatted_time'][:13]  # YYYY-MM-DD HH
            hourly_drops[hour] = hourly_drops.get(hour, 0) + 1
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Ping Monitor Report - {self.target}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .system-info {{ background-color: #ecf0f1; padding: 10px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .stat-box {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ color: #7f8c8d; margin-top: 5px; }}
        .drops-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .drops-table th, .drops-table td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        .drops-table th {{ background-color: #34495e; color: white; }}
        .drops-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .alert {{ background-color: #e74c3c; color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
        .success {{ background-color: #27ae60; color: white; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
        .hourly-analysis {{ margin-top: 30px; }}
        .hourly-table {{ width: 100%; border-collapse: collapse; }}
        .hourly-table th, .hourly-table td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
        .hourly-table th {{ background-color: #3498db; color: white; }}
        .footer {{ margin-top: 30px; text-align: center; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Ping Monitor Report</h1>
            <p><strong>Target:</strong> {self.target} | <strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="system-info">
            <strong>System Info:</strong> {platform.system()} {platform.release()} | 
            <strong>Python:</strong> {platform.python_version()} | 
            <strong>Hostname:</strong> {platform.node()}
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{uptime_str}</div>
                <div class="stat-label">Monitoring Duration</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{self.total_pings:,}</div>
                <div class="stat-label">Total Pings</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{self.dropped_pings:,}</div>
                <div class="stat-label">Dropped Packets</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{success_rate:.2f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{self.max_consecutive_drops}</div>
                <div class="stat-label">Max Consecutive Drops</div>
            </div>
        </div>
        
        {'<div class="alert"><strong>Issue Detected:</strong> Packet loss detected during monitoring period.</div>' if self.dropped_pings > 0 else '<div class="success"><strong>Good News:</strong> No packet loss detected during monitoring period.</div>'}
        
        <h2>Detailed Drop Log</h2>
        {f'<p>Total packet drops recorded: <strong>{len(self.drops_log)}</strong></p>' if self.drops_log else '<p>No packet drops recorded during monitoring period.</p>'}
        
        {'<table class="drops-table"><thead><tr><th>Timestamp</th><th>Consecutive Drops</th><th>Notes</th></tr></thead><tbody>' + ''.join([f'<tr><td>{drop["formatted_time"]}</td><td>{drop["consecutive_count"]}</td><td>{"Start of outage" if drop["consecutive_count"] == 1 else "Ongoing outage"}</td></tr>' for drop in self.drops_log]) + '</tbody></table>' if self.drops_log else ''}
        
        <div class="hourly-analysis">
            <h2>Hourly Drop Analysis</h2>
            {f'<table class="hourly-table"><thead><tr><th>Hour</th><th>Drops</th></tr></thead><tbody>' + ''.join([f'<tr><td>{hour}</td><td>{count}</td></tr>' for hour, count in sorted(hourly_drops.items())]) + '</tbody></table>' if hourly_drops else '<p>No drops to analyze by hour.</p>'}
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
            <h3>Report Summary for ISP</h3>
            <p><strong>Customer Issue:</strong> Intermittent packet loss detected on internet connection.</p>
            <p><strong>Test Method:</strong> Continuous ping monitoring to Google DNS (8.8.8.8) over {uptime_str}.</p>
            <p><strong>Results:</strong> {self.dropped_pings} packet drops out of {self.total_pings} total pings ({(self.dropped_pings/self.total_pings*100):.3f}% loss rate).</p>
            <p><strong>Impact:</strong> {'Significant connectivity issues affecting internet usage.' if success_rate < 99 else 'Minor but noticeable connectivity issues.'}</p>
            <p><strong>System:</strong> {platform.system()} {platform.release()}</p>
        </div>
        
        <div class="footer">
            Generated by Ping Monitor | <a href="https://github.com/yourusername/ping-monitor">GitHub Repository</a>
        </div>
    </div>
</body>
</html>
"""
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report generated: {self.report_file}")
    
    def run(self):
        """Main monitoring loop"""
        print(f"Ping Monitor v1.0 - Cross-Platform Network Monitoring Tool")
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Target: {self.target}")
        print(f"Logging drops to: {self.log_file}")
        print(f"Report will be saved to: {self.report_file}")
        print("Press Ctrl+C to stop monitoring and generate report\n")
        
        # Clear previous log file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"Ping Monitor Started - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"System: {platform.system()} {platform.release()}\n")
            f.write("-" * 50 + "\n")
        
        while self.running:
            timestamp = datetime.datetime.now()
            self.total_pings += 1
            
            if self.ping_once():
                # Successful ping
                if self.consecutive_drops > 0:
                    print(f"✓ Connection restored after {self.consecutive_drops} drops")
                    self.consecutive_drops = 0
                
                # Print status every 60 successful pings (about 1 minute)
                if self.total_pings % 60 == 0:
                    print(f"Status: {self.total_pings} pings sent, {self.dropped_pings} drops ({((self.total_pings-self.dropped_pings)/self.total_pings*100):.1f}% success)")
            
            else:
                # Dropped ping
                self.dropped_pings += 1
                self.consecutive_drops += 1
                self.max_consecutive_drops = max(self.max_consecutive_drops, self.consecutive_drops)
                
                print(f"✗ {timestamp.strftime('%H:%M:%S')} - Packet drop detected (consecutive: {self.consecutive_drops})")
                self.log_drop(timestamp)
            
            time.sleep(self.interval)
        
        # Generate final report
        print(f"\nMonitoring stopped. Generating final report...")
        print(f"Total pings: {self.total_pings}")
        print(f"Dropped pings: {self.dropped_pings}")
        print(f"Success rate: {((self.total_pings-self.dropped_pings)/self.total_pings*100):.2f}%")
        
        self.generate_report()

def main():
    print("=" * 60)
    print("  PING MONITOR - Network Connectivity Testing Tool")
    print("=" * 60)
    
    # You can customize these parameters
    monitor = PingMonitor(
        target="8.8.8.8",           # Target to ping
        interval=1,                 # Seconds between pings
        log_file="ping_drops.log",  # Text log file
        report_file="ping_report.html"  # HTML report file
    )
    
    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nMonitoring interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        monitor.generate_report()

if __name__ == "__main__":
    main()