fastlane documentation
----

# Installation

Make sure you have the latest version of the Xcode command line tools installed:

```sh
xcode-select --install
```

For _fastlane_ installation instructions, see [Installing _fastlane_](https://docs.fastlane.tools/#installing-fastlane)

# Available Actions

## iOS

### ios check

```sh
[bundle exec] fastlane ios check
```

Check App Store Connect credentials and print the latest build number

### ios build

```sh
[bundle exec] fastlane ios build
```

Install pods and build a signed App Store archive

### ios beta

```sh
[bundle exec] fastlane ios beta
```

Build and upload to TestFlight

### ios release

```sh
[bundle exec] fastlane ios release
```

Build, upload, and submit the current version for App Review

### ios resubmit

```sh
[bundle exec] fastlane ios resubmit
```

Push metadata and age rating, then resubmit a rejected version with its current build

----

This README.md is auto-generated and will be re-generated every time [_fastlane_](https://fastlane.tools) is run.

More information about _fastlane_ can be found on [fastlane.tools](https://fastlane.tools).

The documentation of _fastlane_ can be found on [docs.fastlane.tools](https://docs.fastlane.tools).
