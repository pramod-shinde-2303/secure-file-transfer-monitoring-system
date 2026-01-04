import json
import os
from datetime import datetime
from config import settings

class ReportGenerator:
    """
    Parses logs and generates a summary report.
    """
    
    @staticmethod
    def generate_report():
        log_file = settings.LOG_FILE
        if not os.path.exists(log_file):
            return "No logs found to generate report."
            
        events = []
        violations = []
        start_time = None
        end_time = None
        
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        events.append(entry)
                        
                        # Track time range
                        if not start_time:
                            start_time = entry.get('timestamp')
                        end_time = entry.get('timestamp')
                        
                        # Identify violations/alerts
                        if entry.get('extra_data', {}).get('type') == 'ALERT':
                            violations.append(entry)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            return f"Error reading logs: {e}"

        report_filename = f"Security_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path = os.path.join(settings.REPORT_DIR, report_filename)
        
        with open(report_path, 'w') as r:
            r.write("# Secure File Transfer Monitoring System - Audit Report\n\n")
            r.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            r.write(f"**Monitoring Scope:** `{settings.MONITOR_PATH}`\n")
            r.write(f"**Total Events Recorded:** {len(events)}\n")
            r.write(f"**Violations Detected:** {len(violations)}\n")
            r.write("---\n\n")
            
            r.write("## 1. Executive Summary\n")
            if violations:
                r.write(f"The system detected **{len(violations)} security alerts** during the monitoring session. ")
                r.write("Immediate review of the 'Detected Violations' section is recommended.\n")
            else:
                r.write("No high-severity violations were detected during this session. System activity appears normal.\n")
            r.write("\n")
            
            r.write("## 2. Detected Violations\n")
            if violations:
                r.write("| Timestamp | Severity | Message | Path |\n")
                r.write("|-----------|----------|---------|------|\n")
                for v in violations:
                    extra = v.get('extra_data', {})
                    r.write(f"| {v.get('timestamp')} | **{extra.get('severity')}** | {extra.get('message')} | `{extra.get('details', {}).get('path', 'N/A')}` |\n")
            else:
                r.write("*No violations detected.*\n")
            r.write("\n")
            
            r.write("## 3. High-Risk File Activity Timeline (Last 10 Events)\n")
            r.write("| Timestamp | Event | File | Details |\n")
            r.write("|-----------|-------|------|---------|\n")
            # Show last 10 relevant events (skipping raw debugs if any)
            for e in events[-10:]:
                extra = e.get('extra_data', {})
                # Skip the alert wrapper events to avoid duplication if we want raw FS events, 
                # but valid to show everything. Let's show the specific file events.
                evt_type = extra.get('type', 'UNKNOWN')
                path = extra.get('path', extra.get('details', {}).get('path', 'N/A'))
                r.write(f"| {e.get('timestamp')} | {evt_type} | `{path}` | {str(extra)} |\n")
                
            r.write("\n")
            r.write("## 4. Recommendations\n")
            if violations:
                r.write("- [ ] Investigate users associated with the source paths of violations.\n")
                r.write("- [ ] Verify the integrity of sensitive files involved in unauthorized transfers.\n")
                r.write("- [ ] Review permissions for the destination folders.\n")
            else:
                r.write("- [ ] Continue routine monitoring.\n")
            
            r.write("\n---\n*Generated automatically by Secure File Transfer Monitoring System*")

        return report_path
