## Automate notification to Chat mediums with Python

This is a sample reference repository for my blog post [A Simple ChatOps with Python](). 

Webhooks and ChatOps are part of modern DevOps in automating event management and notification in any SDLC platform

- Create a virtual environment
- Install the requirements
- Add the ACCESS_URL of the MS-Team's Configured [connector](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/what-are-webhooks-and-connectors)(capture and expose as environment variable)
- Add image urls for your chat messages.
- Set a threshold value for your CPU and Memory limit with SET_CPU_LIMIT and SET_MEMORY_LIMIT
- Deploy it in a server, configure a cronjob and get notified if CPU and Memory usage reaches above the threshold. 
  