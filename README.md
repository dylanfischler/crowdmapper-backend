## The Backend for CrowdMapper

This repository includes the backend python server for processing and data and writing it to the database, as well as the AWS KCL for consuming data from the Kinesis stream.

#### Set Up
Create an `app.properties` file from the provided `app.properties.sample`. Fill in executableName with an absolute path to `server.py` (in this repository).

Create an `start_kpl` file from the provided `start_kpl.sample`. Provide a path to Java on your system.

#### Running
For now: start the KPL by running `./start_kpl`