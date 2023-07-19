# reaxpro-marketplace-api

The development is still progress.
TODO:
1. support token reconfigure for the reaxpro user in market place when session times out. Currently, we have to manually copy the token into the cli file and or any test file where we initiate the execution. Refer test.py file and cli.py files in repositories.
2. Docker support
3. If the datasink design changes in market place then we have to reimplement some of the logic.
4. Update the readme file after docker support
5. All the functionalities has to be tested again

Note: Some of the functionalities from vimpp are not supported. For example there is no property field supported for digital objects, and currently the digital objects are downloded only "as-directories".


# Some basic commands to test cli functionalities. (change the value based on your usecases)
mpsession_search_information_packages --search-query "title=upload_test_dir"
mpsession_ingest_digital_objects_from_paths -t "cli_test" -p "/root/symphony/upload_test_dir/test1.txt"
mpsession_ingest_digital_objects_from_sourcedir -t "cli_test123" -s "/root/symphony/upload_test_dir"
mpsession_download_digital_objects_from_search_query -s "title=upload_test_dir" -d "/root/symphony/download_test"
