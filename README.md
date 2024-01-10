# rstudio-grafana-example

A demo Grafana dashboard and Prometheus exporter for Posit RStudio Workbench

This is just a simple example of how to create a Prometheus exporter using Python. Also there is a Grafana dashboard included.

![Preview](/RSWGrafana.png?raw=true "Preview")

Create a virtual environment on your RStudio Workbench server using the `requirements.txt` file, and run the exporter. On your Grafana system, edit `prometheus.yml` to include the host.

Based on: https://trstringer.com/quick-and-easy-prometheus-exporter/
