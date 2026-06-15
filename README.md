# TaskerHA Companion

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This is a companion HACS integration for the [TaskerHA Android App](https://github.com/db1996/TaskerHa).

**[Full documentation](https://taskerha.db1996-gh.com/)**


## Install Home Assistant integration

### Via HACS


1. Ensure HACS is installed in your Home Assistant setup. If not, follow
   the [HACS installation guide](https://hacs.xyz/docs/setup/download).
2. Install
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=db1996&repository=taskerha-hacs&category=integration)
1. It will ask you to add it as a custom repository, press add. 
2. Click `Install` to add the component to your Home Assistant setup.
3. Restart Home Assistant after the installation completes.
4. Go to Settings -> Integrations and add TaskerHA Companion as a device.

### Manual Installation

1. Navigate to your Home Assistant configuration directory (where your `configuration.yaml` is located).
2. Create a folder named `custom_components` if it doesn't exist.
3. Inside the `custom_components` folder, create another folder named `taskerha_companion`.
4. Clone this repository or download the source code and copy all files from the `custom_components/taskerha_companion/` from the [repository](https://github.com/db1996/taskerha-hacs)
   directory to the newly created `taskerha_companion` folder.
5. Restart Home Assistant to load the custom component.
