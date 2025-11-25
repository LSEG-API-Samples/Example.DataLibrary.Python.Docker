# How to Containerization Data Library for Python Application

- Last update: November 2025
- Environment: Any with Python support 
- Compiler: Python
- Prerequisite: Delivery Platform (RDP) Access Credentials

## Overview

Containerization is a software deployment process that helps developers to package an application and it dependencies into a single portable unit. This unit can increase agility and portability to speed up software delivery anf flexible deployment. Containerization helps you deploy your application on your local server on expand to the Cloud easily. 

This article demonstrates how to containerization the [LSEG Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python) (aka Data Library version 2) application. This means you can package the application and run it anywhere without worrying about installing Python or managing dependencies on your local machine.

### What you'll learn

- How to containerize a Python application that accesses LSEG financial data
- How to connect to LSEG's cloud platform (Platform Session) from within a container
- How to build and run containers using Docker or Podman

### Technology used
- Data Library for Python version 2.1.1
- Python 3.12
- Docker or Podman (containerization tools)

## Benefits of Containerization

Containerization of applications offers many benefits as follows:

- Consistency: Containers encapsulate the application and its dependencies, so less issue of compatibility issues on various environments.
- Agility: Streamline software delivery process across peers such as QA and DevOps teams, enable automation workflow.
- Efficiency: Container is easiest way to virtualization.
- Isolation: Containers gives isolate environment that include all requires dependencies (libraries, config files, etc) that can run your application anywhere (that supports Container). 
- Portability: Easy deployment to different environments such as on-prem server or the Cloud.

And much more.

## What You'll Need

Before you begin, make sure you have:

1. **LSEG Credentials**: An account with access to the Delivery Platform (Data Platform) that includes Pricing and Historical Pricing permissions
   - *Don't have credentials?* Contact your LSEG representative for access
2. **Containerization Tool**: Either [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman-desktop.io/) installed on your computer
3. **Internet Connection**: Required to download packages and connect to LSEG services

## About the Data Library for Python

The [Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python) provides a set of ease-of-use interfaces offering coders uniform access to the breadth and depth of financial data and services available on the Workspace, RDP, and Real-Time Platforms. The API is designed to provide consistent access through multiple access channels and target both Professional Developers and Financial Coders. Developers can choose to access content from the desktop, through their deployed streaming services, or directly to the cloud. With the Data Library, the same Python code can be used to retrieve data regardless of which access point you choose to connect to the platform.

![Figure-1](images/datalib_image.png "Data Library Diagram") 

The Data Library are available in the following programming languages:

- [Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python)
- [.NET](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-net)
- [TypeScript](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-typescript)

