# fSpectrum
A lite Python network downtime logger, built out of spite with the help of ChatGPT

## Description
This Python app uses a simple GET request to a 'likely-up' URL, logging the response and timestamp in a local data file. This allows for simple uptime/downtime tracking, logging, and output. This does not track network performance markers like upload, download, or latency.

Test frequency can be set via a slider input from 1 to 120 minutes. A plot is generated based on previous data and setting a datetime range via two text inputs (a drop-down select provides quick presets). This graph will be updated dynamically as new datapoints are added.

### Dependencies
* Tested on Windows 10 & Windows 11, Python v3.10+

Packages used:
* tkinter
* datetime
* matplotlib
* pickle
(note that this program checks for installed packages and will install the necessary packages if they are not found)

### Installing
* As of v0.1 simply download the fSpectrum folder/repository to your preferred directory. No further installation is required.

### Executing program
* Navigate to the folder where you have downloaded fSpectrum
* Run fSpectrum.py
```
cd /path/to/your/folder/fSpectrum/
python.exe fSpectrum.py
```

## Authors
Alex Pinson
[@pnsn_engineering](https://instagram.com/pnsn_engineering)

## Version History
* 0.1.0
    * Initial Release

## License
This project is licensed under the GNU GPL v3.0 License - see the LICENSE.md file for details
