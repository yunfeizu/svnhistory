TODO List
===========

Features to be supported
-----------
* TODO: generate change report between builds or revisions for testers 
* TODO: generate review protocol for project management


Functionality to be improved:
-----------
* TODO: support mirror server settings
* TODO: support filter by date and revisions in CodeHistoryViewer
* TODO: add clear search kewords button on CodeHistoryViewer

Bug to be fixed:
-----------
* Done: fix diff with new added file
* Done: exception handle when not starting in work path
* Done: segmentation error on ubuntu 
        reason: pysvn.Client().root_url_from_path() crashes, use info2() instead
