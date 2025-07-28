from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "File_Type_Not_Supported"
    FILE_SIZE_EXCEEDED = "File_Size_Exceeded_It's_Limit"
    FILE_UPLOADED_SUCCESS = "File_Uploaded_Successfully"
    FILE_UPLOADED_FAILED = "File_Uploading_Failed"
    
