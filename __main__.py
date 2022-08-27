import pathlib
from pprint import pprint
from os import listdir
from PIL import Image
from inky.auto import auto
# import pyheif

PHOTOS_DIRECTORY = '/opt/inky-photos'


def display_photo(display, photo_path: pathlib.Path, aspect_ratio: float) -> None:
    """
    test_function does blah blah blah.

    :param photo_path: Path to photo file we're processing
    :param aspect_ratio: Desired aspect ratio, in width/height
    """

    # read the photo in
    # if photo_path.suffix.lower() == "heic":
        # heif_file = pyheif.read(photo_path)
        # image = Image.frombytes(
        #     heif_file.mode,
        #     heif_file.size,
        #     heif_file.data,
        #     "raw",
        #     heif_file.mode,
        #     heif_file.stride,
        # )
    # else:
    image = Image.open(photo_path)

    # crop to desired aspect ratio
    thing = 1

    # scale the photo

    # dither

    # display
    display.set_image(image)
    display.show()


    # color = display.color
    # resolution = display.resolution

    # pprint(color)
    # pprint(resolution)

    # apiKey = API_KEY_OVERRIDE if API_KEY_OVERRIDE else os.environ.get('GOOGLE_API_KEY')
    #
    # if apiKey is None:
    #     raise RuntimeError(f"Missing required env var GOOGLE_API_KEY")
    #
    # # Build the Google Sheets API interface
    # sheetConfigs = yaml.load(open('app/config/sheets.yaml', 'r'), Loader=yaml.FullLoader)
    # apiService = build('sheets', 'v4', developerKey=apiKey)
    # sheetInterface = apiService.spreadsheets()
    #
    # # Iterate over our sheet configurations
    # for sheetConfig in sheetConfigs:
    #     sheetId = sheetConfig['sheetId']
    #     if sheetId is None:
    #         raise RuntimeError(f"Missing sheetId in sheet config")
    #
    #     outputFilename = sheetConfig['outputFilename']
    #     if outputFilename is None:
    #         raise RuntimeError(f"Missing outputFilename for sheet config with sheetId {sheetId}")
    #
    #     cellRange = sheetConfig['range']
    #     if cellRange is None:
    #         raise RuntimeError(f"Missing range for sheet config with sheetId {sheetId}")
    #
    #     # Call the Sheets API to get the actual values
    #     result = sheetInterface.values().get(spreadsheetId=sheetId,
    #                                          range=cellRange).execute()
    #     values = result.get('values', [])
    #
    #     if not values:
    #         print(f"No data fetched for sheet {sheetId}")
    #         continue
    #
    #     # Open CSV file for writing
    #     with open(f"output/{sheetConfig['outputFilename']}", 'w', newline='') as csvFile:
    #         # Using the Unix dialect for now because it seems the most reasonable. Can switch to Excel if it makes
    #         #   more sense for whomever is using this output.
    #         writer = csv.writer(csvFile, dialect='unix')
    #         writer.writerows(values)
    # # cleanup
    # print(f"Successfully processed {len(sheetConfigs)} sheets")


if __name__ == '__main__':
    print("Running inky photo display")

    # Initialization
    display = auto()
    height = display.height
    width = display.width
    aspect_ratio = width / height

    photo_files = listdir(PHOTOS_DIRECTORY)

    display_photo(display, pathlib.Path(PHOTOS_DIRECTORY + '/' + photo_files[0]), aspect_ratio)

    # Event loop
