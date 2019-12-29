# CR2 Preprocessor
Moves, batch process, and losslessly compresses [dual-iso](https://www.magiclantern.fm/forum/?topic=7139.0) cr2 raw image files.

## Installation
See [Brilliant Imagery](http://www.brilliantimagery.org/) for more info and binaries (versions of the software that you can just double click to run rather than setup) (hopefully it'll be up by the time you see this).

If you don't already have `pipenv`, install it. Note, it shouldn't be installed into a virtual environment.

```
$ pip install pipenv
```

Clone the reposatory to a working directory.

```
$ git clone https://github.com/brilliantimagery/CR2_Preprocessor.git
```


From the top level within the project (from within the `CR2_Preprocessor` folder that has the `README.md` file it it), create the virtual environment and install the dependencies.

```
$ pipenv install
```

[Adobe DNG Converter](https://helpx.adobe.com/photoshop/using/adobe-dng-converter.html) also needs to be installed and the location of the "Adobe DNG Converter.exe" file needs to be known. It may be at "C:/Program Files (x86)/Adobe/Adobe DNG Converter.exe".

## Run the App

From the top level of the project, activate the virtual environment.

```
$ pipenv shell
```

Start the app.

```
$ python run.py
```

Set the location of the "Adobe DNG Converter.exe" file.

Set the location of the files that are to be converted.

Set the location of where the output file are to be saved to.

## Compiling for Distribution
The app along with all required supporting parts can be gathered into one distributable folder using PyInstaller.

With the pipenv shell activated run:

```
$ pytest ui.spec
```

The `CR2_Preprocessor` folder from within the `dist` folder can be used as a standalone distribution. To run the app, run `CR2_Preprocessor.exe` from within the `CR2_Prepocessor` folder.

[Adobe DNG Converter](https://helpx.adobe.com/photoshop/using/adobe-dng-converter.html) still needs to be installed to a known location.


## Testing
Being a small stop-gap project, there isn't currently any testing. If people start using it, that'll likely change.

## Apple Support
I have Windows computers so I support them. If you have an Mac and would like to help bring support to them, let me know!

## Included Dependencies
[cr2hdr](https://magiclantern.fm/), [dcraw](https://www.dechifro.org/dcraw/), and [exiftool](https://exiftool.org/) are all included dependencies. See their respective sites for more info, and thank you for your work.
