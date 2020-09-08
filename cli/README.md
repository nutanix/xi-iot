# Introducing the KPS Command Line Interface (CLI)

**Note**: Nutanix is actively developing the kps CLI. As a result, the software published here is release candidate (RC) quality until further notice. 
Use this software at your own risk and do not use it in a production environment or deployment. The latest release candidate is shown below.

The kps CLI is a command line tool that helps you manage your Karbon Platform Services  resources from your terminal or shell. With minimal configuration, you can start using Karbon Platform Services functionality equal to that provided by the browser-based Karbon Platform Services Management Console from the command prompt in your favorite terminal program.

## Shell Support
**Linux and macOS** You can use common shell programs such as bash and zsh.
Note that autocompletion for zsh is experimental in this release.

# Installing kps CLI
## MacOS
Download the kps CLI for MacOS:

**64-bit**
[kps-v1.0.0-rc8-darwin_amd64.tar.gz](https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-darwin_amd64.tar.gz)

**32-bit**
[kps-v1.0.0-rc8-darwin_386.tar.gz](https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-darwin_386.tar.gz)

Optionally, from your terminal or shell, use `wget`.
```
$ wget https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-darwin_amd64.tar.gz
$ mkdir kps && tar zxvf kps-v1.0.0-rc8-darwin_amd64.tar.gz -C kps
$ sudo kps/install [*optional_path*]
```

**Note** The kps binary default installation directory is `/usr/local/bin/`. 
To install the kps binary in a custom location, specify the custom directory or path as follows, where
my/custom/dir is the installation path:
```
$ sudo kps/install /my/custom/dir
```

## Linux
Download the kps CLI for Linux:

**64-bit**
[kps-v1.0.0-rc8-linux_amd64.tar.gz](https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-linux_amd64.tar.gz)

**32-bit**
[kps-v1.0.0-rc8-linux_386.tar.gz](https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-linux_386.tar.gz)

Optionally, from your terminal or shell, use `wget`.
```
$ wget https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-linux_amd64.tar.gz
$ mkdir kps && tar zxvf kps-v1.0.0-rc8-linux_amd64.tar.gz -C kps
$ sudo kps/install [*optional_path*]
```

**Note** The kps binary default installation directory is `/usr/local/bin/`. 
To install the kps binary in a custom location, specify the custom directory or path as follows, where
my/custom/dir is the installation path:
```
$ sudo kps/install /my/custom/dir
```

## Windows

Download the kps CLI for Microsoft Windows:

**64-bit**
[kps-v1.0.0-rc8-windows_amd64.zip](https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-windows_amd64.zip)

**32-bit**
[kps-v1.0.0-rc8-windows_386.zip](https://kps-cli.s3-us-west-2.amazonaws.com/kps-v1.0.0-rc8-windows_386.zip)

1. Extract the .EXE file from the zip file.
2. Rename the extracted .EXE file to kps.exe
2. Open a command windows, navigate to the .EXE file, and run it.


# Configuring kps CLI
Configure the kps CLI to interact with Karbon Platform Services API, including your user role and credentials.
A kps CLI user operates under a specific context. A user email address, password, and context name defines the context.
The user operates according to the role assigned to their user name and email for Karbon Platform Services users. 

For example, create a context named local_user_ctx_1 for an existing local user user1@contoso.com with a password of nutanix/4u.
(A local user is a user that does not have My Nutanix portal credentials.) 

**Note**: You can only specify an existing local user email name and password in this example. 
If you do not have a local user, create one according to the [Creating a User topic](https://portal.nutanix.com/#/page/docs/details?targetId=kps-Infra-Admin-Guide:edg-iot-add-users-t.html) at the Nutanix Support Portal.

```
kps config create-context local_user_ctx_1 --email user1@contoso.com --password nutanix/4u
```


# Autocompletion for bash/zsh
The kps CLI supports autocompletion with bash on MacOS and Linux. Using this command for zsh is experimental and not formally supported.
To configure auto-completion for your favorite shell, run this command and follow the instructions.
```
kps completion --help
```

# Using samples
Under `samples/` directory, there are samples for various Karbon Platform Services entities including Data Sources, Data Pipelines, Applications, etc. These samples can be used as a reference when creating your own Karbon Platform Services entities. Each entity has a README which explains the details of each individual attribute of that entity.
