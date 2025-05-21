#!/usr/bin/env python3
"""
Monitoring system for Curatrak workflows in MagenticUI.
This script tracks and analyzes API calls made through the CuratrakGrokClient.

NOTE: API keys and actual implementation details have been removed for security.
This is a demonstration file only.
"""

import os
import json
import time
import datetime
import argparse
from collections import defaultdict

# Curatrak configuration (API keys removed for security)
CURATRAK_LOG_FILE = "curatrak_workflows.log"

class CuratrakMonitor:
    """Monitor and analyze Curatrak workflows."""
    
    def __init__(self, log_file=None):
        self.log_file = log_file or CURATRAK_LOG_FILE
        self.workflows = defaultdict(list)
        self.active_workflows = set()
    
    def start_monitoring(self, interval=5):
        """Start monitoring workflows at the specified interval (in seconds)."""
        print(f"Starting Curatrak workflow monitoring...")
        print(f"Log file: {self.log_file}")
        
        try:
            # Create log file if it doesn't exist
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    f.write("# Curatrak Workflow Log\n")
            
            # For demonstration purposes, we'll just run a few iterations
            for i in range(3):
                print(f"\nMonitoring iteration {i+1}/3")
                self._process_log_file()
                self._print_status()
                time.sleep(interval)
                
            print("\nDemonstration monitoring completed.")
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    
    def _process_log_file(self):
        """Process the log file to extract workflow events."""
        if not os.path.exists(self.log_file):
            return
        
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    if line.strip().startswith("CURATRAK EVENT:"):
                        # Extract the JSON part
                        json_str = line.strip().replace("CURATRAK EVENT:", "", 1).strip()
                        try:
                            event_data = json.loads(json_str)
                            self._process_event(event_data)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"Error processing log file: {e}")
    
    def _process_event(self, event_data):
        """Process a single workflow event."""
        workflow_id = event_data.get("workflow_id")
        request_id = event_data.get("request_id")
        event_type = event_data.get("event_type")
        
        if not workflow_id or not request_id or not event_type:
            return
        
        # Add to workflows collection
        self.workflows[workflow_id].append(event_data)
        
        # Track active workflows
        if event_type == "request_start":
            self.active_workflows.add(workflow_id)
        elif event_type == "request_complete" or event_type == "request_error":
            # Check if this was the last active request in the workflow
            all_requests = {e.get("request_id") for e in self.workflows[workflow_id]}
            pending_requests = {
                e.get("request_id") for e in self.workflows[workflow_id] 
                if e.get("event_type") == "request_start"
            } - {
                e.get("request_id") for e in self.workflows[workflow_id]
                if e.get("event_type") in ["request_complete", "request_error"]
            }
            
            if not pending_requests:
                self.active_workflows.discard(workflow_id)
    
    def _print_status(self):
        """Print the current status of all workflows."""
        now = datetime.datetime.now().isoformat()
        print(f"\n=== Curatrak Workflow Status ({now}) ===")
        
        if not self.workflows:
            print("No workflows detected yet.")
            return
        
        print(f"Total workflows: {len(self.workflows)}")
        print(f"Active workflows: {len(self.active_workflows)}")
        
        # Print details for each active workflow
        for workflow_id in self.active_workflows:
            events = self.workflows[workflow_id]
            total_requests = len({e.get("request_id") for e in events})
            completed = len({
                e.get("request_id") for e in events 
                if e.get("event_type") in ["request_complete", "request_error"]
            })
            
            print(f"\nWorkflow: {workflow_id}")
            print(f"Requests: {completed}/{total_requests} completed")
            
            # Get the most recent event
            if events:
                latest = max(events, key=lambda e: e.get("timestamp", ""))
                print(f"Last event: {latest.get('event_type')} at {latest.get('timestamp')}")
                
                # Show token usage if available
                if latest.get("event_type") == "request_complete":
                    usage = latest.get("metadata", {}).get("token_usage", {})
                    if usage:
                        print(f"Token usage: {usage}")

def main():
    """Main entry point for the Curatrak monitoring script."""
    parser = argparse.ArgumentParser(description="Monitor Curatrak workflows for MagenticUI")
    parser.add_argument("--log-file", help="Path to the Curatrak log file")
    parser.add_argument("--interval", type=int, default=5, help="Monitoring interval in seconds")
    args = parser.parse_args()
    
    monitor = CuratrakMonitor(log_file=args.log_file)
    monitor.start_monitoring(interval=args.interval)

if __name__ == "__main__":
    main()