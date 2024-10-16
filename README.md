# APK Significant properties extractor

This script extracts the file `AndroidManifest.xml` from an APK package, decodes it and outputs the significant properties of the APK defined by the user in the `axml.ini` file both in the shell and in an XML file.

## Use
Define the properties you want to extract from the APK file in the `axml.ini` file (omit the "android:" namespace). Different attributes of the same element are appended and separated by "@" as shown in the [axml.ini](axml.ini) sample file.

Run the `main.py` file and provide
* As the first argument, a filename (either an `AndroidManifest.xml` file or an APK file);
* Optionnally, as the second argument, the expected filename of the XML output (it will be "result.xml" by defualt).
`
## Credits
The script `axml.py` was reused from [@i64](https://github.com/i64): https://gist.github.com/i64/b7d9d5e9c7745c276d34ac21289f6537

The script `main.py` was originally made by Jérémy Lavalley (Bibliothèque nationale de France) then edited by me.