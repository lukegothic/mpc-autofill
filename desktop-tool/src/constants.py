"""
image_name Google Scripts API
Deployed at: https://script.google.com/macros/s/AKfycbw90rkocSdppkEuyVdsTuZNslrhd5zNT3XMgfucNMM1JjhLl-Q/exec
Usage: pass the Google Drive file ID as the `id` parameter of the POST request body.

function doPost(e) {
  return (function(id){
    var file = DriveApp.getFileById(id);
    return ContentService
      .createTextOutput(JSON.stringify({
        //result: file.getBlob().getBytes(),
        name: file.getName(),
        mimeType: file.getBlob().getContentType()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  })(e.parameters.id);
}


image_content Google Scripts API
Deployed at: https://script.google.com/macros/s/AKfycbw8laScKBfxda2Wb0g63gkYDBdy8NWNxINoC4xDOwnCQ3JMFdruam1MdmNmN4wI5k4/exec
Usage: pass the Google Drive file ID as the `id` parameter in a GET request.

function doGet(e) {
  return (function(id){
    var file = DriveApp.getFileById(id);
    var size = file.getSize();
    var result = [];
    if (size <= 30000000) {
      result = file.getBlob().getBytes();
    }
    return ContentService
      .createTextOutput(Utilities.base64Encode(result))
      .setMimeType(ContentService.MimeType.TEXT);
  })(e.parameter.id);
}
"""


from enum import Enum
from functools import partial

from PIL import Image

import src.webdrivers as wd


class States(str, Enum):
    initialising = "Initialising"
    defining_order = "Defining Order"
    paging_to_fronts = "Paging to Fronts"
    paging_to_backs = "Paging to Backs"
    paging_to_review = "Paging to Review"
    inserting_fronts = "Inserting Fronts"
    inserting_backs = "Inserting Backs"
    finished = "Finished"


class Faces(str, Enum):
    front = "Front"
    back = "Back"


class Cardstocks(str, Enum):
    S30 = "(S30) Standard Smooth"
    S33 = "(S33) Superior Smooth"
    M31 = "(M31) Linen"
    P10 = "(P10) Plastic"


class BaseTags(str, Enum):
    details = "details"
    fronts = "fronts"
    backs = "backs"
    cardback = "cardback"
    filepath = "filepath"


class DetailsTags(str, Enum):
    quantity = "quantity"
    bracket = "bracket"
    stock = "stock"
    foil = "foil"


class CardTags(str, Enum):
    id = "id"
    slots = "slots"
    name = "name"
    query = "query"


class Browsers(Enum):
    chrome = partial(wd.get_chrome_driver)
    brave = partial(wd.get_brave_driver)
    edge = partial(wd.get_edge_driver)
    # TODO: add support for firefox


class GoogleScriptsAPIs(str, Enum):
    # POST
    image_name = "https://script.google.com/macros/s/AKfycbw90rkocSdppkEuyVdsTuZNslrhd5zNT3XMgfucNMM1JjhLl-Q/exec"
    # GET
    image_content = "https://script.google.com/macros/s/AKfycbw8laScKBfxda2Wb0g63gkYDBdy8NWNxINoC4xDOwnCQ3JMFdruam1MdmNmN4wI5k4/exec"

    def __str__(self) -> str:
        return str(self.value)


class ImageResizeMethods(Enum):
    NEAREST = Image.NEAREST
    BOX = Image.BOX
    BILINEAR = Image.BILINEAR
    HAMMING = Image.HAMMING
    BICUBIC = Image.BICUBIC
    LANCZOS = Image.LANCZOS


DPI_HEIGHT_RATIO = 300 / 1110  # TODO: share this between desktop tool and backend


BRACKETS = [18, 36, 55, 72, 90, 108, 126, 144, 162, 180, 198, 216, 234, 396, 504, 612]
THREADS = 5  # shared between CardImageCollections
