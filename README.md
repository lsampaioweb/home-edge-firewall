# Home Edge Firewall

Repository with the settings used on my Fortigate 80E on the Home environment.

This repository uses sub-modules:<br/>
1. [ansible-common-tasks](https://github.com/lsampaioweb/ansible-common-tasks "ansible-common-tasks").

In order to download all the submodules, you have to run the followinng commands:

```bash
# Clone the repository and all of its submodules.
git clone --recurse-submodules https://github.com/lsampaioweb/home-edge-firewall.git

# If you have already cloned. Just initialize the tracking of the submodules.
git submodule --init
git pull --recurse-submodules

# Or in just one line:
git submodule update --init --recursive
```

# Links:

[Links](links.md "Links")

# License:

[MIT](LICENSE "MIT License")

# Created by:

1. Luciano Sampaio.
