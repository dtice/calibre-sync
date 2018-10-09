**UNDER CONSTRUCTION**
# Calibre Sync 
### Allows you to synchronize your calibre library using a Google Drive account

#### Psuedocode:
```python
def synchronize():
	if(!directory_on_GDrive()):
		create_directory_on_GDrive("calibre_sync_library")
		print("No files to synchronize!")
	else:
		for every artist in path_to_calibre_library:
			for every book in artist:
				if !file_exists(remote) && file_exists(local):
					push_remote_dir("artist/book/*")
```
