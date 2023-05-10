# GrowCube_Hacking

These are my notes reverse engineering the protocl used in Growcube. 

I have used Jadx to reverse engineer the Android app to get some insights in how the protocol works. 

> Note: This is still very much a work in progress

## Python script

The python script `growcube_packet_decoder.py` can be used to connect to a Growcube. It dumps the data section and displays the parsed message in a readable format.

```
Connecting to Growcube at 172.30.2.202
Connected
[ 12#3.6@12663500# ] - RepVersionAndWater: version 3.6
[ 3#0@0# ] - Unknown report: 33: data 3, 0@0, 
[ 1#1# ] - RepWaterState: water_warning: False
[ 10#0@50@48@24# ] - RepSTHSate: pump: 0, sh: 50, th: 48, temperature: 24
[ 10#1@33@48@24# ] - RepSTHSate: pump: 1, sh: 33, th: 48, temperature: 24
[ 10#2@27@48@24# ] - RepSTHSate: pump: 2, sh: 27, th: 48, temperature: 24
[ 10#3@29@48@24# ] - RepSTHSate: pump: 3, sh: 29, th: 48, temperature: 24
```

## Communication

The device has a TCP port open on port 8800, connect to that using a raw socket, and it starts to peridocally write out messages. It also support accepting commands.

This is a sample output running Telnet, I just added a line feed to separate different messages.

```
Connected to 172.30.2.202.
Escape character is '^]'.
elea24#12#3.6@12663500#
elea28#1#0#
elea28#1#1#
elea28#1#3#
elea33#3#0@0#
elea21#10#0@26@45@25#
elea21#10#1@17@45@25#
elea21#10#2@23@45@25#
elea21#10#3@15@45@25#
```

## Message format

The messages are composed by the following parts.

Part | Description
---- | ----
"elea" | Message header
XX | Command/Response
"#" | Delimiter
NN | Length of the following data
data | Data, delimited by # delimiters and sub delimited by @ characters
"#" | End of data

## Response values

Value | Description | Attributes | Sample value
---- | ---- | ---
20 | RepWaterState | Water warning? | 1
21 | RepSTHSate | pump #, "st", "th", temperature | 0@50@49@24
22 | RepCurve | ?? |
23 | RepAutoWater | pump #, time stamp divided in separate strings |
24 | RepVersionAndWater | version number (Probably water warning as well?) | 3.6@12663500
25 | RepErasureData | Erasure state |
26 | RepPumpOpen | pump # | 3
27 | RepPumpClose | pump # | 3
33 | (Unknown) | ?? | 0@0

## Command values
Value | Description | Attributes
---- | ---- | ---
43 | SetWorkmode ?? | mode
44 | SyncTime | Current time
45 | PlantEnd ?? | pump #
46 | ClosePump | pump #
47 | Water | pump #, state
48 | CurveData | pump #
49 | WaterMode | sub data: pump #, mode, min value, max value
50 | WifiSettings | sub data: WiFi name, WiFi password, time mils

Command `ele502` is SyncWaterLevel
Command `ele503` is SyncWaterTime
Command `ele504` is Device upgrade command
Command `ele505` is Factory reset command

