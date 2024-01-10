"""Application exporter"""

import os
import time
import sys
import subprocess
from prometheus_client import start_http_server, Gauge, Enum
import requests

def run_command_with_output(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.stdout.read().decode().strip()

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, app_port=80, polling_interval_seconds=30):
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.logged_in_users = Gauge("app_logged_in_users", "Logged In Users")
        self.open_sessions = Gauge("app_open_sessions", "Open Sessions")
        self.used_memory = Gauge("app_used_memory", "Used Memory")
        self.free_memory = Gauge("app_free_memory", "Free Memory")
        self.health = Enum("app_server_status", "Status", states=["active", "inactive", "failed"])

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Fetch raw status data from the application
        self.logged_in_users.set(run_command_with_output("rstudio-server active-sessions rstudio-server active-sessions | grep username | awk '{ print $2 }' | sort | uniq | wc -l"))
        self.open_sessions.set(run_command_with_output("rstudio-server active-sessions 2> /dev/null | grep sessionId | wc -l"))
        self.used_memory.set(run_command_with_output("free | grep Mem | awk '{ print $3 }'"))
        self.free_memory.set(run_command_with_output("free | grep Mem | awk '{ print $4 }'"))
        self.health.state(run_command_with_output("rstudio-server status | fgrep 'Active:' | awk '{print $2;}'"))

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "30"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9877"))

    app_metrics = AppMetrics(
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()
