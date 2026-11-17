# FactIndic for macOS

A native SwiftUI viewer for the completed exploratory pilot. It shows the four
model/prompt result groups and project methods without running inference or
requiring internet access. Factuality labels are AI-screened; human verification
was skipped for this version.

## Run

From the repository root:

```sh
./macos/FactIndicApp/build-macos-app.sh
open macos/FactIndicApp/FactIndic.app
```

Requires an Apple Silicon Mac, macOS 13 or later, and the Swift command line
tools. Model generation continues to run in Colab; this app is a local results
viewer only.
