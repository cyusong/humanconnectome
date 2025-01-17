# 3D GenomeConnectome Database

Welcome to the 3D Genome Connectome project!  The project is currently in its infancy stages; the latest version of this project is live at: [https://3dgenomeconnectome.herokuapp.com/](https://powerful-tor-67991-ea0c206d8603.herokuapp.com/).

This GitHub repository is publicly-accessible and serves as a means of hosting the project's application and storing the code generated for this project!

## What is 3D GenomeConnectome?

3D GenomeConnetome is a database that contains over 95000 entities with several thousand interaction types between the said amount of entities.  These entities and interactions were obtained from having GPT process over 20000 paper abstracts from various popular scientific journals.

## Folders of this Repository

This repository contains files and folders that are crucial in getting 3D GenomeConnectome up and running, of which include:

1.  `static`

    This folder contains images, CSS, and JavaScript that 3D GenomeConnectome's pages use.  All CSS are stored in the `css` sub-directory while all JS are stored in the `js` sub-directory.

1.  `templates`
    
    This folder contains HTML templates that will be rendered and displayed to the user.

1.  `tests`
    
    This folder contains unit tests (so far) to ensure that the application is running smoothly.

1.  `utils` 

    This folder contains utility functions that are used by the routes to perform certain functionalities.

1.  `routes`

    This folder contains the applicaton's routes.