**Want to learn more?** Check out these resources:
- [Quick Start Guide](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/quick-start)
- [Full Documentation](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/documentation)
- [Step-by-Step Tutorials](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/tutorials)
- [Code Examples on GitHub](https://github.com/LSEG-API-Samples/Example.DataLibrary.Python)

## Why Use "Platform Session" Access Point for Containers Demonstration?

The Data Library can connect to data in different ways:

- **Desktop Session**: Requires the LSEG Workspace desktop application running on your computer
- **Platform Session**: Connects directly to LSEG's [Delivery Platform](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis) (aka Data Platform, RDP) on the Cloud or the Real-Time Platform (on-prem or Cloud hosted). No desktop app needed.

For containerized applications, we use **Platform Session** because:

1. Containers can't access the Workspace desktop applications running on your host computer
2. Platform Session consumes data from cloud (or RTDS which can be connected from Container)
3. Your container can run anywhere with internet access (or access to your RTDS)

### What If I Am Using the Real-Time Platform Access Point?

Yes, you can containerize your Data Library application if you are connecting to your Real-Time Distribution System (RTDS). The container can connect to on-prem RTDS and Cloud/LSEG hosted RTDS. 

The local RTDS also supports containerization too. 

## Application Source Code

The example application source code uses simple Access Layer methods to get snapshot pricing and historical data.

If you have requirements to get more flexible API interfaces, you can use the Content and Delivery Layers too.


```python
try:
   # Open the data session
   ld.open_session()
   session = ld.session.get_default()
   session.open()
   if str(session.open_state) == 'OpenState.Opened':
      print('Session is opened')
      # request snapshot real-time data
      get_price_data(['THB=', 'JPY='],['BID', 'ASK'])
		
      print()
		# request historical data
      get_historical_interday_data(
         instruments=['AMD.O','NVDA.O'],
         fields=['BID','ASK','OPEN_PRC','HIGH_1','LOW_1','TRDPRC_1','NUM_MOVES','TRNOVR_UNS'])
      # Close session  
      print('Close Session')
      ld.close_session()
except Exception as ex:
    print(f'Error in open_session: {str(ex)}')
    sys.exit(1)
```

The code above uses the basic **ld.open_session()** method to load your RDP credential from the **lseg-data.config.json** that should be located on the same location as the code.

```json
{
    "logs": {....},
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
}
```

The **get_price_data()** method calls the Data Library **ld.get_data()** method for a snapshot real-time data.

```python
def get_price_data(instruments, fields):
    """ This method gets snapshot pricing data from RDP """
    print(f'Getting Snapshot Price data for {instruments} fields = {fields}')
    data = ld.get_data(universe=instruments, fields=fields)
    print(data)
```

The **get_historical_interday_data()** method calls the Data Library **ld.get_history()** method for a historical data.

```python
def get_historical_interday_data(instruments, fields):
    """
    This method sends a request message to RDP Historical Pricing service.

    Args:
        universe (str): RIC Code

    Returns: 
        interday data (Pandas Dataframe): Interday data in DataFrame object
    """
    print(f'Getting Historical Pricing Interday data for {instruments} fields = {fields}')
    # Time Variables
    interval = 'weekly' #weekly
    start_day = '2025-10-01'
    end_day = '2025-11-10'

    # Send request message
    response = ld.get_history(universe=instruments,
                        interval=interval, 
                        fields=fields,
                        count=15,
                        start=start_day,
                        end= end_day)
    print('This is a Historical Pricing Inter-Day data result from Data Library - Access Layer - get_history method')
    print(response)
```

That is all I have to say about the code.

## Image, Container, and Dockerfile

An Image is a read-only template or blueprint of your application including source code, runtime, libraries, and configurations. A [Dockerfile](https://docs.docker.com/build/concepts/dockerfile/) (aka Containerfile - for Podman) is like a recipe for creating Image. It contains a step-by-step needed to setup and run a software. 

A Container is instance of Image. It is an actual thing that runs your application.

Summary of key differences.

| Docker Image              | Docker Container            | 
|---------------------------|-----------------------------|
| Blueprint                 | Real instance               | 
| Static/unchanging         | Active/running              | 
| Storage on disk           | Running in memory           | 
|Can't execute alone        | Actually does the work      |
|Create once, use many times| Create from image each time |

**Note**: Podman is fully compatible with Dockerfile.

You can find more details on the following resources:

- [What’s the Difference Between Docker Images and Containers?](https://aws.amazon.com/compare/the-difference-between-docker-images-and-containers/)
- [Docker image vs container: What are the differences?](https://circleci.com/blog/docker-image-vs-container/)
- [Running a pod using a container or docker file](https://podman-desktop.io/tutorial/running-a-pod-using-a-container-docker-file)

## Data Library for Python Dockerfile

I am demonstrating the Data Library for Python Dockerfile (or Containerfile) using a **single-stage build** which is a simplest way to create an Image. The single-stage build means all instructions for building and running an application are contained in one Dockerfile stage. An intention is to make it easy to understand as much as possible.

```Dockerfile
ARG PYTHON_VERSION=3.12
ARG VARIANT=slim-bookworm
FROM docker.io/python:${PYTHON_VERSION}-${VARIANT}

LABEL maintainer="LSEG Developer Relations"

COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
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

The first instruction is define a **FROM** instruction to specify the base image to use. I am using the **ARG** [build arguments](https://docs.docker.com/build/building/variables/#arg-usage-example) to set the Python version and variant.

```Dockerfile
ARG PYTHON_VERSION=3.12
ARG VARIANT=slim-bookworm
FROM docker.io/python:${PYTHON_VERSION}-${VARIANT}
```

I am using Python 3.12 with a slim version Debian 12 (Bookworm) OS. I am not using the *Alpine* which is the lightest variant because it is hard to install [Pandas](https://pandas.pydata.org/) which is required for the Data Library for Python.

The next step is copy Python dependencies file [requirements.txt](https://pip.pypa.io/en/stable/reference/requirements-file-format/) to the image and run **pip install* to install all project dependencies.

```Dockerfile
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir --no-warn-script-location --user -r requirements.txt
```

Please be noticed that I am using **--trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org** arguments to **workaround** LSEG beloved ZScaler that blocks access to [PyPI](https://pypi.org/) repository. If your environment does have this stupid limitation, please use the following instructions instead.

```Dockerfile
COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt
```

Next, I am setting an Image environment variables about the character encoding and stdout/stderr on the terminal console. I also set the working directory of an Image.

```Dockerfile
WORKDIR /app

# Update PATH environment variable + set Python buffer to make Docker print every message instantly.
ENV PATH=/root/.local:$PATH \
    PYTHONUNBUFFERED=1\
    PYTHONIOENCODING=utf-8\
    PYTHONLEGACYWINDOWSSTDIO=utf-8
```

Then I am copying the source code **ld_app.py** and **lseg-data.config.json** configuration file to an Image.

```Dockerfile
#Copy application files
COPY ["ld_app.py", "lseg-data.config.json", "/app/"]
```

And lastly, I use the **ENTRYPOINT** ([reference](https://docs.docker.com/reference/dockerfile/#entrypoint)) to run a python application.

```Dockerfile
#Run Python
ENTRYPOINT ["python", "/app/ld_app.py"]
```

Now this Dockerfile/Containerfile is ready to create an Image.

For references about Dockerfile/Containerfile, please see the following resources:

- [Write your first Containerfile for Podman](https://www.redhat.com/en/blog/write-your-first-containerfile-podman)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)

## Step 1: Creating An Image

Now we come to Image building steps. I am demonstrating with [podman-build] command, but if you're using Docker, simply replace ***podman*** with ***docker***.

The first step to build Image is open a command prompt or terminal application and navigate to the project folder, then run the following command to create an Image name *ld_app*.

```bash
podman build -t ld_app .
```

This process may take a few minutes as it downloads and installs everything needed.

When complete, verify the image was created with the following command:

```bash
podman images
```

You should see *ld_app* Image in the list.

![figure-2](images/ld_docker_1.png "ld library python app image is created")

That’s all I have to say about how to build an Image.

## Step 2: Running A Container

Now, what about how to run a Container from this newly created Image. You can run a Container with the following command:

```bash
podman run -it --name ld_app ld_app
```

**Note**: Please let me remind you, use ```docker``` instead of ```podman``` if you are using Docker.

Your application will now run and connect to LSEG's data platform!

![figure-3](images/ld_docker_2.png "run ld_app container")

To stop a Container, press ```Ctrl+C``` button or run ```podman stop ld_app``` command.

Please see more detail on [podman stop](https://docs.podman.io/en/stable/markdown/podman-stop.1.html) command document.

## Step 3: Cleanup (Optional)

That brings us to clean up a Container. Once you have stopped a Container, you cannot run a Container with the same name until you delete it (or just change a Container name). 

You can delete a Container with the following command:

```bash
podman rm ld_app
```

Please see more detail on [podman rm](https://docs.podman.io/en/stable/markdown/podman-rm.1.html) and [podman container cleanup](https://docs.podman.io/en/stable/markdown/podman-container-cleanup.1.html) commands documents.

![figure-4](images/ld_docker_3.png "deleting ld_app container")

Optionally, you can delete an Image with the following command (all associated Containers must be removed).

```bash
podman rmi ld_app
```

![figure-5](images/ld_docker_4.png "deleting ld_app image")

You can find more detail about this command on the [podman rmi](https://docs.podman.io/en/latest/markdown/podman-rmi.1.html) document page.

That covers how to run and cleanup Container.

## What if I am using Docker?

The Containerfile/Dockerfile supports Docker Containerization tool. You can just replace the ```podman``` command on step 1,2, and 3 with ```docker```.  I have tested the project with Docker and it works fine.

![figure-6](images/ld_docker_mac_1.png "docker image result")

![figure-7](images/ld_docker_mac_2.png "docker container run result")

## Conclusion

Congratulations! You've successfully containerized a Data Library for Python application. You now have a portable, self-contained package that can run consistently across different environments—from your local development machine to production servers or cloud platforms.

### What You've Accomplished

In this article, you learned how to:

- **Package a Python application** with all its dependencies into a container image
- **Connect to LSEG's Data Platform** from within a containerized environment
- **Build and run containers** using either Docker or Podman
- **Understand key concepts** like Images, Containers, and Dockerfile/Containerfile

### Key Benefits You Can Now Leverage

By containerizing your Data Library application, you've unlocked several advantages:

- **Consistency**: Your application will run the same way regardless of where you deploy it
- **Portability**: Easily move your application between development, testing, and production environments
- **Isolation**: Your application and its dependencies won't conflict with other software on your system
- **Simplified Deployment**: Deploy to cloud platforms or on-premises servers with minimal configuration
- **Reproducibility**: Share your containerized application with team members who can run it immediately

### Next Steps

Now that you understand the basics of containerization, consider exploring:

- **Multi-stage builds** to create smaller, more optimized images
- **Docker Compose or Podman Compose** for managing multi-container applications
- **Cloud deployment** to platforms like AWS, Azure, or Google Cloud
- **Orchestration tools** like Kubernetes for managing containers at scale
- **CI/CD pipelines** to automate building and deploying your containers

## References

For more information about containerization and LSEG Data Library:

- [LSEG Data Library for Python](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python) page on the [LSEG Developers Portal](https://developers.lseg.com/en) website.
- [LSEG Data Library for Python Documentation](https://developers.lseg.com/en/api-catalog/lseg-data-platform/lseg-data-library-for-python/documentation).
- [LSEG Data Library Examples on GitHub](https://github.com/LSEG-API-Samples/Example.DataLibrary.Python).
- [LSEG Delivery Platform](https://developers.lseg.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-platform-apis).
- [Podman Documentation](https://docs.podman.io/en/latest/).
- [Getting Started with Podman](https://podman.io/docs).
- [Docker Documentation](https://docs.docker.com/).
- [Getting Started with Docker](https://docs.docker.com/get-started/)
- [Benefits of Containerization](https://circleci.com/blog/benefits-of-containerization/)
- [What is Containerization? - AWS](https://aws.amazon.com/what-is/containerization/)
- [Containerization for Python Developers](https://medium.com/@ebojacky/back-end-engineering-containerization-for-python-developers-4d79933eb5b0)
- [The Benefits of Containerization - IBM](https://www.ibm.com/think/insights/the-benefits-of-containerization-and-what-it-means-for-you)


For any questions related to this example or the LSEG Data Library, please use the Developer Community [Q&A Forum](https://community.developers.refinitiv.com/).