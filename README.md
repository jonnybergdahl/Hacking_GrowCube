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

Using Wireshark reveals the server is sending more data than Telnet shows.

``` pcap
0000   00 08 a2 0f 0f 3e a8 48 fa c1 3a cc 08 00 45 00   .....>.H..:...E.
0010   00 be 96 be 00 00 ff 06 c8 83 ac 1e 02 46 ac 1e   .............F..
0020   01 75 22 60 fa 7f 00 00 c9 85 92 1d 31 b0 50 18   .u"`........1.P.
0030   08 5e 2f 58 00 00 65 6c 65 61 32 31 23 31 30 23   .^/X..elea21#10#
0040   31 40 32 39 40 33 30 40 32 34 23 00 00 00 00 00   1@29@30@24#.....
0050   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0060   00 00 00 00 00 00 00 00 65 6c 65 61 32 31 23 31   ........elea21#1
0070   30 23 32 40 33 34 40 33 30 40 32 34 23 00 00 00   0#2@34@30@24#...
0080   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
0090   00 00 00 00 00 00 00 00 00 00 65 6c 65 61 32 31   ..........elea21
00a0   23 31 30 23 33 40 33 36 40 33 30 40 32 34 23 00   #10#3@36@30@24#.
00b0   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
00c0   00 00 00 00 00 00 00 00 00 00 00 00               ............
```

### App communication

When the app starts, it connects to the Growcube and starts communication. 

The app starts by sending a `SyncTime` command with the current data and time. 
The device responds with a `RepVersionAndWater` response.

```
> elea44#19#2023@07@12@22@49@05#
< elea24#12#3.6@12663500#
```

The app sends a `SetWorkmode` command for mode `2`. It the continues
asking for data with a `CurveData` command for plant 0.

```
> elea43#1#2#
> elea48#1#0#
< elea22#83#0@2023@7@12@00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,00,95,96,00#
```

The Growcube then sends out it's usual data stream.

```
< elea35#3#0@1#elea23#16#0@2023@6@19@6@38#
< elea35#3#0@1#elea23#16#0@2023@6@19@6@38#
< elea23#16#0@2023@6@19@6@40#
< elea23#16#0@2023@6@19@6@42#elea23#17#0@2023@6@22@18@21#
< elea23#17#0@2023@6@22@18@23#
< elea23#17#0@2023@6@22@18@25#
< elea23#16#0@2023@6@26@0@18#
< elea23#16#0@2023@6@26@0@21#
< elea23#16#0@2023@6@26@0@23#elea23#16#0@2023@6@26@0@25#elea23#15#0@2023@7@1@22@5#

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
---- | ---- | ---- | ----
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
47 | WaterMode | pump #, state, 1 = Start pump, 0 = Stop pump 
48 | CurveData | pump #
49 | WaterMode | sub data: pump #, mode, min value, max value
50 | WifiSettings | sub data: WiFi name, WiFi password, time mils

Command `ele502` is SyncWaterLevel
Command `ele503` is SyncWaterTime
Command `ele504` is Device upgrade command
Command `ele505` is Factory reset command

