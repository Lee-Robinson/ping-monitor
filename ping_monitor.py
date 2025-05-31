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
import threading

class PingMonitor:
    def __init__(self, target="8.8.8.8", duration=None, log_file="ping_drops.log", report_file="ping_report.html"):
        self.target = target
        self.target_name = self.get_target_name(target)
        self.duration = duration  # Duration in hours, None for continuous
        self.log_file = log_file
        self.report_file = report_file
        self.total_pings = 0
        self.dropped_pings = 0
        self.consecutive_drops = 0
        self.max_consecutive_drops = 0
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.drops_log = []
        self.running = True
        self.os_type = platform.system().lower()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        if self.os_type != "windows":
            signal.signal(signal.SIGTERM, self.signal_handler)
    
    def get_target_name(self, ip):
        """Get friendly name for common DNS servers"""
        names = {
            "8.8.8.8": "Google DNS Primary",
            "8.8.4.4": "Google DNS Secondary", 
            "1.1.1.1": "Cloudflare DNS Primary",
            "1.0.0.1": "Cloudflare DNS Secondary",
            "9.9.9.9": "Quad9 DNS",
            "208.67.222.222": "OpenDNS",
            "208.67.220.220": "OpenDNS Secondary"
        }
        return names.get(ip, f"Custom Server ({ip})")
    
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
    
    def check_duration(self):
        """Check if test duration has been reached"""
        if self.duration is None:
            return False  # Run continuously
        
        elapsed_hours = (datetime.datetime.now() - self.start_time).total_seconds() / 3600
        return elapsed_hours >= self.duration
    
    def format_duration(self, hours):
        """Format duration for display"""
        if hours is None:
            return "Continuous"
        elif hours < 1:
            minutes = int(hours * 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif hours >= 24:
            days = int(hours // 24)
            remaining_hours = hours % 24
            if remaining_hours == 0:
                return f"{days} day{'s' if days != 1 else ''}"
            elif remaining_hours < 1:
                remaining_minutes = int(remaining_hours * 60)
                return f"{days} day{'s' if days != 1 else ''} {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"
            else:
                return f"{days} day{'s' if days != 1 else ''} {remaining_hours:.1f} hour{'s' if remaining_hours != 1 else ''}"
        else:
            if hours == int(hours):
                return f"{int(hours)} hour{'s' if hours != 1 else ''}"
            else:
                return f"{hours:.1f} hour{'s' if hours != 1 else ''}"
    
    def format_time_remaining(self, hours):
        """Format remaining time with hours and minutes"""
        if hours <= 0:
            return "0 minutes"
        
        total_minutes = int(hours * 60)
        hours_part = total_minutes // 60
        minutes_part = total_minutes % 60
        
        if hours_part > 0 and minutes_part > 0:
            return f"{hours_part}h {minutes_part}m"
        elif hours_part > 0:
            return f"{hours_part}h"
        else:
            return f"{minutes_part}m"
    
    def get_progress_bar(self, current_seconds, total_seconds, width=30):
        """Generate a text progress bar"""
        if total_seconds <= 0:
            return "[Continuous Mode]"
        
        progress = min(current_seconds / total_seconds, 1.0)
        filled_width = int(progress * width)
        bar = "█" * filled_width + "░" * (width - filled_width)
        percentage = int(progress * 100)
        return f"[{bar}] {percentage}%"
    
    def generate_report(self):
        """Generate an HTML report with statistics and drop details"""
        self.end_time = datetime.datetime.now()
        uptime = self.end_time - self.start_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds
        
        # Calculate statistics
        success_rate = ((self.total_pings - self.dropped_pings) / self.total_pings * 100) if self.total_pings > 0 else 0
        
        # Group drops by hour for analysis
        hourly_drops = {}
        for drop in self.drops_log:
            hour = drop['formatted_time'][:13]  # YYYY-MM-DD HH
            hourly_drops[hour] = hourly_drops.get(hour, 0) + 1
        
        # Test completion status
        completion_status = "Completed Successfully" if self.check_duration() and self.duration else "Manually Stopped"
        if self.duration and not self.check_duration():
            completion_status = "Interrupted"
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Ping Monitor Report - {self.target_name}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .config-summary {{ background-color: #3498db; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
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
            <p><strong>Target:</strong> {self.target_name} ({self.target}) | <strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="config-summary">
            <h3>✓ Test Configuration Summary:</h3>
            <p><strong>Server:</strong> {self.target_name} ({self.target})</p>
            <p><strong>Duration:</strong> {self.format_duration(self.duration) if self.duration else 'Continuous (until stopped manually)'}</p>
            <p><strong>Interval:</strong> 1 second (continuous monitoring)</p>
            <p><strong>Status:</strong> {completion_status}</p>
        </div>
        
        <div class="system-info">
            <strong>System Info:</strong> {platform.system()} {platform.release()} | 
            <strong>Python:</strong> {platform.python_version()} | 
            <strong>Hostname:</strong> {platform.node()}
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{uptime_str}</div>
                <div class="stat-label">Actual Duration</div>
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
            <p><strong>Test Method:</strong> Continuous ping monitoring to {self.target_name} ({self.target}) over {uptime_str}.</p>
            <p><strong>Results:</strong> {self.dropped_pings} packet drops out of {self.total_pings} total pings ({(self.dropped_pings/self.total_pings*100):.3f}% loss rate).</p>
            <p><strong>Impact:</strong> {'Significant connectivity issues affecting internet usage.' if success_rate < 99 else 'Minor but noticeable connectivity issues.'}</p>
            <p><strong>System:</strong> {platform.system()} {platform.release()}</p>
        </div>
        
        <div style="margin-top: 30px; padding: 15px; background-color: #ecf0f1; border-radius: 5px;">
            <h3>📊 Packet Loss Interpretation Guide</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
                <div style="background-color: #27ae60; color: white; padding: 12px; border-radius: 5px;">
                    <h4 style="margin: 0 0 8px 0;">🟢 Excellent (99.9%+ success)</h4>
                    <p style="margin: 0; font-size: 14px;"><strong>0-0.1% packet loss</strong><br>
                    Normal operation. Occasional single drops expected during network maintenance or brief congestion. No action needed.</p>
                </div>
                <div style="background-color: #f39c12; color: white; padding: 12px; border-radius: 5px;">
                    <h4 style="margin: 0 0 8px 0;">🟡 Good (99.0-99.9% success)</h4>
                    <p style="margin: 0; font-size: 14px;"><strong>0.1-1% packet loss</strong><br>
                    Minor issues, possibly during peak usage. Monitor for patterns. Generally acceptable for most uses.</p>
                </div>
                <div style="background-color: #e67e22; color: white; padding: 12px; border-radius: 5px;">
                    <h4 style="margin: 0 0 8px 0;">🟠 Fair (95.0-99.0% success)</h4>
                    <p style="margin: 0; font-size: 14px;"><strong>1-5% packet loss</strong><br>
                    Noticeable issues affecting streaming, gaming, video calls. Contact ISP if persistent, especially during off-peak hours.</p>
                </div>
                <div style="background-color: #e74c3c; color: white; padding: 12px; border-radius: 5px;">
                    <h4 style="margin: 0 0 8px 0;">🔴 Poor (<95% success)</h4>
                    <p style="margin: 0; font-size: 14px;"><strong>>5% packet loss</strong><br>
                    Significant problems affecting all internet usage. Immediate ISP contact required - indicates serious network issues.</p>
                </div>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background-color: white; border-radius: 5px; border-left: 4px solid #3498db;">
                <h4 style="margin: 0 0 10px 0; color: #2c3e50;">💡 Important Notes:</h4>
                <ul style="margin: 0; padding-left: 20px; color: #2c3e50;">
                    <li><strong>100% success is unrealistic</strong> - Network equipment maintenance, routing changes, and brief congestion cause occasional drops</li>
                    <li><strong>WiFi connections</strong> typically have slightly higher loss rates than wired connections</li>
                    <li><strong>Peak hours</strong> (7-11 PM) may show increased packet loss due to network congestion</li>
                    <li><strong>Patterns matter more than totals</strong> - Consistent drops at specific times indicate issues worth investigating</li>
                    <li><strong>Burst losses</strong> (many consecutive drops) are more concerning than scattered single drops</li>
                </ul>
            </div>
            
            <div style="margin-top: 15px; padding: 12px; background-color: #d4edda; border-radius: 5px; border-left: 4px solid #28a745;">
                <p style="margin: 0; color: #155724;"><strong>Your Result: {success_rate:.2f}% success rate</strong> - {'🟢 Excellent network quality' if success_rate >= 99.9 else '🟡 Good network quality with minor issues' if success_rate >= 99.0 else '🟠 Fair network quality - monitor for patterns' if success_rate >= 95.0 else '🔴 Poor network quality - contact ISP immediately'}</p>
            </div>
        </div>
        
        <div class="footer">
            Generated by Ping Monitor | Written by Lee Robinson | <a href="https://github.com/Lee-Robinson/ping-monitor">GitHub Repository</a>
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
        # Clear previous log file
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"Ping Monitor Started - {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Target: {self.target_name} ({self.target})\n")
            f.write(f"Duration: {self.format_duration(self.duration) if self.duration else 'Continuous'}\n")
            f.write(f"System: {platform.system()} {platform.release()}\n")
            f.write("-" * 50 + "\n")
        
        print(f"\n🔄 Starting ping monitor...")
        print(f"📡 Target: {self.target_name} ({self.target})")
        print(f"⏱️  Duration: {self.format_duration(self.duration) if self.duration else 'Continuous (until Ctrl+C)'}")
        print(f"📄 Logging to: {self.log_file}")
        print(f"📊 Report will be saved to: {self.report_file}")
        print(f"\nPress Ctrl+C to stop monitoring early and generate report")
        print("=" * 60)
        
        while self.running:
            # Check if duration has been reached
            if self.check_duration():
                print(f"\n⏰ Test duration reached ({self.format_duration(self.duration)})")
                break
                
            timestamp = datetime.datetime.now()
            self.total_pings += 1
            
            if self.ping_once():
                # Successful ping
                if self.consecutive_drops > 0:
                    print(f"✅ Connection restored after {self.consecutive_drops} drops")
                    self.consecutive_drops = 0
                
                # Print status every 60 successful pings (about 1 minute)
                if self.total_pings % 60 == 0:
                    elapsed = datetime.datetime.now() - self.start_time
                    elapsed_str = str(elapsed).split('.')[0]
                    
                    if self.duration:
                        # Calculate remaining time and progress
                        elapsed_hours = elapsed.total_seconds() / 3600
                        remaining_hours = max(0, self.duration - elapsed_hours)
                        remaining_str = self.format_time_remaining(remaining_hours)
                        
                        # Progress bar
                        total_seconds = self.duration * 3600
                        current_seconds = elapsed.total_seconds()
                        progress_bar = self.get_progress_bar(current_seconds, total_seconds)
                        
                        print(f"📊 {progress_bar}")
                        print(f"📈 Status: {self.total_pings} pings, {self.dropped_pings} drops ({((self.total_pings-self.dropped_pings)/self.total_pings*100):.1f}% success)")
                        print(f"⏱️  Elapsed: {elapsed_str} | Remaining: {remaining_str}")
                    else:
                        print(f"📊 Status: {self.total_pings} pings, {self.dropped_pings} drops ({((self.total_pings-self.dropped_pings)/self.total_pings*100):.1f}% success) | Elapsed: {elapsed_str}")
                    
                    print("-" * 60)
            
            else:
                # Dropped ping
                self.dropped_pings += 1
                self.consecutive_drops += 1
                self.max_consecutive_drops = max(self.max_consecutive_drops, self.consecutive_drops)
                
                print(f"❌ {timestamp.strftime('%H:%M:%S')} - Packet drop detected (consecutive: {self.consecutive_drops})")
                self.log_drop(timestamp)
            
            time.sleep(1)  # 1 second interval
        
        # Generate final report
        elapsed = datetime.datetime.now() - self.start_time
        
        # Calculate final statistics
        success_rate = ((self.total_pings - self.dropped_pings) / self.total_pings * 100) if self.total_pings > 0 else 0
        loss_rate = (self.dropped_pings / self.total_pings * 100) if self.total_pings > 0 else 0
        
        # Determine test completion reason
        completion_reason = "Completed Successfully" if self.check_duration() and self.duration else "Manually Stopped"
        if self.duration and not self.check_duration():
            completion_reason = "Interrupted"
        
        print(f"\n" + "=" * 70)
        print(f"🏁 TEST COMPLETE")
        print("=" * 70)
        
        # Test Summary Section
        print(f"📊 TEST SUMMARY:")
        print(f"   Server: {self.target_name} ({self.target})")
        print(f"   Duration: {str(elapsed).split('.')[0]} (planned: {self.format_duration(self.duration) if self.duration else 'Continuous'})")
        print(f"   Status: {completion_reason}")
        print(f"   System: {platform.system()} {platform.release()}")
        print()
        
        # Results Section
        print(f"📈 RESULTS:")
        print(f"   Total Pings: {self.total_pings:,}")
        print(f"   Successful: {self.total_pings - self.dropped_pings:,}")
        print(f"   Dropped: {self.dropped_pings:,}")
        print(f"   Success Rate: {success_rate:.2f}%")
        print(f"   Packet Loss: {loss_rate:.3f}%")
        print(f"   Max Consecutive Drops: {self.max_consecutive_drops}")
        print()
        
        # Network Quality Assessment
        if success_rate >= 99.9:
            quality = "🟢 EXCELLENT - No significant issues detected"
        elif success_rate >= 99.0:
            quality = "🟡 GOOD - Minor connectivity issues"
        elif success_rate >= 95.0:
            quality = "🟠 FAIR - Noticeable connectivity problems"
        else:
            quality = "🔴 POOR - Significant connectivity issues"
        
        print(f"🎯 NETWORK QUALITY: {quality}")
        print()
        
        print(f"📈 Generating detailed reports...")
        
        self.generate_report()
        
        # Show full file paths
        current_dir = os.path.abspath(".")
        log_path = os.path.join(current_dir, self.log_file)
        report_path = os.path.join(current_dir, self.report_file)
        
        print()
        print("=" * 70)
        print("📁 REPORTS GENERATED:")
        print(f"📄 Text Log: {log_path}")
        print(f"🌐 HTML Report: {report_path}")
        print("=" * 70)
        print("💡 NEXT STEPS:")
        print("   • Open the HTML report in your browser for detailed analysis")
        print("   • Share the HTML report with your ISP or IT support team")
        if self.dropped_pings > 0:
            print("   • Use the timestamped data to correlate with network events")
        print("=" * 70)

def select_server():
    """Interactive server selection menu"""
    servers = [
        ("8.8.8.8", "Google DNS Primary", "Reliable, global coverage"),
        ("8.8.4.4", "Google DNS Secondary", "Backup Google DNS"),
        ("1.1.1.1", "Cloudflare DNS Primary", "Fast, privacy-focused"),
        ("1.0.0.1", "Cloudflare DNS Secondary", "Backup Cloudflare DNS"),
        ("9.9.9.9", "Quad9 DNS", "Security and privacy focused"),
        ("208.67.222.222", "OpenDNS", "Family-safe DNS filtering"),
        ("208.67.220.220", "OpenDNS Secondary", "Backup OpenDNS")
    ]
    
    print("🌍 SERVER SELECTION")
    print("Choose a reliable server for ping testing:")
    print()
    
    for i, (ip, name, description) in enumerate(servers, 1):
        print(f"{i}. {name} ({ip}) - {description}")
    
    print("8. Enter custom server")
    print()
    
    while True:
        try:
            choice = input("Choose option (1-8): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                return servers[int(choice)-1][0]
            elif choice == '8':
                custom_ip = input("Enter custom IP address: ").strip()
                # Basic IP validation
                parts = custom_ip.split('.')
                if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                    return custom_ip
                else:
                    print("❌ Invalid IP address format. Please try again.")
            else:
                print("❌ Invalid choice. Please select 1-8.")
        except (ValueError, IndexError):
            print("❌ Invalid input. Please try again.")

def select_duration():
    """Interactive duration selection menu"""
    durations = [
        (0.5, "30 minutes"),
        (1, "1 hour"),
        (2, "2 hours"), 
        (4, "4 hours"),
        (8, "8 hours"),
        (12, "12 hours"),
        (24, "24 hours (1 day)"),
        (48, "48 hours (2 days)"),
        (None, "Continuous (until stopped manually)"),
        ("custom", "Custom duration")
    ]
    
    print("\n⏱️  TEST DURATION SELECTION")
    print("How long should the test run?")
    print()
    
    for i, (hours, description) in enumerate(durations, 1):
        print(f"{i}. {description}")
    
    print()
    
    while True:
        try:
            choice = input("Choose option (1-10): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return durations[int(choice)-1][0]
            elif choice == '10':
                # Custom duration input
                print("\n📝 CUSTOM DURATION")
                print("Enter duration in one of these formats:")
                print("  - Minutes: '45m' or '45 minutes'")
                print("  - Hours: '3h' or '3 hours'") 
                print("  - Hours and minutes: '2h 30m' or '2.5h'")
                print("  - Days: '1d' or '1 day'")
                print()
                
                while True:
                    custom_input = input("Enter custom duration: ").strip().lower()
                    
                    try:
                        # Parse different formats
                        if 'd' in custom_input and 'h' not in custom_input and 'm' not in custom_input:
                            # Days only: "2d" or "2 days"
                            days = float(custom_input.replace('d', '').replace('ays', '').replace('ay', '').strip())
                            return days * 24
                        elif 'h' in custom_input and 'm' in custom_input:
                            # Hours and minutes: "2h 30m"
                            parts = custom_input.replace('ours', '').replace('our', '').replace('inutes', '').replace('inute', '').replace('ins', '').replace('in', '')
                            h_part = parts.split('h')[0].strip()
                            m_part = parts.split('h')[1].replace('m', '').strip()
                            hours = float(h_part) if h_part else 0
                            minutes = float(m_part) if m_part else 0
                            return hours + (minutes / 60)
                        elif 'h' in custom_input:
                            # Hours only: "3h" or "3.5h" or "3 hours"
                            hours = float(custom_input.replace('h', '').replace('ours', '').replace('our', '').strip())
                            return hours
                        elif 'm' in custom_input:
                            # Minutes only: "90m" or "90 minutes"
                            minutes = float(custom_input.replace('m', '').replace('inutes', '').replace('inute', '').replace('ins', '').replace('in', '').strip())
                            return minutes / 60
                        else:
                            # Try to parse as decimal hours
                            hours = float(custom_input)
                            if hours <= 0:
                                print("❌ Duration must be greater than 0. Please try again.")
                                continue
                            return hours
                    except ValueError:
                        print("❌ Invalid format. Please try again.")
                        print("Examples: '30m', '2h', '1.5h', '2h 30m', '1d'")
                        continue
            else:
                print("❌ Invalid choice. Please select 1-10.")
        except (ValueError, IndexError):
            print("❌ Invalid input. Please try again.")

def show_configuration_summary(target, target_name, duration):
    """Display configuration summary before starting test"""
    print("\n" + "=" * 60)
    print("✅ CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"📡 Server: {target_name} ({target})")
    print(f"⏱️  Duration: {PingMonitor('').format_duration(duration) if duration else 'Continuous (until stopped manually)'}")
    print(f"🔄 Interval: 1 second (continuous monitoring)")
    print(f"📄 Log file: ping_drops.log")
    print(f"📊 Report file: ping_report.html")
    print("=" * 60)
    
    confirm = input("\nProceed with this configuration? (y/n): ").strip().lower()
    return confirm in ['y', 'yes']

def main():
    print("=" * 70)
    print("  PING MONITOR - Network Connectivity Testing Tool")
    print("  Written by Lee Robinson")
    print("  GitHub: https://github.com/Lee-Robinson")
    print("  Repository: https://github.com/Lee-Robinson/ping-monitor")
    print("=" * 70)
    
    try:
        # Interactive configuration
        target = select_server()
        duration = select_duration()
        
        # Create monitor instance to get target name
        temp_monitor = PingMonitor(target)
        target_name = temp_monitor.get_target_name(target)
        
        # Show configuration summary and get confirmation
        if not show_configuration_summary(target, target_name, duration):
            print("❌ Test cancelled by user.")
            return
        
        # Create and run the monitor
        monitor = PingMonitor(
            target=target,
            duration=duration,
            log_file="ping_drops.log",
            report_file="ping_report.html"
        )
        
        monitor.run()
        
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
