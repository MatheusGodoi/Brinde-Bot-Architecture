# Utils

This folder is used to store functions that can be used on other cogs, in a generic manner. <br>
Due to the nature of python imports, a empty *__init__.py* to allow for its usage.

## Present utils

The following utils are included by default:

[voice_channel.py](/src/utils/voice_channel.py)
**connect** Made to allow for voice channel connecting<br>
**disconnect** Made to allow for voice channel disconnecting<br>

[cogfile_manage.py](/src/utils/cogfile_manage.py)
**clearCogFile** Made to empty the entire cog file<br>
**writeCommentCogFile** Made to write the comment section in a cog file<br>
**writeCogFile** Made to write a list of cogs in the cog file<br>
**readCogFile** Made to read the cog file and return all cogs (even deactivated ones)<br>
