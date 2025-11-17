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

- https://medium.com/@ebojacky/back-end-engineering-containerization-for-python-developers-4d79933eb5b0
- https://circleci.com/blog/benefits-of-containerization/
- https://aws.amazon.com/what-is/containerization/
- https://www.ibm.com/think/insights/the-benefits-of-containerization-and-what-it-means-for-you