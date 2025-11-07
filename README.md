# How to run Data Library for Python in Docker

## Overview

This example project shows how to use [LSEG Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python) (aka Data Library version 2) with Container using the Platform Session.

I am demonstrating with library version 2.1.1,Python 3.12, and [Podman](https://podman-desktop.io/) as a Containerization tool. However, the project supports [Docker](https://www.docker.com/) as well.

## <a id="prerequisite"></a> Prerequisite

This example requires the following dependencies.

1. Delivery Platform (aka Data Platform) credential with Pricing and Historical Pricing permission.
2. [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman-desktop.io/) Containerization tool.
3. Internet connection.

Please contact your LSEG representative to help you to access the RTO account and services.

## <a id="rdp_lib"></a>Introduction to the Data Library for Python

The [Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python) provides a set of ease-of-use interfaces offering coders uniform access to the breadth and depth of financial data and services available on the Workspace, RDP, and Real-Time Platforms. The API is designed to provide consistent access through multiple access channels and target both Professional Developers and Financial Coders. Developers can choose to access content from the desktop, through their deployed streaming services, or directly to the cloud. With the Data Library, the same Python code can be used to retrieve data regardless of which access point you choose to connect to the platform.

![Figure-1](images/datalib_image.png "Data Library Diagram") 

The Data Library are available in the following programming languages:

- [Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python)
- [.NET](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-net)
- [TypeScript](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-typescript)

For more deep detail regarding the Data Library for Python, please refer to the following articles and tutorials:

- [Quickstart](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/quick-start).
- [Documentation](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/documentation).
- [Tutorials](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/tutorials).
- [GitHub](https://github.com/LSEG-API-Samples/Example.DataLibrary.Python).

## Why Platform Session?

The Data Library supports Workspace ("Desktop Session"), Delivery/Data Platform ("Platform Session"), and the Real-Time Platform.  The "Desktop Session" needs the [LSEG Workspace Desktop Application](https://www.lseg.com/en/data-analytics/search/workspace) as an api proxy between the library and the Workspace platform. However, the Workspace desktop application does not support Containerization, so you cannot use a "Desktop Session".

That is when the "Platform Session" comes in. This session connects and consumes data from the [Delivery Platform](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) (aka Data Platform, or RDP) on the Cloud. It is suitable for Container application which can be run anywhere.

## Why not using get_data method?

You might wondering why I am not demonstrating with the ```ld.get_data()``` method. I found that the ```ld.get_data()``` works best with the Desktop session. The [Content Layer - Pricing object](https://cdn.refinitiv.com/public/lseg-lib-python-doc/2.0.0.2/book/en/sections/content-layer/pricing/about-pricing.html) is more suitable for the Platform Session.

## Dockerfile

I am using a basic single stage Dockerfile as follows:

```ini
ARG PYTHON_VERSION=3.12
ARG VARIANT=slim-bookworm
FROM docker.io/python:${PYTHON_VERSION}-{VARIANT}

LABEL maintainer="LSEG Developer Relations"

COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
#RUN pip install --upgrade pip && \
#    pip install --no-cache-dir --user -r requirements.txt
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir --no-warn-script-location --user -r requirements.txt

WORKDIR /app

# Update PATH environment variable + set Python buffer to make Docker print every message instantly.
ENV PATH=/root/.local:$PATH \
    PYTHONUNBUFFERED=1\
    PYTHONIOENCODING=utf-8\
    PYTHONLEGACYWINDOWSSTDIO=utf-8
#Copy application files
COPY ["ld_app.py", "lseg-data.config.json", "/app/"]

#Run Python
ENTRYPOINT ["python", "/app/ld_app.py"]
```

The use of ```--trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir``` command is to avoid LSEG beloved [Zscaler](https://www.zscaler.com/) that blocks access to [PyPI](https://pypi.org/) repository by default (don't ask me why). 

The command bypass SSL certificate verification. If you need the SSL verification, please change Dockerfile's ```RUN``` commands to the following statements:

```ini
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt
```

## How to run an application with Containerization Tool

I am demonstrating with Podman (```podman``` command), but you can change it to ```docker``` if you are using Docker.

The first step is to unzip or download the example project folder into a directory of your choice. 

1. Open the ```lseg_data.config.json``` file and add your RDP information based on your preference

    ```json
    "sessions": {
        "default": "platform.ldp",
        "platform": {
            "ldp": {
                "app-key": "YOUR APP KEY GOES HERE!",
                "username": "YOUR LDP LOGIN OR MACHINE GOES HERE!",
                "password": "YOUR LDP PASSWORD GOES HERE!",
                "signon_control":true
            },
            "ldpv2":{
                "client_id": "Service-ID (Client ID V2)",
                "client_secret": "Client Secret",
                "signon_control":true,
                "app-key": ""
            }
        }
    }
    ```
2. Please note that the ```platform``` configuration is based on your connection information:
    
    - if you are using the RDP with the *Version 1 Authentication* (Machine-ID), the ```default``` value must be ```platform.ldp```.
    - if you are using the RDP with the *Version 2 Authentication* (Service-ID), the ```default``` value must be ```platform.ldpv2```.

3. Open a command prompt application and go to the project folder
4. Run the following command in a console to build an image from a Dockerfile.

    ```bash
    podman build -t ld_app .
    ```
5. Once the build is a succeed, you will see a newly created image via a ```podman images``` comand

    ![figure-1](images/ld_docker_1.png "ld library python app image is created")

6. Run a container of this *ld_app* image with the following command

    ```bash
    podman run -it --name ld_app  ld_app
    ```

    ![figure-2](images/ld_docker_2.png "run ld_app container")

7. Press ```Ctrl+C``` to stop an application.
8. To delete a container, run the following command

    ```bash
    podman rm ld_app
    ```

    ![figure-3](images/ld_docker_3.png "deleting ld_app container")

9. To delete the *ld_app* image, run the following command (after you have deleted its containers)

    ```bash
    podman rmi ld_all
    ```

    ![figure-4](images/ld_docker_4.png "deleting ld_app image")

## <a id="references"></a>References

For further details, please check out the following resources:

- [LSEG Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python)
- [Data Platform](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis)
- [Account authorization V1 to V2 migration cheat sheet](https://developers.lseg.com/en/article-catalog/article/account-authorization-v1-to-v2-migration-cheat-sheet) article.
- [Essential Guide to the Data Libraries - Generations of Python library (EDAPI, RDP, RD, LD)](https://developers.lseg.com/en/article-catalog/article/essential-guide-to-the-data-libraries)
- [LSEG Data Library for Python and its Configuration Process](https://developers.lseg.com/en/article-catalog/article/configuration-process)
- [A beginner's guide to Python containers](https://developers.redhat.com/articles/2023/09/05/beginners-guide-python-containers#)
- [How to “Dockerize” Your Python Applications](https://www.docker.com/blog/how-to-dockerize-your-python-applications/)
- [Containerize a Python application](https://docs.docker.com/guides/python/containerize/)

For any questions related to this example or the LSEG Data Library, please use the Developer Community [Q&A Forum](https://community.developers.refinitiv.com/).