from typing import Literal


PingScanResult = Literal["Alive", "Down or Filtered", "Unexpected Response"]

TcpAckScanResult = Literal[
    "Unfiltered",
    "Filtered",
    "Filtered or No Response",
    "Filtered or Unexpected Response",
]

HalfOpenScanResult = Literal[
    "Filtered or Dropped",
    "Unexpected TCP Flags",
    "Closed",
    "Open",
    "Filtered or Unexpected Response",
]

TcpWindowScanResult = Literal["Filtered or No response", "Open", "Closed", "Filtered or Unexpected Response"]


TcpConnectScanResult = Literal["Filtered or Dropped", "Open", "Closed", "Filtered or Unexpected Response"]


TcpNullScanResult = Literal["Open or Filtered", "Closed", "Filtered or Unexpected Response"]

TcpXmasScanResult = Literal["Open or Filtered", "Closed", "Filtered or Unexpected Response"]

TcpFinScan = Literal["Open or Filtered", "Closed", "Filtered or Unexpected Response"]
